#!/usr/bin/env node
/**
 * 配置管理器 v6.0-Phase3
 * 
 * 核心功能:
 * 1. 配置集中管理 (YAML/JSON)
 * 2. 配置热加载 (运行时更新)
 * 3. 版本管理 (历史追溯)
 * 4. 回滚机制 (失败恢复)
 * 5. 变更审计 (日志记录)
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const chokidar = require('chokidar');

// ============ 配置 ============

const CONFIG = {
  configDir: path.join(__dirname, '../config'),
  versionsDir: path.join(__dirname, '../config/versions'),
  currentConfigFile: path.join(__dirname, '../config/current.yaml'),
  changelogFile: path.join(__dirname, '../config/changelog.md'),
  maxVersions: 50,  // 最多保留 50 个历史版本
  validateOnChange: true  // 变更时验证
};

// ============ 配置 Schema ============

const CONFIG_SCHEMA = {
  version: { type: 'string', required: true },
  environment: { 
    type: 'string', 
    required: true,
    enum: ['development', 'staging', 'production']
  },
  
  quality: {
    type: 'object',
    properties: {
      thresholds: {
        type: 'object',
        required: true,
        properties: {
          pass: { type: 'number', min: 0, max: 100, required: true },
          warning: { type: 'number', min: 0, max: 100, required: true },
          reject: { type: 'number', min: 0, max: 100, required: true }
        }
      },
      weights: {
        type: 'object',
        required: true,
        properties: {
          completeness: { type: 'number', min: 0, max: 1, required: true },
          consistency: { type: 'number', min: 0, max: 1, required: true },
          compliance: { type: 'number', min: 0, max: 1, required: true },
          creativity: { type: 'number', min: 0, max: 1, required: true }
        }
      }
    }
  },
  
  token: {
    type: 'object',
    properties: {
      models: {
        type: 'object',
        required: true,
        properties: {
          maxTokens: { type: 'number', min: 1000 },
          maxOutputTokens: { type: 'number', min: 100 },
          reservedTokens: { type: 'number', min: 0 }
        }
      }
    }
  },
  
  agent: {
    type: 'object',
    properties: {
      maxConcurrent: { type: 'number', min: 1, max: 20 },
      idleTimeout: { type: 'number', min: 60000 },
      sleepTimeout: { type: 'number', min: 30000 }
    }
  },
  
  circuit_breaker: {
    type: 'object',
    properties: {
      failureThreshold: { type: 'number', min: 1, max: 100 },
      resetTimeout: { type: 'number', min: 10000 },
      gradualRecovery: { type: 'boolean' }
    }
  },
  
  monitoring: {
    type: 'object',
    properties: {
      enabled: { type: 'boolean' },
      dashboard: { type: 'boolean' },
      updateInterval: { type: 'number', min: 100 }
    }
  }
};

// ============ 配置管理器类 ============

class ConfigManager {
  constructor(options = {}) {
    this.configPath = options.configPath || CONFIG.configDir;
    this.currentConfig = null;
    this.versionHistory = [];
    this.watchers = new Set();
    this.watcher = null;
    
    this.ensureDirs();
  }

  /**
   * 确保目录存在
   */
  ensureDirs() {
    if (!fs.existsSync(this.configPath)) {
      fs.mkdirSync(this.configPath, { recursive: true });
    }
    if (!fs.existsSync(CONFIG.versionsDir)) {
      fs.mkdirSync(CONFIG.versionsDir, { recursive: true });
    }
  }

  /**
   * 加载配置
   */
  async load() {
    console.log('📖 加载配置...');
    
    try {
      const config = await this.readConfig();
      const valid = this.validate(config);
      
      if (!valid.valid) {
        throw new Error(`配置验证失败：${valid.errors.join(', ')}`);
      }
      
      this.currentConfig = config;
      console.log('✅ 配置加载成功');
      console.log(`   版本：${config.version}`);
      console.log(`   环境：${config.environment}`);
      
      return config;
    } catch (error) {
      console.error('❌ 配置加载失败:', error.message);
      throw error;
    }
  }

  /**
   * 读取配置文件
   */
  async readConfig() {
    if (!fs.existsSync(CONFIG.currentConfigFile)) {
      // 如果当前配置不存在，创建默认配置
      const defaultConfig = this.getDefaultConfig();
      await this.writeConfig(defaultConfig);
      return defaultConfig;
    }
    
    const content = fs.readFileSync(CONFIG.currentConfigFile, 'utf-8');
    
    // 自动识别 YAML 或 JSON
    if (CONFIG.currentConfigFile.endsWith('.yaml') || CONFIG.currentConfigFile.endsWith('.yml')) {
      return yaml.load(content);
    } else if (CONFIG.currentConfigFile.endsWith('.json')) {
      return JSON.parse(content);
    } else {
      // 尝试 YAML
      try {
        return yaml.load(content);
      } catch {
        return JSON.parse(content);
      }
    }
  }

  /**
   * 写入配置文件
   */
  async writeConfig(config) {
    const content = yaml.dump(config, {
      indent: 2,
      lineWidth: -1,  // 不限制行宽
      noRefs: true    // 不使用引用
    });
    
    fs.writeFileSync(CONFIG.currentConfigFile, content, 'utf-8');
  }

  /**
   * 更新配置
   */
  async update(newConfig, reason = '') {
    console.log('🔄 更新配置...');
    
    // 验证新配置
    if (CONFIG.validateOnChange) {
      const valid = this.validate(newConfig);
      if (!valid.valid) {
        throw new Error(`配置验证失败：${valid.errors.join(', ')}`);
      }
    }
    
    // 保存当前版本
    const oldConfig = this.currentConfig;
    await this.saveVersion(oldConfig);
    
    // 应用新配置
    this.currentConfig = newConfig;
    await this.writeConfig(newConfig);
    
    // 通知所有监听者
    this.notify(newConfig, oldConfig);
    
    // 记录变更日志
    await this.logChange(oldConfig, newConfig, reason);
    
    console.log('✅ 配置更新成功');
    console.log(`   原因：${reason || '无'}`);
    
    return true;
  }

  /**
   * 获取配置项
   */
  get(key, defaultValue = undefined) {
    const keys = key.split('.');
    let value = this.currentConfig;
    
    for (const k of keys) {
      if (value === undefined || value === null) {
        return defaultValue;
      }
      value = value[k];
    }
    
    return value !== undefined ? value : defaultValue;
  }

  /**
   * 设置配置项
   */
  async set(key, value, reason = '') {
    const keys = key.split('.');
    const newConfig = JSON.parse(JSON.stringify(this.currentConfig));
    
    let obj = newConfig;
    for (let i = 0; i < keys.length - 1; i++) {
      if (!obj[keys[i]]) {
        obj[keys[i]] = {};
      }
      obj = obj[keys[i]];
    }
    
    obj[keys[keys.length - 1]] = value;
    
    return await this.update(newConfig, reason);
  }

  /**
   * 保存版本
   */
  async saveVersion(config) {
    if (!config) return;
    
    const version = config.version || 'unknown';
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const versionFile = path.join(CONFIG.versionsDir, `v${version}-${timestamp}.yaml`);
    
    const content = yaml.dump(config, { indent: 2 });
    fs.writeFileSync(versionFile, content, 'utf-8');
    
    // 清理旧版本（保留最近的 maxVersions 个）
    this.cleanupVersions();
    
    console.log(`💾 版本已保存：v${version}`);
  }

  /**
   * 获取历史版本
   */
  async getVersion(version) {
    const files = fs.readdirSync(CONFIG.versionsDir);
    const versionFile = files.find(f => f.startsWith(`v${version}-`));
    
    if (!versionFile) {
      return null;
    }
    
    const content = fs.readFileSync(path.join(CONFIG.versionsDir, versionFile), 'utf-8');
    return yaml.load(content);
  }

  /**
   * 回滚配置
   */
  async rollback(version, reason = '') {
    console.log(`↩️ 回滚配置到版本 ${version}...`);
    
    const config = await this.getVersion(version);
    if (!config) {
      throw new Error(`版本 ${version} 不存在`);
    }
    
    return await this.update(config, reason || `回滚到版本 ${version}`);
  }

  /**
   * 获取版本历史
   */
  getVersionHistory() {
    const files = fs.readdirSync(CONFIG.versionsDir)
      .filter(f => f.endsWith('.yaml'))
      .sort()
      .reverse();
    
    return files.map(f => {
      const match = f.match(/v(.+?)-(.+)\.yaml/);
      if (match) {
        return {
          version: match[1],
          timestamp: match[2],
          file: f
        };
      }
      return null;
    }).filter(v => v !== null);
  }

  /**
   * 对比版本
   */
  diffVersions(version1, version2) {
    const config1 = await this.getVersion(version1);
    const config2 = await this.getVersion(version2);
    
    if (!config1 || !config2) {
      throw new Error('版本不存在');
    }
    
    return this.diffObjects(config1, config2);
  }

  /**
   * 对比对象
   */
  diffObjects(obj1, obj2, prefix = '') {
    const diffs = [];
    
    const allKeys = new Set([...Object.keys(obj1), ...Object.keys(obj2)]);
    
    for (const key of allKeys) {
      const key1 = obj1[key];
      const key2 = obj2[key];
      const fullKey = prefix ? `${prefix}.${key}` : key;
      
      if (key1 === undefined) {
        diffs.push({ key: fullKey, type: 'added', old: undefined, new: key2 });
      } else if (key2 === undefined) {
        diffs.push({ key: fullKey, type: 'removed', old: key1, new: undefined });
      } else if (typeof key1 === 'object' && typeof key2 === 'object') {
        diffs.push(...this.diffObjects(key1, key2, fullKey));
      } else if (key1 !== key2) {
        diffs.push({ key: fullKey, type: 'changed', old: key1, new: key2 });
      }
    }
    
    return diffs;
  }

  /**
   * 监听配置变化
   */
  watch(callback) {
    this.watchers.add(callback);
    
    // 启动文件监听
    if (!this.watcher) {
      this.startFileWatch();
    }
    
    return () => {
      this.watchers.delete(callback);
      if (this.watchers.size === 0 && this.watcher) {
        this.watcher.close();
        this.watcher = null;
      }
    };
  }

  /**
   * 启动文件监听
   */
  startFileWatch() {
    console.log('👁️ 启动配置监听...');
    
    this.watcher = chokidar.watch(CONFIG.currentConfigFile, {
      persistent: true,
      ignoreInitial: true
    });
    
    this.watcher.on('change', async () => {
      console.log('📝 配置文件变化，重新加载...');
      try {
        const config = await this.readConfig();
        const valid = this.validate(config);
        
        if (valid.valid) {
          const oldConfig = this.currentConfig;
          this.currentConfig = config;
          this.notify(config, oldConfig);
          console.log('✅ 配置已热加载');
        } else {
          console.error('❌ 配置验证失败，忽略变更');
        }
      } catch (error) {
        console.error('❌ 配置加载失败:', error.message);
      }
    });
  }

  /**
   * 通知配置变化
   */
  notify(newConfig, oldConfig) {
    this.watchers.forEach(callback => {
      try {
        callback(newConfig, oldConfig);
      } catch (error) {
        console.error('配置通知失败:', error.message);
      }
    });
  }

  /**
   * 验证配置
   */
  validate(config) {
    const errors = [];
    
    // 验证必填字段
    if (!config.version) {
      errors.push('缺少必填字段：version');
    }
    if (!config.environment) {
      errors.push('缺少必填字段：environment');
    }
    
    // 验证 environment 枚举
    if (config.environment && !['development', 'staging', 'production'].includes(config.environment)) {
      errors.push('environment 必须是 development/staging/production 之一');
    }
    
    // 验证 quality 配置
    if (config.quality) {
      if (config.quality.thresholds) {
        const { pass, warning, reject } = config.quality.thresholds;
        if (pass < reject) {
          errors.push('quality.thresholds.pass 必须大于 quality.thresholds.reject');
        }
      }
      
      if (config.quality.weights) {
        const { completeness, consistency, compliance, creativity } = config.quality.weights;
        const sum = completeness + consistency + compliance + creativity;
        if (Math.abs(sum - 1.0) > 0.01) {
          errors.push(`quality.weights 总和必须为 1，当前为 ${sum}`);
        }
      }
    }
    
    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * 记录变更日志
   */
  async logChange(oldConfig, newConfig, reason) {
    const timestamp = new Date().toISOString();
    const diffs = this.diffObjects(oldConfig, newConfig);
    
    const logEntry = `
## ${timestamp}

**原因**: ${reason || '无'}

**变更**:
${diffs.map(d => `- ${d.key}: ${d.old} → ${d.new} (${d.type})`).join('\n')}

---
`;
    
    fs.appendFileSync(CONFIG.changelogFile, logEntry, 'utf-8');
  }

  /**
   * 清理旧版本
   */
  cleanupVersions() {
    const files = this.getVersionHistory();
    
    if (files.length > CONFIG.maxVersions) {
      const toDelete = files.slice(CONFIG.maxVersions);
      for (const file of toDelete) {
        fs.unlinkSync(path.join(CONFIG.versionsDir, file.file));
      }
      console.log(`🧹 已清理 ${toDelete.length} 个旧版本`);
    }
  }

  /**
   * 获取默认配置
   */
  getDefaultConfig() {
    return {
      version: '6.0.0',
      environment: 'production',
      
      quality: {
        thresholds: {
          pass: 80,
          warning: 70,
          reject: 60
        },
        weights: {
          completeness: 0.3,
          consistency: 0.3,
          compliance: 0.2,
          creativity: 0.2
        }
      },
      
      token: {
        models: {
          qwen3.5-plus: {
            maxTokens: 32000,
            maxOutputTokens: 8000,
            reservedTokens: 2000
          }
        }
      },
      
      agent: {
        maxConcurrent: 5,
        idleTimeout: 3600000,
        sleepTimeout: 1800000
      },
      
      circuit_breaker: {
        failureThreshold: 5,
        resetTimeout: 300000,
        gradualRecovery: true
      },
      
      monitoring: {
        enabled: true,
        dashboard: true,
        updateInterval: 1000
      }
    };
  }

  /**
   * 导出配置
   */
  exportConfig() {
    return JSON.parse(JSON.stringify(this.currentConfig));
  }

  /**
   * 导入配置
   */
  async importConfig(config, reason = '导入配置') {
    return await this.update(config, reason);
  }
}

