/**
 * AuditLogger — 轻量级安全事件审计日志
 *
 * 记录关键安全事件（环境变量访问、补丁应用、文件状态变更等），
 * 写入可配置的仅追加日志文件，支持自动轮转和大小限制。
 *
 * 使用方式：
 *   const audit = new AuditLogger(projectRoot);
 *   audit.log('env_access', { variable: 'HEARTFLOW_AES_KEY', source: 'startup' });
 *   audit.log('patch_apply', { target: 'src/core/foo.js', patchId: 'xxx' });
 *   audit.log('file_modify', { file: 'data/memory.json', action: 'write' });
 *   audit.close(); // 关闭写流
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const DEFAULT_MAX_SIZE = 10 * 1024 * 1024; // 10MB，超过自动轮转

class AuditLogger {
  /**
   * @param {string} rootPath - 项目根目录
   * @param {string} [logDir] - 日志目录（默认 data/）
   * @param {number} [maxSize] - 单文件最大字节（默认 10MB）
   */
  constructor(rootPath, logDir, maxSize) {
    this.rootPath = rootPath;
    this.logDir = logDir || path.join(rootPath, 'data');
    this.maxSize = maxSize || DEFAULT_MAX_SIZE;
    this._logPath = path.join(this.logDir, 'audit.log');
    this._stream = null;
    this._closed = false;
    this._init();
  }

  /** 初始化：确保日志目录存在，打开写流 */
  _init() {
    try {
      if (!fs.existsSync(this.logDir)) {
        fs.mkdirSync(this.logDir, { recursive: true, mode: 0o755 });
      }
      // 文件过大时自动轮转
      if (fs.existsSync(this._logPath)) {
        const stat = fs.statSync(this._logPath);
        if (stat.size >= this.maxSize) {
          this._rotate();
        }
      }
      // 以追加模式打开（日志文件仅追加，不可修改历史）
      this._stream = fs.createWriteStream(this._logPath, {
        flags: 'a',
        mode: 0o600,
      });
    } catch (e) {
      console.warn(`[AuditLogger] 初始化失败: ${e.message}`);
    }
  }

  /** 自动轮转：重命名当前文件 */
  _rotate() {
    try {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const rotatedPath = `${this._logPath  }.${  timestamp}`;
      fs.renameSync(this._logPath, rotatedPath);
    } catch (e) {
      console.warn(`[AuditLogger] 轮转失败: ${e.message}`);
    }
  }

  /**
   * 记录一条安全事件
   * @param {string} eventType - 事件类型（如 env_access, patch_apply, file_modify）
   * @param {Object} details - 事件详情（不含敏感值）
   */
  log(eventType, details = {}) {
    if (!this._stream || this._closed) return;
    const entry = {
      t: Date.now(),
      e: eventType,
      d: details,
      h: this._hash(eventType + JSON.stringify(details) + Date.now()),
    };
    this._stream.write(`${JSON.stringify(entry)  }\n`);
  }

  /**
   * 关闭写流（程序退出前调用确保数据落盘）
   */
  close() {
    this._closed = true;
    if (this._stream) {
      this._stream.end();
      this._stream = null;
    }
  }

  /**
   * 读取近期事件（用于排查）
   * @param {number} [limit=50] - 读取条数
   * @returns {Array} 事件数组（从新到旧）
   */
  readRecent(limit = 50) {
    try {
      if (!fs.existsSync(this._logPath)) return [];
      const data = fs.readFileSync(this._logPath, 'utf8');
      const lines = data.trim().split('\n').filter(Boolean);
      return lines.slice(-limit).reverse().map(line => {
        try { return JSON.parse(line); } catch { return { raw: line }; }
      });
    } catch {
      return [];
    }
  }

  /** 获取日志统计 */
  getStats() {
    try {
      if (!fs.existsSync(this._logPath)) return { total: 0 };
      const data = fs.readFileSync(this._logPath, 'utf8');
      const lines = data.trim().split('\n').filter(Boolean);
      const types = {};
      lines.forEach(line => {
        try {
          const entry = JSON.parse(line);
          types[entry.e] = (types[entry.e] || 0) + 1;
        } catch { /* 忽略格式错误的旧条目 */ }
      });
      return { total: lines.length, types };
    } catch {
      return { total: 0, error: '读取失败' };
    }
  }

  /** 生成短哈希用于追踪 */
  _hash(str) {
    return crypto.createHash('sha256').update(str).digest('hex').slice(0, 12);
  }
}

module.exports = { AuditLogger };
