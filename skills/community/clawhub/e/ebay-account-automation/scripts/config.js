/**
 * 配置文件
 * 优先级：config_local.js > 环境变量 > 默认值
 */

let localConfig = {};
try {
  localConfig = require('./config_local');
} catch (e) {
  // config_local.js 不存在，使用默认值
}

const config = {
  ADS_API_BASE: localConfig.ADS_API_BASE || process.env.ADS_API_BASE || 'http://local.adspower.net:50325',
  ADS_API_KEY: localConfig.ADS_API_KEY || process.env.ADS_API_KEY || '',
  ACCOUNT_RUNTIME_MS: localConfig.ACCOUNT_RUNTIME_MS || 30 * 60 * 1000,
  KEYWORDS_FILE: localConfig.KEYWORDS_FILE || 'keywords.txt',
  STATE_DIR: localConfig.STATE_DIR || 'state',
  CYCLE_STATE_FILE: localConfig.CYCLE_STATE_FILE || 'state/cycle_state.json',
  EBAY_BASE_URL: localConfig.EBAY_BASE_URL || 'https://www.ebay.com',
  MAX_RETRIES: 2,
  LOG_LEVEL: 'info',
};

if (!config.ADS_API_KEY) {
  console.error('错误: 未设置 ADS_API_KEY。请在 config_local.js 或环境变量中设置。');
  process.exit(1);
}

module.exports = config;
