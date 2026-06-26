#!/usr/bin/env node
/**
 * 性能调优配置 v1.0
 * 
 * 根据不同场景提供预设配置
 */

const path = require('path');

// ============ 预设配置模板 ============

const CONFIG_PRESETS = {
  // 开发环境（低配置）
  development: {
    engine: {
      checkInterval: 30000,       // 30 秒检查
      maxConcurrentTasks: 2,      // 最大并发 2
      autoLearn: true
    },
    cache: {
      maxSize: 50 * 1024 * 1024,  // 50MB
      ttl: 3600,                  // 1 小时
      maxMemoryCacheSize: 50
    },
    memory: {
      maxShortMemorySize: 50,
      maxLongMemorySessions: 100
    },
    gateway: {
      rateLimitMax: 50,           // 每分钟 50 次
      dailyTokenBudget: 500000,   // 50 万 tokens
      failureThreshold: 10
    },
    monitoring: {
      tokenWarningThreshold: 80,
      tokenCriticalThreshold: 95,
      cacheWarningThreshold: 20
    }
  },

  // 生产环境（标准配置）
  production: {
    engine: {
      checkInterval: 10000,       // 10 秒检查
      maxConcurrentTasks: 5,      // 最大并发 5
      autoLearn: true
    },
    cache: {
      maxSize: 500 * 1024 * 1024, // 500MB
      ttl: 7200,                  // 2 小时
      maxMemoryCacheSize: 200
    },
    memory: {
      maxShortMemorySize: 200,
      maxLongMemorySessions: 500
    },
    gateway: {
      rateLimitMax: 200,          // 每分钟 200 次
      dailyTokenBudget: 2000000,  // 200 万 tokens
      failureThreshold: 5
    },
    monitoring: {
      tokenWarningThreshold: 70,
      tokenCriticalThreshold: 90,
      cacheWarningThreshold: 30
    }
  },

  // 高性能环境（大配置）
  highPerformance: {
    engine: {
      checkInterval: 5000,        // 5 秒检查
      maxConcurrentTasks: 10,     // 最大并发 10
      autoLearn: true
    },
    cache: {
      maxSize: 1024 * 1024 * 1024, // 1GB
      ttl: 14400,                  // 4 小时
      maxMemoryCacheSize: 500
    },
    memory: {
      maxShortMemorySize: 500,
      maxLongMemorySessions: 1000
    },
    gateway: {
      rateLimitMax: 500,           // 每分钟 500 次
      dailyTokenBudget: 10000000,  // 1000 万 tokens
      failureThreshold: 3
    },
    monitoring: {
      tokenWarningThreshold: 60,
      tokenCriticalThreshold: 85,
      cacheWarningThreshold: 40
    }
  },

  // 小说创作专用（优化 Token 消耗）
  novelCreation: {
    engine: {
      checkInterval: 15000,       // 15 秒检查
      maxConcurrentTasks: 3,      // 最大并发 3
      autoLearn: true
    },
    cache: {
      maxSize: 200 * 1024 * 1024, // 200MB
      ttl: 86400,                 // 24 小时（长缓存）
      maxMemoryCacheSize: 100
    },
    memory: {
      maxShortMemorySize: 100,
      maxLongMemorySessions: 200
    },
    gateway: {
      rateLimitMax: 100,
      dailyTokenBudget: 1000000,  // 100 万 tokens
      failureThreshold: 5
    },
    // 小说创作特有的上下文优化
    contextRouter: {
      maxStringLength: 5000,      // 更激进的压缩
      maxArrayLength: 20,
      maxDepth: 3
    },
    monitoring: {
      tokenWarningThreshold: 70,
      tokenCriticalThreshold: 90,
      cacheWarningThreshold: 25
    }
  }
};

// ============ 配置管理类 ============

class PerformanceTuner {
  constructor() {
    this.currentPreset = 'production';
    this.customConfig = {};
  }

