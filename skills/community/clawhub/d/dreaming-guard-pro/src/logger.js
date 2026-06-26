/**
 * Dreaming Guard Pro - Logger Module
 * 
 * 统一日志管理，支持多级别输出和自动轮转
 * 纯Node.js实现，零外部依赖
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 日志级别定义
const LOG_LEVELS = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3
};

// 默认配置
const DEFAULT_CONFIG = {
  level: 'info',
  file: path.join(os.homedir(), '.openclaw', 'logs', 'dreaming-guard.log'),
  maxSize: 5 * 1024 * 1024, // 5MB
  maxFiles: 5,
  console: true
};

/**
 * Logger类 - 日志管理器
 */
class Logger {
  constructor(options = {}) {
    this.config = { ...DEFAULT_CONFIG, ...options };
    this.level = LOG_LEVELS[this.config.level] ?? LOG_LEVELS.info;
    this.module = this.config.module || 'core';
    
    // 确保日志目录存在
    const logDir = path.dirname(this.config.file);
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
  }

  /**
   * 格式化日志消息
   * @param {string} level - 日志级别
   * @param {string} message - 日志消息
   * @param {object} data - 附加数据
   * @returns {string} 格式化后的日志行
   */
  _format(level, message, data = null) {
    const timestamp = new Date().toISOString().replace('T', ' ').slice(0, 19);
    let line = `[${timestamp}] [${level.toUpperCase()}] [${this.module}] ${message}`;
    if (data) {
      line += ` | ${JSON.stringify(data)}`;
    }
    return line;
  }

  /**
   * 写入日志文件
   * @param {string} line - 日志行
   */
  _writeFile(line) {
    try {
      // 检查文件大小，必要时轮转
      if (fs.existsSync(this.config.file)) {
        const stats = fs.statSync(this.config.file);
        if (stats.size >= this.config.maxSize) {
          this._rotate();
        }
      }
      fs.appendFileSync(this.config.file, line + '\n');
    } catch (err) {
      // 写文件失败，只输出到控制台
      console.error('[Logger] Failed to write log file:', err.message);
    }
  }

  /**
   * 轮转日志文件
   */
  _rotate() {
    const dir = path.dirname(this.config.file);
    const ext = path.extname(this.config.file);
    const base = path.basename(this.config.file, ext);

    // 删除最旧的日志文件
    const oldest = path.join(dir, `${base}.${this.config.maxFiles}${ext}`);
    if (fs.existsSync(oldest)) {
      fs.unlinkSync(oldest);
    }

    // 重命名现有日志文件
    for (let i = this.config.maxFiles - 1; i >= 1; i--) {
      const oldFile = path.join(dir, `${base}.${i}${ext}`);
      const newFile = path.join(dir, `${base}.${i + 1}${ext}`);
      if (fs.existsSync(oldFile)) {
        fs.renameSync(oldFile, newFile);
      }
    }

    // 当前日志重命名为 .1
    const current = this.config.file;
    const first = path.join(dir, `${base}.1${ext}`);
    if (fs.existsSync(current)) {
      fs.renameSync(current, first);
    }
  }

  /**
   * 输出日志
   * @param {string} level - 日志级别
   * @param {string} message - 日志消息
   * @param {object} data - 附加数据
   */
  _log(level, message, data) {
    const levelNum = LOG_LEVELS[level];
    if (levelNum === undefined || levelNum < this.level) {
      return;
    }

    const line = this._format(level, message, data);

    // 输出到控制台
    if (this.config.console) {
      const consoleMethod = level === 'error' ? 'error' : level === 'warn' ? 'warn' : 'log';
      console[consoleMethod](line);
    }

    // 输出到文件
    this._writeFile(line);
  }

  // 公开的日志方法
  debug(message, data) { this._log('debug', message, data); }
  info(message, data) { this._log('info', message, data); }
  warn(message, data) { this._log('warn', message, data); }
  error(message, data) { this._log('error', message, data); }

  /**
   * 创建子logger
   * @param {string} module - 模块名
   * @returns {Logger} 新的logger实例
   */
  child(module) {
    return new Logger({
      ...this.config,
      module: module,
      console: false // 子logger默认不输出到控制台，避免重复
    });
  }

  /**
   * 设置日志级别
   * @param {string} level - 日志级别 (debug/info/warn/error)
   */
  setLevel(level) {
    if (LOG_LEVELS[level] !== undefined) {
      this.level = LOG_LEVELS[level];
    }
  }
}

module.exports = Logger;