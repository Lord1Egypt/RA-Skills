const constants = require("../config/constants");
const utils = require("../utils/utils");
const { skillName } = require("../utils/name");
const { withRetry } = require("./retry");
const {
  SkillError,
  ApiError,
  NetworkError,
  TimeoutError,
  AuthError,
} = require("./errors");
const https = require("https");
const querystring = require("querystring");

const AUTH_MESSAGE =
  "GUAIKEI_API_TOKEN 无效, 请检查环境变量 或 联系微信: 13395823479 获取解决方案";

async function request(options, data = null) {
  return new Promise((resolve, reject) => {
    let timedOut = false;
    let settled = false;
    const finish = (fn, value) => {
      if (settled || timedOut) return;
      settled = true;
      fn(value);
    };

    const req = https.request(
      { ...options, timeout: constants.REQUEST_TIMEOUT },
      (res) => {
        res.setEncoding("utf-8");
        res.on("error", (err) => {
          finish(reject, new NetworkError(`响应流错误: ${err.message}`));
        });
        let body = "";
        res.on("data", (chunk) => {
          body += chunk;
          if (body.length > 10 * 1024 * 1024) {
            finish(reject, new NetworkError("响应体超过 10MB"));
            req.destroy();
          }
        });
        res.on("end", () => {
          if (timedOut || settled) return;
          if (res.statusCode === 200) {
            try {
              const jsonBody = JSON.parse(body);
              if (typeof jsonBody.errcode !== "number") {
                finish(
                  reject,
                  new ApiError("API_ERROR", "接口响应缺少有效的 errcode", true),
                );
              } else if (jsonBody.errcode === 0) {
                finish(resolve, jsonBody);
              } else if (jsonBody.errcode === 401 || jsonBody.errcode === 403) {
                finish(reject, new AuthError(AUTH_MESSAGE));
              } else if (jsonBody.errcode === 410) {
                finish(reject, new ApiError("410", "TOKEN 状态异常", true));
              } else {
                const errmsg = jsonBody.errmsg || "请求失败";
                const pending =
                  jsonBody.errcode === 1 || errmsg.includes("处理中");
                const noRetry =
                  jsonBody.errcode >= 10 ||
                  (jsonBody.errcode !== 1 && jsonBody.errcode !== 0 && !pending);
                finish(
                  reject,
                  new ApiError(jsonBody.errcode.toString(), errmsg, noRetry),
                );
              }
            } catch (parseError) {
              finish(
                reject,
                new NetworkError(`响应解析失败: ${parseError.message}`),
              );
            }
          } else if (res.statusCode === 401 || res.statusCode === 403) {
            finish(reject, new AuthError(AUTH_MESSAGE));
          } else {
            const status = res.statusCode;
            const serverError = status >= 500 && status <= 599;
            const code = serverError ? "HTTP_5xx" : `HTTP_${status}`;
            finish(
              reject,
              new ApiError(
                code,
                `请求失败, 状态码: ${status}`,
                !serverError,
              ),
            );
          }
        });
      },
    );

    req.on("error", (err) => {
      if (timedOut || settled) return;
      if (err.code === "ETIMEDOUT" || err.code === "ECONNRESET") {
        finish(reject, new TimeoutError("请求超时或连接被重置"));
      } else {
        finish(reject, new NetworkError(`网络错误: ${err.message}`));
      }
    });

    req.on("timeout", () => {
      if (settled) return;
      timedOut = true;
      settled = true;
      req.destroy();
      reject(new TimeoutError(`请求超时 (${constants.REQUEST_TIMEOUT}ms)`));
    });

    if (data) req.write(data);
    req.end();
  });
}

async function postJson(path, token, data) {
  if (!path || typeof path !== "string") {
    throw new SkillError("PATH_INVALID", "路径 必须是非空字符串", true);
  }
  if (!token || typeof token !== "string") {
    throw new SkillError("TOKEN_INVALID", "token 必须是非空字符串", true);
  }
  if (!data || typeof data !== "object") {
    throw new SkillError("DATA_INVALID", "数据 必须是对象", true);
  }

  const params = { _: Date.now(), skill_name: skillName() };
  const fullPath = `${path}?${querystring.stringify(params)}`;
  const jsonData = JSON.stringify(data);

  const options = {
    host: constants.BASE_URL,
    path: fullPath,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept-Encoding": "identity",
      "Content-Length": Buffer.byteLength(jsonData),
      TOKEN: token,
    },
  };

  return await request(options, jsonData);
}

/**
 * 查询接口的轮询分类。
 * errcode 1 表示处理中，继续等。11-14 为入参/任务错误，立即失败。
 * 其它业务错误立即失败。网络错误、请求超时和 HTTP 5xx 可以继续查。
 * @param {Error} error
 * @returns {"pending"|"fail"|"retry"}
 */
function classifyPollError(error) {
  const message = error && error.message ? String(error.message) : "";
  if (error && String(error.code) === "1") return "pending";
  if (message.includes("处理中")) return "pending";
  if (error && error.code === "HTTP_5xx") return "retry";
  if (
    error &&
    (error.noRetry || error.name === "ApiError" || error.name === "AuthError")
  ) {
    return "fail";
  }
  return "retry";
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * 创建类请求。网络错误、超时和 HTTP 5xx 会重试；认证失败、业务错误码 >= 10，以及非「处理中」的 errcode 1，立即失败。
 */
async function requestApi(path, token, data, maxAttempts, actionName) {
  return await withRetry(
    async () => {
      return await postJson(path, token, data);
    },
    maxAttempts,
    (attempt, error) => {
      utils.printError(
        `【${actionName}重试】${attempt + 1}/${maxAttempts} 次 - ${error.message}`,
      );
    },
  );
}

/**
 * 轮询视频文案。间隔从 RETRY_INTERVAL 起按 2、4、8 秒翻倍，单次最长 RETRY_MAX_INTERVAL。
 * 次数用尽仍是「处理中」时抛出 STILL_PROCESSING，不把未完成当成空结果。
 */
async function pollTaskResult(path, token, data, actionName) {
  const maxAttempts = constants.QUERY_MAX_ATTEMPTS;
  let lastError;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      return await postJson(path, token, data);
    } catch (error) {
      lastError = error;
      const kind = classifyPollError(error);
      if (kind === "fail") throw error;
      if (kind === "pending") {
        utils.printInfo(
          `【${actionName}】处理中 ${attempt + 1}/${maxAttempts}`,
        );
      } else {
        utils.printError(
          `【${actionName}重试】${attempt + 1}/${maxAttempts} 次 - ${error.message}`,
        );
      }
      if (attempt < maxAttempts - 1) {
        const delay = Math.min(
          constants.RETRY_INTERVAL * 2 ** attempt,
          constants.RETRY_MAX_INTERVAL,
        );
        await sleep(delay);
      }
    }
  }
  if (classifyPollError(lastError) === "pending") {
    throw new SkillError("STILL_PROCESSING", "视频仍在处理中", true);
  }
  throw lastError || new SkillError("STILL_PROCESSING", "视频仍在处理中", true);
}

module.exports = { requestApi, pollTaskResult, classifyPollError };
