const https = require("https");
const querystring = require("querystring");
const constants = require("../config/constants");
const { withRetry } = require("../utils/retry");
const { ApiError, NetworkError, TimeoutError, AuthError } = require("./errors");
const utils = require("../utils/utils");

async function request(options, data = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(
      { ...options, timeout: constants.REQUEST_TIMEOUT },
      (res) => {
        res.setEncoding("utf-8");
        let body = "";
        res.on("data", (chunk) => (body += chunk));
        res.on("end", () => {
          if (res.statusCode === 200) {
            try {
              const jsonBody = JSON.parse(body);
              if (jsonBody.errcode === 0) {
                resolve(jsonBody);
              } else {
                reject(
                  new ApiError(
                    jsonBody.errcode.toString(),
                    jsonBody.errmsg || "请求失败",
                  ),
                );
              }
            } catch (parseError) {
              reject(new NetworkError(`响应解析失败: ${parseError.message}`));
            }
          } else if (res.statusCode === 401 || res.statusCode === 403) {
            reject(
              new AuthError(
                "GUAIKEI_API_TOKEN 无效, 请检查环境变量 或 联系微信: 13395823479 获取解决方案",
              ),
            );
          } else {
            reject(
              new ApiError(
                `HTTP_${res.statusCode}`,
                `请求失败, 状态码: ${res.statusCode}`,
              ),
            );
          }
        });
      },
    );

    req.on("error", (err) => {
      if (err.code === "ETIMEDOUT" || err.code === "ECONNRESET") {
        reject(new TimeoutError("请求超时或连接被重置"));
      } else {
        reject(new NetworkError(`网络错误: ${err.message}`));
      }
    });

    req.on("timeout", () => {
      req.destroy();
      reject(new TimeoutError(`请求超时 (${constants.REQUEST_TIMEOUT}ms)`));
    });

    if (data) {
      req.write(data);
    }
    req.end();
  });
}

async function postJson(path, params, data) {
  if (!path || typeof path !== "string") {
    throw new Error("path 必须是非空字符串");
  }
  if (!params || typeof params !== "object") {
    throw new Error("params 必须是对象");
  }
  if (!data || typeof data !== "object") {
    throw new Error("data 必须是对象");
  }

  const fullPath = `${path}?${querystring.stringify(params)}`;
  const jsonData = JSON.stringify(data);

  const options = {
    host: constants.BASE_URL,
    path: fullPath,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Content-Length": Buffer.byteLength(jsonData),
    },
  };

  return await request(options, jsonData);
}

async function getJson(path, params) {
  if (!path || typeof path !== "string") {
    throw new Error("path 必须是非空字符串");
  }
  if (!params || typeof params !== "object") {
    throw new Error("params 必须是对象");
  }

  const fullPath = `${path}?${querystring.stringify(params)}`;
  const options = {
    host: constants.BASE_URL,
    path: fullPath,
    method: "GET",
  };

  return await request(options);
}

/**
 * 通用 API 请求方法
 * @param {string} method - HTTP 方法 (GET/POST)
 * @param {string} path - 请求路径
 * @param {object} params - URL 参数
 * @param {object} [data] - 请求体数据 (仅 POST)
 * @param {number} maxAttempts - 最大重试次数
 * @param {string} actionName - 操作名称（用于日志）
 * @returns {Promise<object>} API 响应
 */
async function requestApi(method, path, params, data, maxAttempts, actionName) {
  return await withRetry(
    async () => {
      let response;
      if (method === "POST") {
        response = await postJson(path, params, data);
      } else {
        response = await getJson(path, params);
      }
      return response;
    },
    maxAttempts,
    (attempt, err) => {
      utils.printError(
        `【${actionName}重试】 ${attempt + 1}/${maxAttempts} 次 - ${err.message}`,
      );
    },
  );
}

module.exports = { getJson, postJson, requestApi };
