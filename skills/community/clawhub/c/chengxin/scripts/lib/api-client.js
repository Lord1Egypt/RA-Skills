#!/usr/bin/env node

/**
 * 同程程心 API 客户端
 *
 * 提供统一的 API 调用接口和配置管理
 */

const https = require('https');
const url = require('url');
const fs = require('fs');
const path = require('path');

// 接口基础配置
const API_BASE_URL = 'https://wx.17u.cn/skills/gateway/api/v1/gateway';
const API_VERSION = '0.9.0';

// 超时配置（15 秒）
const API_TIMEOUT = 15000;

// 配置读取（优先级：环境变量 > config.json）
let API_KEY = process.env.CHENGXIN_API_KEY;

if (!API_KEY) {
  try {
    const config_path = path.join(__dirname, '..', '..', 'config.json');
    const config = JSON.parse(fs.readFileSync(config_path, 'utf8'));
    API_KEY = config.apiKey;
  } catch (e) {
    // 静默处理：文件不存在走试用额度，其他异常由后续 API 调用的错误码 3 引导配置
  }
}

/**
 * 获取 API Key
 * @returns {string|null} API Key 或 null
 */
function get_api_key() {
  return API_KEY || null;
}

/**
 * 构建 Authorization Token
 * @param {string} key - API Key
 * @returns {string} Token 字符串
 */
function build_auth_token(key) {
  if (!key) return '';
  return `Bearer ${key}`;
}

/**
 * 调用同程程心 API
 * @param {string} api_path - API 路径（如 /trainResource）
 * @param {object} params - 查询参数
 * @returns {Promise<object>} API 响应
 */
function call_api(api_path, params) {
  return new Promise((resolve, reject) => {
    const api_url = `${API_BASE_URL}${api_path}`;
    const parsed_url = url.parse(api_url);
    if (parsed_url.protocol !== 'https:') {
      reject(new Error('仅支持 HTTPS 协议，请检查 API_BASE_URL'));
      return;
    }

    const post_data = JSON.stringify({
      ...params,
      version: API_VERSION
    });

    const options = {
      hostname: parsed_url.hostname,
      port: parsed_url.port || 443,
      path: parsed_url.path,
      method: 'POST',
      timeout: API_TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(post_data),
        'User-Agent': `Chengxin-NodeJS/${API_VERSION}`,
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://www.ly.com',
        'Referer': 'https://www.ly.com/',
        ...(API_KEY ? { 'Authorization': build_auth_token(API_KEY) } : {})
      }
    };

    const req = https.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        // 检查 HTTP 状态码
        if (res.statusCode < 200 || res.statusCode >= 300) {
          reject(new Error(`HTTP 错误：${res.statusCode} ${res.statusMessage || ''}`));
          return;
        }

        try {
          const result = JSON.parse(data);
          resolve(result);
        } catch (e) {
          reject(new Error(`解析响应失败：${e.message}`));
        }
      });
    });

    // 超时处理
    req.on('timeout', () => {
      req.destroy();
      reject(new Error(`请求超时（${API_TIMEOUT / 1000}秒）`));
    });

    req.on('error', (e) => {
      reject(new Error(`请求失败：${e.message}`));
    });

    req.write(post_data);
    req.end();
  });
}

/**
 * 验证 API Key 是否已配置
 * @returns {boolean} 是否已配置
 */
function is_configured() {
  return !!API_KEY;
}

/**
 * 获取配置错误信息
 * @returns {string} 错误信息
 */
function get_config_error() {
  if (!API_KEY) {
    return '未找到 CHENGXIN_API_KEY 环境变量或 config.json 文件\n请设置环境变量或在技能目录下创建 config.json 文件';
  }
  return '';
}

module.exports = {
  API_BASE_URL,
  API_VERSION,
  get_api_key,
  build_auth_token,
  call_api,
  is_configured,
  get_config_error
};