// ============ CLI 接口 ============

function printHelp() {
  console.log(`
配置管理器 v6.0-Phase3

用法：node config-manager.js <命令> [选项]

命令:
  load                加载配置
  get <key>           获取配置项
  set <key> <value>   设置配置项
  update <file>       从文件更新配置
  history             查看版本历史
  diff <v1> <v2>      对比版本
  rollback <version>  回滚配置
  validate            验证配置
  export              导出配置
  import <file>       导入配置
  watch               监听配置变化

示例:
  node config-manager.js get quality.thresholds.pass
  node config-manager.js set quality.thresholds.pass 85 "调整通过阈值"
  node config-manager.js history
  node config-manager.js rollback v6.0.0
`);
}

// ============ 主程序 ============

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help' || command === '-h') {
    printHelp();
    return;
  }

  const manager = new ConfigManager();

  try {
    switch (command) {
      case 'load':
        await manager.load();
        break;

      case 'get':
        await manager.load();
        const key = args[1];
        if (!key) {
          console.log('❌ 请指定配置键');
          return;
        }
        const value = manager.get(key);
        console.log(`${key} =`, JSON.stringify(value, null, 2));
        break;

      case 'set':
        await manager.load();
        const setKey = args[1];
        const setValue = args[2];
        const reason = args.slice(3).join(' ');
        if (!setKey || setValue === undefined) {
          console.log('❌ 请指定配置键和值');
          return;
        }
        await manager.set(setKey, JSON.parse(setValue), reason);
        break;

      case 'update':
        await manager.load();
        const file = args[1];
        if (!file) {
          console.log('❌ 请指定配置文件');
          return;
        }
        const newConfig = yaml.load(fs.readFileSync(file, 'utf-8'));
        await manager.update(newConfig, '从文件更新');
        break;

      case 'history':
        await manager.load();
        const history = manager.getVersionHistory();
        console.log('版本历史:');
        history.forEach((h, i) => {
          console.log(`  ${i + 1}. v${h.version} (${h.timestamp})`);
        });
        break;

      case 'rollback':
        await manager.load();
        const version = args[1];
        if (!version) {
          console.log('❌ 请指定版本号');
          return;
        }
        await manager.rollback(version);
        break;

      case 'validate':
        await manager.load();
        const valid = manager.validate(manager.currentConfig);
        if (valid.valid) {
          console.log('✅ 配置验证通过');
        } else {
          console.log('❌ 配置验证失败:');
          valid.errors.forEach(e => console.log(`   - ${e}`));
        }
        break;

      case 'export':
        await manager.load();
        console.log(yaml.dump(manager.exportConfig()));
        break;

      case 'import':
        await manager.load();
        const importFile = args[1];
        if (!importFile) {
          console.log('❌ 请指定配置文件');
          return;
        }
        const importConfig = yaml.load(fs.readFileSync(importFile, 'utf-8'));
        await manager.importConfig(importConfig);
        break;

      case 'watch':
        await manager.load();
        console.log('👁️ 监听配置变化... (Ctrl+C 停止)');
        manager.watch((newConfig, oldConfig) => {
          console.log('📝 配置已更新');
        });
        
        // 保持进程运行
        setInterval(() => {}, 1000);
        break;

      default:
        console.log(`未知命令：${command}`);
        printHelp();
    }
  } catch (error) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
}

// 导出 API
module.exports = { ConfigManager, CONFIG_SCHEMA, CONFIG };

// 运行 CLI
if (require.main === module) {
  main().catch(console.error);
}
