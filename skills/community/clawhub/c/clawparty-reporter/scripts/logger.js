/**
 * 日志工具模块
 * 提供结构化的日志输出，确保 api_key 不会泄露
 */

const LOG_PREFIX = '[clawparty-reporter]';

function sanitizeMessage(message) {
  if (typeof message !== 'string') return message;

  // 移除可能的 API key
  return message
    .replace(/claw_[a-zA-Z0-9_]+/g, '***')
    .replace(/Bearer\s+[a-zA-Z0-9_]+/g, 'Bearer ***');
}

function info(message, ...args) {
  console.log(LOG_PREFIX, sanitizeMessage(message), ...args.map(sanitizeMessage));
}

function warn(message, ...args) {
  console.warn(LOG_PREFIX, 'WARN:', sanitizeMessage(message), ...args.map(sanitizeMessage));
}

function error(message, ...args) {
  console.error(LOG_PREFIX, 'ERROR:', sanitizeMessage(message), ...args.map(sanitizeMessage));
}

function debug(message, ...args) {
  if (process.env.CLAWPARTY_REPORTER_DEBUG) {
    console.log(LOG_PREFIX, 'DEBUG:', sanitizeMessage(message), ...args.map(sanitizeMessage));
  }
}

module.exports = {
  info,
  warn,
  error,
  debug
};
