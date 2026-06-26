/**
 * Dreaming Guard Pro - Config Module
 * 
 * 配置管理，支持读取/验证/默认值
 * 支持文件配置和环境变量覆盖
 * 纯Node.js实现，零外部依赖
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 默认配置
const DEFAULT_CONFIG = {
  version: '1.0.0',
  workspaces: [
    {
      path: path.join(os.homedir(), '.openclaw', 'workspace'),
      enabled: true,
      thresholds: {
        warning: 524288,    // 512KB
        critical: 1048576,  // 1MB
        emergency: 2097152  // 2MB
      }
    }
  ],
  monitor: {
    interval: 5000,
    useFileWatcher: true
  },
  archive: {
    path: path.join(os.homedir(), '.openclaw', 'archive', 'dreaming'),
    retention: {
      keepRecent: 100,
      maxAge: 7,
      maxSize: 10485760
    },
    compression: 'gzip'
  },
  protection: {
    memoryThreshold: 512,
    actions: {
      warning: 'alert',
      critical: 'compress',
      emergency: 'restart'
    }
  },
  recovery: {
    enabled: true,
    maxAttempts: 3,
    recoveryPointInterval: 3600000
  },
  reporter: {
    interval: 86400000,
    output: path.join(os.homedir(), '.openclaw', 'logs', 'dreaming-health.log')
  }
};

// 环境变量映射
const ENV_MAPPING = {
  'DREAMING_GUARD_MONITOR_INTERVAL': 'monitor.interval',
  'DREAMING_GUARD_MEMORY_THRESHOLD': 'protection.memoryThreshold',
  'DREAMING_GUARD_ARCHIVE_PATH': 'archive.path',
  'DREAMING_GUARD_RECOVERY_ENABLED': 'recovery.enabled',
  'DREAMING_GUARD_THRESHOLD_WARNING': 'workspaces.0.thresholds.warning',
  'DREAMING_GUARD_THRESHOLD_CRITICAL': 'workspaces.0.thresholds.critical',
  'DREAMING_GUARD_THRESHOLD_EMERGENCY': 'workspaces.0.thresholds.emergency'
};

/**
 * Config类 - 配置管理器
 */
class Config {
  constructor(configPath = null) {
    this.configPath = configPath || path.join(os.homedir(), '.openclaw', 'dreaming-guard.json');
    this.config = JSON.parse(JSON.stringify(DEFAULT_CONFIG)); // 深拷贝默认配置
    this.loaded = false;
  }

  /**
   * 加载配置文件
   * @returns {Promise<object>} 配置对象
   */
  async load() {
    // 尝试读取配置文件
    if (fs.existsSync(this.configPath)) {
      try {
        const content = fs.readFileSync(this.configPath, 'utf-8');
        const userConfig = JSON.parse(content);
        this.config = this._merge(this.config, userConfig);
      } catch (err) {
        console.warn(`[Config] Failed to load config file: ${err.message}, using defaults`);
      }
    }

    // 应用环境变量覆盖
    this._applyEnvOverrides();

    this.loaded = true;
    return this.config;
  }

  /**
   * 同步加载配置（兼容性方法）
   * @returns {object} 配置对象
   */
  loadSync() {
    if (fs.existsSync(this.configPath)) {
      try {
        const content = fs.readFileSync(this.configPath, 'utf-8');
        const userConfig = JSON.parse(content);
        this.config = this._merge(this.config, userConfig);
      } catch (err) {
        console.warn(`[Config] Failed to load config file: ${err.message}`);
      }
    }
    this._applyEnvOverrides();
    this.loaded = true;
    return this.config;
  }

  /**
   * 深度合并配置
   * @param {object} target - 目标对象
   * @param {object} source - 源对象
   * @returns {object} 合并后的对象
   */
  _merge(target, source) {
    const result = { ...target };
    for (const key of Object.keys(source)) {
      if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
        result[key] = this._merge(target[key] || {}, source[key]);
      } else {
        result[key] = source[key];
      }
    }
    return result;
  }

  /**
   * 应用环境变量覆盖
   */
  _applyEnvOverrides() {
    for (const [envKey, configPath] of Object.entries(ENV_MAPPING)) {
      const envValue = process.env[envKey];
      if (envValue !== undefined) {
        this._setNestedValue(configPath, this._parseEnvValue(envValue));
      }
    }
  }

  /**
   * 解析环境变量值
   * @param {string} value - 环境变量值
   * @returns {*} 解析后的值
   */
  _parseEnvValue(value) {
    // 尝试解析数字
    const num = Number(value);
    if (!isNaN(num)) return num;
    // 尝试解析布尔值
    if (value.toLowerCase() === 'true') return true;
    if (value.toLowerCase() === 'false') return false;
    // 返回字符串
    return value;
  }

  /**
   * 设置嵌套配置值
   * @param {string} path - 配置路径 (如 'monitor.interval')
   * @param {*} value - 配置值
   */
  _setNestedValue(path, value) {
    const keys = path.split('.');
    let current = this.config;
    for (let i = 0; i < keys.length - 1; i++) {
      const key = keys[i];
      if (!current[key]) {
        current[key] = {};
      }
      current = current[key];
    }
    current[keys[keys.length - 1]] = value;
  }

  /**
   * 获取嵌套配置值
   * @param {string} path - 配置路径 (如 'monitor.interval')
   * @param {*} defaultValue - 默认值
   * @returns {*} 配置值
   */
  get(path, defaultValue = undefined) {
    const keys = path.split('.');
    let current = this.config;
    for (const key of keys) {
      if (current === undefined || current === null) {
        return defaultValue;
      }
      current = current[key];
    }
    return current !== undefined ? current : defaultValue;
  }

  /**
   * 设置配置值
   * @param {string} path - 配置路径
   * @param {*} value - 配置值
   */
  set(path, value) {
    this._setNestedValue(path, value);
  }

  /**
   * 验证配置
   * @returns {object} 验证结果 { valid: boolean, errors: string[] }
   */
  validate() {
    const errors = [];

    // 验证workspaces
    if (!Array.isArray(this.config.workspaces) || this.config.workspaces.length === 0) {
      errors.push('workspaces must be a non-empty array');
    } else {
      this.config.workspaces.forEach((ws, index) => {
        if (!ws.path) {
          errors.push(`workspaces[${index}].path is required`);
        }
        if (ws.thresholds) {
          if (ws.thresholds.warning <= 0) {
            errors.push(`workspaces[${index}].thresholds.warning must be positive`);
          }
          if (ws.thresholds.critical <= ws.thresholds.warning) {
            errors.push(`workspaces[${index}].thresholds.critical must be greater than warning`);
          }
        }
      });
    }

    // 验证monitor
    if (this.config.monitor?.interval && this.config.monitor.interval < 1000) {
      errors.push('monitor.interval must be at least 1000ms');
    }

    // 验证protection
    if (this.config.protection?.memoryThreshold && this.config.protection.memoryThreshold <= 0) {
      errors.push('protection.memoryThreshold must be positive');
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * 保存配置到文件
   * @returns {Promise<void>}
   */
  async save() {
    const dir = path.dirname(this.configPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(this.configPath, JSON.stringify(this.config, null, 2));
  }

  /**
   * 重置为默认配置
   */
  reset() {
    this.config = JSON.parse(JSON.stringify(DEFAULT_CONFIG));
  }
}

module.exports = Config;