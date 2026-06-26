/**
 * 统一日志模块 (Legacy)
 * 提供结构化的日志输出 - 使用 Winston 替代
 * @deprecated 请使用 src/utils/logger.cjs
 */

const LOG_LEVELS = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3
};

let currentLevel = LOG_LEVELS.INFO;
let enableTimestamp = true;
let enableColors = true;

const colors = {
  reset: '\x1b[0m',
  debug: '\x1b[36m',    // cyan
  info: '\x1b[32m',     // green
  warn: '\x1b[33m',     // yellow
  error: '\x1b[31m',    // red
  gray: '\x1b[90m'      // gray
};

function formatMessage(level, module, message, meta = {}) {
  const parts = [];
  
  // Timestamp
  if (enableTimestamp) {
    const now = new Date().toISOString();
    parts.push(enableColors ? `${colors.gray}[${now}]${colors.reset}` : `[${now}]`);
  }
  
  // Level
  const levelColor = colors[level.toLowerCase()] || colors.reset;
  parts.push(enableColors ? `${levelColor}[${level.padEnd(5)}]${colors.reset}` : `[${level.padEnd(5)}]`);
  
  // Module
  parts.push(`[${module}]`);
  
  // Message
  parts.push(message);
  
  // Meta
  if (Object.keys(meta).length > 0) {
    parts.push(JSON.stringify(meta));
  }
  
  return parts.join(' ');
}

function log(level, module, message, meta) {
  if (LOG_LEVELS[level] >= currentLevel) {
    console.log(formatMessage(level, module, message, meta));
  }
}

const logger = {
  // Configuration
  setLevel(level) {
    currentLevel = LOG_LEVELS[level.toUpperCase()] || LOG_LEVELS.INFO;
  },
  
  setTimestamp(enable) {
    enableTimestamp = enable;
  },
  
  setColors(enable) {
    enableColors = enable;
  },
  
  // Log methods
  debug(module, message, meta) {
    log('DEBUG', module, message, meta);
  },
  
  info(module, message, meta) {
    log('INFO', module, message, meta);
  },
  
  warn(module, message, meta) {
    log('WARN', module, message, meta);
  },
  
  error(module, message, meta) {
    log('ERROR', module, message, meta);
  },
  
  // Performance logging
  perf(module, operation, durationMs, success = true) {
    this.info(module, `${operation} completed`, {
      duration: durationMs,
      success,
      timestamp: Date.now()
    });
  }
};

module.exports = logger;
