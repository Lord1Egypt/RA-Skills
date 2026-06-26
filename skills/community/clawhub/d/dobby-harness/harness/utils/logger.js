/**
 * Logger - 日志工具
 * 
 * 提供分级日志、结构化输出、日志持久化
 */

import { writeFileSync, appendFileSync, mkdirSync, existsSync } from 'fs';
import { dirname } from 'path';

const LogLevel = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3,
  NONE: 4,
};

export class Logger {
  constructor(options = {}) {
    this.prefix = options.prefix || '[Harness]';
    this.level = LogLevel[options.level?.toUpperCase()] ?? LogLevel.INFO;
    this.logFile = options.logFile;
    this.enableColors = options.enableColors ?? true;
    this.includeTimestamp = options.includeTimestamp ?? true;

    // 确保日志目录存在
    if (this.logFile) {
      const dir = dirname(this.logFile);
      if (!existsSync(dir)) {
        mkdirSync(dir, { recursive: true });
      }
    }
  }

  /**
   * 设置日志级别
   */
  setLevel(level) {
    this.level = LogLevel[level?.toUpperCase()] ?? LogLevel.INFO;
  }

  /**
   * 格式化日志消息
   */
  format(level, levelName, ...args) {
    if (this.level > level) return null;

    const timestamp = this.includeTimestamp 
      ? new Date().toISOString() 
      : '';
    
    const message = args.map(arg => 
      typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
    ).join(' ');

    const colored = this.enableColors ? this.colorize(levelName, message) : message;
    const prefix = `${this.prefix} [${levelName}]`;

    return timestamp 
      ? `${timestamp} ${prefix} ${colored}`
      : `${prefix} ${colored}`;
  }

  /**
   * 终端颜色
   */
  colorize(level, message) {
    const colors = {
      DEBUG: '\x1b[36m',  // Cyan
      INFO: '\x1b[32m',   // Green
      WARN: '\x1b[33m',   // Yellow
      ERROR: '\x1b[31m',  // Red
    };
    const reset = '\x1b[0m';
    return `${colors[level] || ''}${message}${reset}`;
  }

  /**
   * 写入日志文件
   */
  writeToFile(formatted) {
    if (!this.logFile || !formatted) return;
    
    // 移除颜色代码
    const plain = formatted.replace(/\x1b\[[0-9;]*m/g, '');
    appendFileSync(this.logFile, plain + '\n');
  }

  /**
   * 输出日志
   */
  output(formatted, ...args) {
    if (!formatted) return;

    const consoleMethod = formatted.includes('[ERROR]') 
      ? 'error' 
      : formatted.includes('[WARN]') 
        ? 'warn' 
        : 'log';
    
    console[consoleMethod](formatted);
    this.writeToFile(formatted);
  }

  debug(...args) {
    const formatted = this.format(LogLevel.DEBUG, 'DEBUG', ...args);
    this.output(formatted, ...args);
  }

  info(...args) {
    const formatted = this.format(LogLevel.INFO, 'INFO', ...args);
    this.output(formatted, ...args);
  }

  warn(...args) {
    const formatted = this.format(LogLevel.WARN, 'WARN', ...args);
    this.output(formatted, ...args);
  }

  error(...args) {
    const formatted = this.format(LogLevel.ERROR, 'ERROR', ...args);
    this.output(formatted, ...args);
  }

  /**
   * 结构化日志
   */
  logStructured(event, data) {
    const entry = {
      timestamp: new Date().toISOString(),
      event,
      ...data,
    };
    
    const formatted = JSON.stringify(entry);
    if (this.logFile) {
      appendFileSync(this.logFile, formatted + '\n');
    }
    
    if (this.level <= LogLevel.INFO) {
      console.log(`${this.prefix} [EVENT] ${event}`, data);
    }
  }

  /**
   * 清除日志文件
   */
  clear() {
    if (this.logFile && existsSync(this.logFile)) {
      writeFileSync(this.logFile, '');
    }
  }
}

export default Logger;