  /**
   * 加载预设配置
   */
  loadPreset(presetName) {
    if (!CONFIG_PRESETS[presetName]) {
      console.error(`❌ 未知预设: ${presetName}`);
      console.log('可用预设:', Object.keys(CONFIG_PRESETS).join(', '));
      return null;
    }
    
    this.currentPreset = presetName;
    console.log(`✅ 加载预设配置: ${presetName}`);
    return CONFIG_PRESETS[presetName];
  }

  /**
   * 获取当前配置
   */
  getCurrentConfig() {
    return {
      preset: this.currentPreset,
      ...CONFIG_PRESETS[this.currentPreset],
      ...this.customConfig
    };
  }

  /**
   * 自定义配置
   */
  setCustomConfig(key, value) {
    const keys = key.split('.');
    let target = this.customConfig;
    
    for (let i = 0; i < keys.length - 1; i++) {
      if (!target[keys[i]]) {
        target[keys[i]] = {};
      }
      target = target[keys[i]];
    }
    
    target[keys[keys.length - 1]] = value;
    console.log(`✅ 设置自定义配置: ${key} = ${JSON.stringify(value)}`);
  }

  /**
   * 根据系统资源自动推荐配置
   */
  autoRecommend() {
    const os = require('os');
    const totalMemory = os.totalmem() / (1024 * 1024 * 1024); // GB
    const cpuCount = os.cpus().length;
    
    console.log('\n📊 系统资源检测:');
    console.log(`   内存: ${totalMemory.toFixed(1)} GB`);
    console.log(`   CPU: ${cpuCount} 核`);
    
    let recommended = 'development';
    
    if (totalMemory >= 16 && cpuCount >= 8) {
      recommended = 'highPerformance';
    } else if (totalMemory >= 8 && cpuCount >= 4) {
      recommended = 'production';
    } else if (totalMemory >= 4) {
      recommended = 'novelCreation'; // 中等配置，Token 优化
    }
    
    console.log(`\n✅ 推荐配置: ${recommended}`);
    return recommended;
  }

  /**
   * 生成配置文件
   */
  generateConfigFile(outputPath) {
    const config = this.getCurrentConfig();
    const content = `// 自动生成的性能配置
// 预设: ${this.currentPreset}
// 生成时间: ${new Date().toISOString()}

module.exports = ${JSON.stringify(config, null, 2)};
`;
    
    const fs = require('fs');
    fs.writeFileSync(outputPath, content);
    console.log(`✅ 配置文件已生成: ${outputPath}`);
  }

  /**
   * 打印所有预设
   */
  listPresets() {
    console.log('\n📋 可用预设配置:\n');
    
    for (const [name, config] of Object.entries(CONFIG_PRESETS)) {
      console.log(`【${name}】`);
      console.log(`  引擎检查间隔: ${config.engine.checkInterval}ms`);
      console.log(`  最大并发任务: ${config.engine.maxConcurrentTasks}`);
      console.log(`  缓存大小: ${config.cache.maxSize / 1024 / 1024}MB`);
      console.log(`  每日 Token 预算: ${config.gateway.dailyTokenBudget}`);
      console.log('');
    }
  }
}

// CLI 入口
if (require.main === module) {
  const tuner = new PerformanceTuner();
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(`
性能调优配置工具

用法:
  node performance-tuner.js list          # 列出所有预设
  node performance-tuner.js recommend     # 自动推荐
  node performance-tuner.js load <预设>   # 加载预设
  node performance-tuner.js current       # 显示当前配置
`);
    process.exit(0);
  }
  
  const command = args[0];
  
  switch (command) {
    case 'list':
      tuner.listPresets();
      break;
      
    case 'recommend':
      tuner.autoRecommend();
      break;
      
    case 'load':
      const preset = args[1];
      if (preset) {
        tuner.loadPreset(preset);
        console.log('\n当前配置:');
        console.log(JSON.stringify(tuner.getCurrentConfig(), null, 2));
      } else {
        console.log('❌ 请指定预设名称');
      }
      break;
      
    case 'current':
      console.log('\n当前配置:');
      console.log(JSON.stringify(tuner.getCurrentConfig(), null, 2));
      break;
      
    default:
      console.log(`❌ 未知命令: ${command}`);
  }
}

module.exports = {
  PerformanceTuner,
  CONFIG_PRESETS
};