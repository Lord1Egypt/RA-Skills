/**
 * 日志系统
 * Winston 日志封装，带降级处理
 */

const path = require('path');
const fs = require('fs');

// 确保日志目录存在
const logDir = path.join(process.cwd(), 'logs');
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
}

// 简单日志实现（Winston 不可用时降级）
class SimpleLogger {
  constructor(name = 'app') {
    this.name = name;
    this.level = process.env.LOG_LEVEL || 'info';
    this.levels = { debug: 0, info: 1, warn: 2, error: 3 };
  }

  _log(level, message, meta = {}) {
    if (this.levels[level] >= this.levels[this.level]) {
      const timestamp = new Date().toISOString();
      const metaStr = Object.keys(meta).length ? JSON.stringify(meta) : '';
      const output = `${timestamp} [${level.toUpperCase()}]: ${message} ${metaStr}`;
      
      // 输出到控制台
      if (level === 'error') {
        console.error(output);
      } else if (level === 'warn') {
        console.warn(output);
      } else {
        console.log(output);
      }
      
      // 写入文件
      try {
        const logFile = level === 'error' ? 'error.log' : 'combined.log';
        fs.appendFileSync(path.join(logDir, logFile), output + '\n');
      } catch (e) {
        // 忽略文件写入错误
      }
    }
  }

  debug(message, meta) { this._log('debug', message, meta); }
  info(message, meta) { this._log('info', message, meta); }
  warn(message, meta) { this._log('warn', message, meta); }
  error(message, meta) { this._log('error', message, meta); }
}

// 尝试加载 Winston，失败时使用简单实现
let winston = null;
try {
  winston = require('winston');
} catch (e) {
  // Winston 未安装，使用降级实现
}

// 日志格式
function createWinstonLogger(name) {
  const logFormat = winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    winston.format.errors({ stack: true }),
    winston.format.json()
  );

  const consoleFormat = winston.format.combine(
    winston.format.colorize(),
    winston.format.timestamp({ format: 'HH:mm:ss' }),
    winston.format.printf(({ level, message, timestamp, ...meta }) => {
      const metaStr = Object.keys(meta).length ? JSON.stringify(meta) : '';
      return `${timestamp} [${level}]: ${message} ${metaStr}`;
    })
  );

  const logger = winston.createLogger({
    level: process.env.LOG_LEVEL || 'info',
    defaultMeta: { service: name },
    format: logFormat,
    transports: [
      new winston.transports.File({
        filename: path.join(logDir, 'error.log'),
        level: 'error',
        maxsize: 10485760,
        maxFiles: 5
      }),
      new winston.transports.File({
        filename: path.join(logDir, 'combined.log'),
        maxsize: 10485760,
        maxFiles: 5
      })
    ]
  });

  if (process.env.NODE_ENV !== 'production') {
    logger.add(new winston.transports.Console({
      format: consoleFormat
    }));
  }

  return logger;
}

// 创建日志实例
function createLogger(name = 'app') {
  if (winston) {
    return createWinstonLogger(name);
  }
  return new SimpleLogger(name);
}

// 默认日志实例
const logger = createLogger();

module.exports = { createLogger, logger, SimpleLogger };
