
#!/usr/bin/env node

/**
 * DataHub 查询提交脚本
 * 用法: node query.js "<自然语言查询>" [sessionId]
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
const TIMEOUT = CONFIG.timeout;
const API_KEY = CONFIG.apiKey;

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
 * 提交查询到DataHub
 */
async function submitQuery(query, sessionId = null) {
  const url = new URL('/api/datahub/execute/v0', BASE_URL);
  
  const payload = JSON.stringify({
    query: query,
    sessionId: sessionId || undefined,
    key: API_KEY  // 添加API Key到请求体
  });

  const options = {
    hostname: url.hostname,
    port: url.port || (url.protocol === 'https:' ? 443 : 80),
    path: url.pathname,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(payload),
      'X-API-Key': API_KEY  // 同时通过Header传递
    },
    timeout: TIMEOUT
  };

  return new Promise((resolve, reject) => {
    const client = url.protocol === 'https:' ? https : http;
    
    const req = client.request(options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            // 尝试解析JSON响应
            const jsonData = JSON.parse(data);
            const processId = jsonData.processId || jsonData.id || jsonData.taskId || data;
            
            resolve({
              success: true,
              processId: processId,
              status: jsonData.status || 'submitted',
              rawResponse: jsonData
            });
          } catch (e) {
            // 如果不是JSON，尝试从文本中提取processId
            const match = data.match(/[a-zA-Z0-9_-]{20,}/);
            const processId = match ? match[0] : data;
            
            resolve({
              success: true,
              processId: processId,
              status: 'submitted',
              rawResponse: data
            });
          }
        } else if (res.statusCode === 401 || res.statusCode === 403) {
          reject(new Error('API Key无效或已过期，请检查配置'));
        } else {
          reject(new Error(`请求失败: HTTP ${res.statusCode} - ${data}`));
        }
      });
    });
    
    req.on('error', (err) => {
      reject(new Error(`网络错误: ${err.message}`));
    });
    
    req.on('timeout', () => {
      req.destroy();
      reject(new Error(`请求超时 (${TIMEOUT}ms)`));
    });
    
    req.write(payload);
    req.end();
  });
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.error('用法: node query.js "<自然语言查询>" [sessionId]');
    process.exit(1);
  }
  
  const query = args[0];
  const sessionId = args[1] || null;
  
  try {
    const result = await submitQuery(query, sessionId);
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
