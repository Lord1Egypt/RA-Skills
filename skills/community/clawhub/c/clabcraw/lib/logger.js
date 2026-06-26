/**
 * Structured JSON logging for Clabcraw agent scripts.
 *
 * All output is valid JSON, one object per line — easy to parse
 * in agent pipelines or pipe to jq.
 */

const LOG_LEVELS = { debug: 0, info: 1, warn: 2, error: 3 };

let currentLevel = LOG_LEVELS.info;

/**
 * Set minimum log level. Messages below this level are suppressed.
 * @param {"debug"|"info"|"warn"|"error"} level
 */
export function setLogLevel(level) {
  currentLevel = LOG_LEVELS[level] ?? LOG_LEVELS.info;
}

function log(level, type, data = {}) {
  if (LOG_LEVELS[level] < currentLevel) return;

  const entry = {
    timestamp: new Date().toISOString(),
    level,
    type,
    ...data,
  };

  const out = level === "error" ? console.error : console.log;
  out(JSON.stringify(entry));
}

export const logger = {
  debug: (type, data) => log("debug", type, data),
  info: (type, data) => log("info", type, data),
  warn: (type, data) => log("warn", type, data),
  error: (type, data) => log("error", type, data),
};
