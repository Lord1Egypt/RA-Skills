/**
 * 配置加载模块
 * 从.env 文件加载配置
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 解析.env 文件
function parseEnvFile(filePath) {
  try {
    const content = readFileSync(filePath, 'utf-8');
    const config = {};
    
    content.split('\n').forEach(line => {
      const trimmedLine = line.trim();
      // 跳过注释和空行
      if (!trimmedLine || trimmedLine.startsWith('#')) {
        return;
      }
      
      const [key, ...valueParts] = trimmedLine.split('=');
      if (key && valueParts.length > 0) {
        config[key.trim()] = valueParts.join('=').trim();
      }
    });
    
    return config;
  } catch (error) {
    console.warn(`⚠️  无法读取配置文件：${filePath}`, error.message);
    return {};
  }
}

// 加载配置
const envConfig = parseEnvFile(join(__dirname, '..', '.env'));

// 默认配置
const defaultConfig = {
  database: {
    path: './clawmem.db',
    walMode: true
  },
  
  retrieval: {
    l0MaxSummaryLength: 100,
    l1MaxSummaryLength: 500,
    l2StoreHighValueOnly: true,
    tokenEstimateRatio: 4,
    maxRetrieveLimit: 100
  },
  
  lifecycle: {
    events: ['session.start', 'session.end', 'tool.call', 'memory.read', 'memory.write'],
    workerIntervalMs: 1000
  },
  
  llm: {
    provider: 'openai',
    model: 'gpt-3.5-turbo',
    maxTokens: 500
  },
  
  logging: {
    level: 'info',
    file: './logs/clawmem.log'
  },
  
  cache: {
    enabled: true,
    ttlMs: 300000 // 5 分钟
  }
};

// 合并配置
export const config = {
  database: {
    ...defaultConfig.database,
    path: envConfig.DATABASE_PATH || defaultConfig.database.path,
    walMode: envConfig.DATABASE_WAL_MODE !== 'false'
  },
  
  retrieval: {
    ...defaultConfig.retrieval,
    l0MaxSummaryLength: parseInt(envConfig.L0_MAX_SUMMARY_LENGTH) || defaultConfig.retrieval.l0MaxSummaryLength,
    l1MaxSummaryLength: parseInt(envConfig.L1_MAX_SUMMARY_LENGTH) || defaultConfig.retrieval.l1MaxSummaryLength,
    l2StoreHighValueOnly: envConfig.L2_STORE_HIGH_VALUE_ONLY !== 'false',
    tokenEstimateRatio: parseInt(envConfig.TOKEN_ESTIMATE_RATIO) || defaultConfig.retrieval.tokenEstimateRatio,
    maxRetrieveLimit: parseInt(envConfig.MAX_RETRIEVE_LIMIT) || defaultConfig.retrieval.maxRetrieveLimit
  },
  
  lifecycle: {
    ...defaultConfig.lifecycle,
    events: envConfig.LIFECYCLE_EVENTS 
      ? envConfig.LIFECYCLE_EVENTS.split(',') 
      : defaultConfig.lifecycle.events,
    workerIntervalMs: parseInt(envConfig.WORKER_INTERVAL_MS) || defaultConfig.lifecycle.workerIntervalMs
  },
  
  llm: {
    ...defaultConfig.llm,
    provider: envConfig.LLM_PROVIDER || defaultConfig.llm.provider,
    model: envConfig.LLM_MODEL || defaultConfig.llm.model,
    maxTokens: parseInt(envConfig.LLM_MAX_TOKENS) || defaultConfig.llm.maxTokens
  },
  
  logging: {
    ...defaultConfig.logging,
    level: envConfig.LOG_LEVEL || defaultConfig.logging.level,
    file: envConfig.LOG_FILE || defaultConfig.logging.file
  },
  
  cache: {
    ...defaultConfig.cache,
    enabled: envConfig.CACHE_ENABLED !== 'false',
    ttlMs: parseInt(envConfig.CACHE_TTL_MS) || defaultConfig.cache.ttlMs
  }
};

// 导出辅助函数
export function getConfig(key, defaultValue = undefined) {
  const keys = key.split('.');
  let value = config;
  
  for (const k of keys) {
    if (value && typeof value === 'object' && k in value) {
      value = value[k];
    } else {
      return defaultValue;
    }
  }
  
  return value;
}

export default config;
