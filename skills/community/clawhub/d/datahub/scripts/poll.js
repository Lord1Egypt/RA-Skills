#!/usr/bin/env node

/**
 * DataHub 结果轮询脚本
 * 用法: node poll.js <processId> [--max-attempts 60] [--interval 1000]
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');
const fs = require('fs');
const path = require('path');
const os = require('os');

// 配置加载
function loadConfig() {
  const config = {
    apiKey: process.env.DATAHUB_API_KEY || null,
    baseUrl: process.env.DATAHUB_BASE_URL || 'https://datahub.codes',
    timeout: parseInt(process.env.DATAHUB_TIMEOUT) || 60000
  };

  // 尝试从配置文件加载
  const configPaths = [
    path.join(os.homedir(), '.datahub', 'config.json'),
    path.join(process.cwd(), '.datahub.json'),
    path.join(process.cwd(), 'datahub.config.json')
  ];

  for (const configPath of configPaths) {
    try {
      if (fs.existsSync(configPath)) {
        const fileConfig = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
        config.apiKey = config.apiKey || fileConfig.apiKey;
        config.baseUrl = fileConfig.baseUrl || config.baseUrl;
        config.timeout = fileConfig.timeout || config.timeout;
        break;
      }
    } catch (e) {
      // 忽略配置文件读取错误
    }
  }

  return config;
}

const CONFIG = loadConfig();
const BASE_URL = CONFIG.baseUrl;
const API_KEY = CONFIG.apiKey;

const DEFAULT_MAX_ATTEMPTS = 60;
const DEFAULT_INTERVAL = 1000;

// 检查API Key
if (!API_KEY) {
  console.error(JSON.stringify({
    success: false,
    error: '缺少API Key。请设置环境变量 DATAHUB_API_KEY 或在 ~/.datahub/config.json 中配置',
    hint: 'export DATAHUB_API_KEY="your-key-here"'
  }));
  process.exit(1);
}

/**
 * 解析命令行参数
 */
function parseArgs(args) {
  const result = {
    processId: null,
    maxAttempts: DEFAULT_MAX_ATTEMPTS,
    interval: DEFAULT_INTERVAL
  };
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--max-attempts' || arg === '-m') {
      result.maxAttempts = parseInt(args[++i]) || DEFAULT_MAX_ATTEMPTS;
    } else if (arg === '--interval' || arg === '-i') {
      result.interval = parseInt(args[++i]) || DEFAULT_INTERVAL;
    } else if (!result.processId) {
      result.processId = arg;
    }
  }
  
  return result;
}

/**
 * 获取处理结果
 */
async function fetchResult(processId) {
  const url = new URL(`/api/processes/${processId}.md`, BASE_URL);
  
  // 将API Key添加到查询参数
  url.searchParams.append('key', API_KEY);
  
  const options = {
    hostname: url.hostname,
    port: url.port || (url.protocol === 'https:' ? 443 : 80),
    path: url.pathname + url.search,
    method: 'GET',
    headers: {
      'Accept': 'application/json, text/markdown, text/plain, */*',
      'X-API-Key': API_KEY  // 同时通过Header传递
    }
  };

  return new Promise((resolve, reject) => {
    const client = url.protocol === 'https:' ? https : http;
    
    const req = client.request(options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        if (res.statusCode === 200) {
          // 尝试解析JSON
          let parsedData = data;
          let isJson = false;
          
          try {
            parsedData = JSON.parse(data);
            isJson = true;
          } catch (e) {
            // 保持原始文本
          }
          
          resolve({
            success: true,
            data: parsedData,
            isJson: isJson,
            contentType: res.headers['content-type']
          });
        } else if (res.statusCode === 404) {
          resolve({
            success: false,
            ready: false,
            statusCode: 404
          });
        } else if (res.statusCode === 401 || res.statusCode === 403) {
          reject(new Error('API Key无效或已过期，请检查配置'));
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
        }
      });
    });
    
    req.on('error', (err) => {
      reject(new Error(`网络错误: ${err.message}`));
    });
    
    req.end();
  });
}

/**
 * 等待指定毫秒
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 轮询获取结果
 */
async function pollForResult(processId, maxAttempts, interval) {
  const startTime = Date.now();
  
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      const result = await fetchResult(processId);
      
      if (result.success) {
        // 结果已就绪
        return {
          success: true,
          data: result.data,
          isJson: result.isJson,
          attempts: attempt,
          elapsed: Date.now() - startTime
        };
      }
      
      if (attempt < maxAttempts) {
        // 结果未就绪，等待后继续
        await sleep(interval);
      }
      
    } catch (error) {
      // 认证错误直接抛出，不重试
      if (error.message.includes('API Key')) {
        throw error;
      }
      
      // 其他网络错误，等待后重试
      if (attempt < maxAttempts) {
        await sleep(interval);
      } else {
        throw error;
      }
    }
  }
  
  // 达到最大尝试次数
  throw new Error(`轮询超时: 已达到最大尝试次数 ${maxAttempts}`);
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  const config = parseArgs(args);
  
  if (!config.processId) {
    console.error('用法: node poll.js <processId> [--max-attempts 60] [--interval 1000]');
    process.exit(1);
  }
  
  try {
    const result = await pollForResult(
      config.processId,
      config.maxAttempts,
      config.interval
    );
    
    console.log(JSON.stringify(result));
  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message
    }));
    process.exit(1);
  }
}

main();
