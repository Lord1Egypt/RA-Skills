/**
 * config.js — 配置加载模块
 *
 * 职责：加载并合并配置来源（优先级：环境变量 > config.json > DEFAULT_CONFIG）
 *
 * 配置来源：
 *   1. config.json          — 持久化配置
 *   2. 环境变量（DB_HOST 等） — 最高优先级
 *   3. DEFAULT_CONFIG      — 内置默认值
 */
const fs = require('fs');
const path = require('path');

// 配置文件路径（skill root）
const CONFIG_PATH = path.join(__dirname, '../../config.json');
const CONFIG_DIR = path.dirname(CONFIG_PATH);

// 默认配置
const DEFAULT_CONFIG = {
  db: {
    type: 'mysql',
    host: '192.168.3.25',
    port: 3306,
    database: 'acm_cloud_acm',
    user: 'root',
    password: 'Wisdom83248380',
    connectTimeout: 10000
  },
  oracle: {
    host: '192.168.3.25',
    port: 1521,
    serviceName: 'orcl',
    user: 'acm',
    password: 'acm'
  },
  api: {
    base: 'http://localhost:8765'
  },
  security: {
    apiAuth: {
      username: 'admin@wisdomidata',
      password: '123456'
    },
    verifyLimit: 3
  },
  workspace: '/Users/yuanlu/.openclaw/workspace'
};

// 加载配置文件
function loadConfigFile() {
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
    }
  } catch (e) {
    console.warn('配置文件读取失败，使用默认配置:', e.message);
  }
  return {};
}

// 从环境变量加载配置
function loadFromEnv() {
  return {
    db: {
      type: process.env.DB_TYPE,
      host: process.env.DB_HOST,
      port: process.env.DB_PORT ? parseInt(process.env.DB_PORT, 10) : undefined,
      database: process.env.DB_NAME,
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD
    },
    oracle: {
      host: process.env.ORACLE_HOST,
      port: process.env.ORACLE_PORT ? parseInt(process.env.ORACLE_PORT, 10) : undefined,
      serviceName: process.env.ORACLE_SERVICE,
      user: process.env.ORACLE_USER,
      password: process.env.ORACLE_PASSWORD
    },
    api: {
      base: process.env.API_BASE
    },
    workspace: process.env.WORKSPACE
  };
}

// 解析工作区路径
function resolveWorkspacePath(workspaceConfig) {
  // 优先使用环境变量
  if (process.env.WORKSPACE) {
    return path.resolve(process.env.WORKSPACE);
  }
  
  // 相对路径相对于 config.json 所在目录（skill root）解析
  return path.resolve(CONFIG_DIR, workspaceConfig);
}

// 合并配置
function mergeConfig() {
  const fileConfig = loadConfigFile();
  const envConfig = loadFromEnv();
  
  // 过滤掉 undefined 值
  const filterUndefined = (obj) => {
    const result = {};
    for (const key in obj) {
      if (obj[key] !== undefined) {
        result[key] = obj[key];
      }
    }
    return result;
  };
  
  const filteredEnvConfig = {
    db: filterUndefined(envConfig.db),
    oracle: filterUndefined(envConfig.oracle),
    api: filterUndefined(envConfig.api),
    workspace: envConfig.workspace
  };
  
  // 解析工作区路径
  const workspacePath = resolveWorkspacePath(filteredEnvConfig.workspace || fileConfig.workspace || DEFAULT_CONFIG.workspace);
  
  return {
    db: { ...DEFAULT_CONFIG.db, ...fileConfig.db, ...filteredEnvConfig.db },
    oracle: { ...DEFAULT_CONFIG.oracle, ...fileConfig.oracle, ...filteredEnvConfig.oracle },
    api: { ...DEFAULT_CONFIG.api, ...fileConfig.api, ...filteredEnvConfig.api },
    security: { ...DEFAULT_CONFIG.security, ...fileConfig.security },
    workspace: workspacePath
  };
}

const config = mergeConfig();
module.exports = config;