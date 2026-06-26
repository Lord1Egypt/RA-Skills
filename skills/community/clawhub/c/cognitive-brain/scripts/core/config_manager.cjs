/**
 * 配置管理器
 * 集中管理所有功能开关和运行时配置
 */

const fs = require('fs');
const path = require('path');
const logger = require('./logger.cjs');

const CONFIG_PATH = path.join(__dirname, '..', '..', 'config.json');

class ConfigManager {
  constructor() {
    this.config = null;
    this.lastLoadTime = 0;
    this.reloadInterval = 60000; // 60秒检查一次
    this.watchers = [];
    this.load();
  }

  /**
   * 加载配置
   */
  load() {
    try {
      if (!fs.existsSync(CONFIG_PATH)) {
        logger.error('ConfigManager', 'Config file not found', { path: CONFIG_PATH });
        return false;
      }
      
      const content = fs.readFileSync(CONFIG_PATH, 'utf8');
      this.config = JSON.parse(content);
      this.lastLoadTime = Date.now();
      
      logger.info('ConfigManager', 'Config loaded successfully', {
        version: this.config.version
      });
      
      return true;
    } catch (e) {
      logger.error('ConfigManager', 'Failed to load config', { error: e.message });
      return false;
    }
  }

  /**
   * 热重载配置
   */
  reload() {
    const now = Date.now();
    if (now - this.lastLoadTime < this.reloadInterval) {
      return false; // 太频繁，跳过
    }
    
    logger.debug('ConfigManager', 'Reloading config...');
    return this.load();
  }

  /**
   * 获取完整配置
   */
  getAll() {
    this.reload();
    return this.config;
  }

  /**
   * 获取指定路径的配置值
   */
  get(path, defaultValue = null) {
    this.reload();
    
    if (!this.config) return defaultValue;
    
    const keys = path.split('.');
    let value = this.config;
    
    for (const key of keys) {
      if (value && typeof value === 'object' && key in value) {
        value = value[key];
      } else {
        return defaultValue;
      }
    }
    
    return value;
  }

  /**
   * 功能开关检查
   */
  isEnabled(feature) {
    return this.get(`features.${feature}.enabled`, false);
  }

  /**
   * 获取功能配置
   */
  getFeatureConfig(feature) {
    return this.get(`features.${feature}`, {});
  }

  /**
   * 数据库配置
   */
  getDatabaseConfig() {
    return this.get('storage.primary', {});
  }

  /**
   * 缓存配置
   */
  getCacheConfig() {
    return this.get('storage.cache', {});
  }

  /**
   * 性能配置
   */
  getPerformanceConfig() {
    return this.get('performance', {});
  }

  /**
   * 记忆配置
   */
  getMemoryConfig() {
    return this.get('memory', {});
  }

  /**
   * 获取版本号
   */
  getVersion() {
    return this.get('version', 'unknown');
  }

  /**
   * 注册配置变更监听器
   */
  onChange(callback) {
    this.watchers.push(callback);
  }

  /**
   * 触发配置变更事件
   */
  notifyChange() {
    this.watchers.forEach(cb => {
      try {
        cb(this.config);
      } catch (e) {
        logger.error('ConfigManager', 'Watcher failed', { error: e.message });
      }
    });
  }

  /**
   * 验证配置完整性
   */
  validate() {
    const errors = [];
    const required = [
      'version',
      'storage.primary.host',
      'storage.primary.database',
      'memory.episodic',
      'forgetting.enabled'
    ];
    
    for (const path of required) {
      if (this.get(path) === null) {
        errors.push(`Missing required config: ${path}`);
      }
    }
    
    if (errors.length > 0) {
      logger.error('ConfigManager', 'Config validation failed', { errors });
      return false;
    }
    
    return true;
  }

  /**
   * 打印配置摘要
   */
  summary() {
    const summary = {
      version: this.getVersion(),
      database: this.get('storage.primary.type'),
      cache: this.get('storage.cache.type'),
      memoryLayers: Object.keys(this.get('memory', {})),
      features: {
        forgetting: this.get('forgetting.enabled'),
        autolearn: this.get('autolearn.enabled'),
        proactive: this.get('proactive.enabled'),
        safety: this.get('safety.enabled')
      }
    };
    
    logger.info('ConfigManager', 'Configuration summary', summary);
    return summary;
  }
}

// 单例实例
let instance = null;

function getConfigManager() {
  if (!instance) {
    instance = new ConfigManager();
  }
  return instance;
}

module.exports = { ConfigManager, getConfigManager };

// CLI 支持
if (require.main === module) {
  const cm = getConfigManager();
  
  const args = process.argv.slice(2);
  const command = args[0] || 'summary';
  
  switch (command) {
    case 'summary':
      cm.summary();
      break;
    case 'validate':
      const valid = cm.validate();
      console.log(valid ? '✅ Config valid' : '❌ Config invalid');
      process.exit(valid ? 0 : 1);
      break;
    case 'get':
      const path = args[1];
      if (path) {
        console.log(JSON.stringify(cm.get(path), null, 2));
      } else {
        console.log('Usage: node config_manager.cjs get <path>');
      }
      break;
    default:
      console.log('Usage: node config_manager.cjs [summary|validate|get <path>]');
  }
}

