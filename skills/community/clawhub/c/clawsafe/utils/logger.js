/**
 * clawSafe Logger / clawSafe 日志记录模块
 * Provides logging functionality for security events
 * 为安全事件提供日志记录功能
 */

const fs = require('fs');
const path = require('path');

class Logger {
  constructor(options = {}) {
    this.logDir = options.logDir || path.join(process.cwd(), 'logs');
    this.logFile = options.logFile || 'clawsafe.log';
    this.maxSize = options.maxSize || 10 * 1024 * 1024; // 10MB
    this.levels = {
      debug: 0,
      info: 1,
      warn: 2,
      error: 3
    };
    this.level = options.level || 'info';
    
    this._ensureLogDir();
  }

  _ensureLogDir() {
    if (!fs.existsSync(this.logDir)) {
      fs.mkdirSync(this.logDir, { recursive: true });
    }
  }

  _shouldLog(level) {
    return this.levels[level] >= this.levels[this.level];
  }

  _getFullPath() {
    return path.join(this.logDir, this.logFile);
  }

  _write(level, message, data = null) {
    if (!this._shouldLog(level)) return;

    const timestamp = new Date().toISOString();
    let logEntry = `[${timestamp}] [${level.toUpperCase()}] ${message}`;
    
    if (data) {
      logEntry += ` | ${JSON.stringify(data)}`;
    }

    // 控制台输出
    console.log(logEntry);

    // 文件输出
    try {
      const filePath = this._getFullPath();
      
      // 检查文件大小
      if (fs.existsSync(filePath)) {
        const stats = fs.statSync(filePath);
        if (stats.size > this.maxSize) {
          this._rotateLog();
        }
      }
      
      fs.appendFileSync(filePath, logEntry + '\n');
    } catch (e) {
      console.error('Logger write error:', e.message);
    }
  }

  _rotateLog() {
    const filePath = this._getFullPath();
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const archivePath = path.join(this.logDir, `clawsafe-${timestamp}.log`);
    
    try {
      fs.renameSync(filePath, archivePath);
    } catch (e) {
      // 忽略重命名错误
    }
  }

  debug(message, data) {
    this._write('debug', message, data);
  }

  info(message, data) {
    this._write('info', message, data);
  }

  warn(message, data) {
    this._write('warn', message, data);
  }

  error(message, data) {
    this._write('error', message, data);
  }

  /**
   * 记录检测结果
   */
  logDetection(input, result) {
    const data = {
      safe: result.safe,
      threatCount: result.threats?.length || 0,
      threats: result.threats?.map(t => ({ type: t.type, severity: t.severity })),
      confidence: result.confidence
    };
    this._write('info', 'Detection performed', data);
  }
}

// 导出默认实例
const logger = new Logger();

module.exports = Logger;
module.exports.default = logger;
