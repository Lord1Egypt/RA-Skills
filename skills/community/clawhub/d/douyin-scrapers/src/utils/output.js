/**
 * stdout 信封。成功/错误/空结果均 write + drain 后再结束。
 * 成功路径：先落盘（可选）→ 刷 stdout → stderr 提示 → exit(0)。
 */
const constants = require("../config/constants");
const log = require("./log");
const utils = require("./utils");
const { formatBeijingTime } = require("./time");

/**
 * 把 JSON 写到 stdout，在 drain/写完回调后 resolve。
 * 管道已关闭（EPIPE）时仍 resolve，避免未捕获异常。
 * @param {object} payload
 * @returns {Promise<void>}
 */
function writeJson(payload) {
  const text = JSON.stringify(payload, null, 2) + "\n";
  return new Promise((resolve) => {
    process.stdout.write(text, (err) => {
      if (err && err.code !== "EPIPE") {
        try {
          process.stderr.write(`stdout 写入失败: ${err.message}\n`);
        } catch (_) {
          /* ignore */
        }
      }
      resolve();
    });
  });
}

/**
 * 把 JSON 写到 stdout，刷出后再按退出码结束。
 * @param {object} payload
 * @param {number} exitCode
 */
function writeJsonAndExit(payload, exitCode) {
  writeJson(payload).then(() => {
    process.exit(exitCode);
  });
}

function buildEnvelope({
  status,
  errorCode,
  message,
  request,
  startTime,
  results = null,
  total,
}) {
  const metadata = {
    skill_version: constants.VERSION,
    runtime_version: process.versions.node,
    execution_time: startTime == null ? 0 : Date.now() - startTime,
  };
  if (total !== undefined) {
    metadata.total = total;
  }
  return {
    status,
    error_code: errorCode,
    message,
    timestamp: formatBeijingTime(new Date()),
    request,
    metadata,
    results,
  };
}

function buildSuccessEnvelope(message, startTime, request, results, total) {
  return buildEnvelope({
    status: "success",
    errorCode: "OK",
    message,
    request,
    startTime,
    results,
    total,
  });
}

/**
 * 成功收尾：可选先写日志，再 flush stdout，再 stderr 提示，最后 exit(0)。
 * @param {object} payload
 * @param {{ logFilename?: string, stderrMessage?: string }} [opts]
 */
async function finishSuccess(payload, opts = {}) {
  const { logFilename, stderrMessage } = opts;
  if (logFilename) {
    await log.writeResultLog(
      logFilename,
      JSON.stringify(payload, null, 2),
    );
  }
  await writeJson(payload);
  if (stderrMessage) {
    utils.printSuccess(stderrMessage);
  }
  process.exit(0);
}

function emitError(command, code, message, exitCode, startTime, request) {
  writeJsonAndExit(
    buildEnvelope({
      status: "error",
      errorCode: code,
      message,
      request: request || { command },
      startTime,
    }),
    exitCode,
  );
}

function emitEmpty(message, startTime, request) {
  writeJsonAndExit(
    buildEnvelope({
      status: "empty",
      errorCode: "NO_MATCH",
      message,
      request,
      startTime,
    }),
    0,
  );
}

function emitUncaught(command, error) {
  writeJsonAndExit(
    buildEnvelope({
      status: "error",
      errorCode: error.code || "UNKNOWN",
      message: error.message || "未知错误",
      request: { command },
    }),
    error.name === "AuthError" ? 3 : 1,
  );
}

module.exports = {
  writeJson,
  writeJsonAndExit,
  buildSuccessEnvelope,
  finishSuccess,
  emitError,
  emitEmpty,
  emitUncaught,
};
