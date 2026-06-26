#!/usr/bin/env node
/**
 * 配置加载模块
 * 
 * 功能：
 * - 加载统一配置（config/config.json）
 * - 支持环境变量覆盖
 * - 命令行参数覆盖
 */

const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, '../../config/config.json');

/**
 * 加载配置文件
 */
function loadConfigFile(filePath) {
  if (!fs.existsSync(filePath)) {
    console.warn(`配置文件不存在：${filePath}`);
    return {};
  }
  return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
}

/**
 * 合并配置（优先级：命令行 > 环境变量 > config.json）
 */
function loadConfig(cliParams = {}) {
  // 加载统一配置
  const config = loadConfigFile(CONFIG_FILE);
  
  // 环境变量覆盖（用于敏感信息）
  if (process.env.OZON_CLIENT_ID) config.ozon.clientId = process.env.OZON_CLIENT_ID;
  if (process.env.OZON_API_KEY) config.ozon.apiKey = process.env.OZON_API_KEY;
  if (process.env.DASHSCOPE_API_KEY) config.llm.apiKey = process.env.DASHSCOPE_API_KEY;
  if (process.env.BAIDU_OCR_API_KEY) config.ocr.apiKey = process.env.BAIDU_OCR_API_KEY;
  if (process.env.BAIDU_OCR_SECRET_KEY) config.ocr.secretKey = process.env.BAIDU_OCR_SECRET_KEY;
  if (process.env.XIANGJI_USER_KEY) config.translator.userKey = process.env.XIANGJI_USER_KEY;
  if (process.env.XIANGJI_IMG_TRANS_KEY) config.translator.imgTransKey = process.env.XIANGJI_IMG_TRANS_KEY;
  
  // 命令行参数覆盖
  if (cliParams.pauseBeforeUpload !== undefined) config.common.pauseBeforeUpload = cliParams.pauseBeforeUpload;
  if (cliParams.profitMargin !== undefined) config.pricing.defaultProfit = cliParams.profitMargin;
  
  return config;
}

/**
 * 保存配置
 */
function saveConfig(config) {
  const configDir = path.dirname(CONFIG_FILE);
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
}

module.exports = {
  loadConfig,
  saveConfig,
  CONFIG_FILE
};
