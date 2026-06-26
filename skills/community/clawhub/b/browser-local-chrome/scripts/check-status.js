#!/usr/bin/env node

/**
 * 检查浏览器状态
 * 
 * 用法：node scripts/check-status.js [端口]
 */

const https = require('https');
const http = require('http');

const CDP_PORT = process.argv[2] || '9222';
const CDP_URL = `http://127.0.0.1:${CDP_PORT}/json/version`;

console.log('🔍 检查浏览器状态...\n');

http.get(CDP_URL, (res) => {
  let data = '';
  
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    if (res.statusCode === 200) {
      const info = JSON.parse(data);
      console.log('✅ Chrome 调试模式运行中！');
      console.log('   版本:', info.Browser);
      console.log('   V8 版本:', info['V8-Version']);
      console.log('   WebKit 版本:', info['WebKit-Version']);
      console.log('   CDP 地址:', CDP_URL);
      console.log('   WebSocket:', info.webSocketDebuggerUrl);
    } else {
      console.error('❌ CDP 响应异常:', res.statusCode);
    }
  });
}).on('error', (err) => {
  console.error('❌ 无法连接到 Chrome 调试模式');
  console.error('   错误:', err.message);
  console.error('\n💡 提示：');
  console.error('   1. 启动 Chrome: node scripts/start-chrome.js');
  console.error('   2. 检查端口是否被占用：netstat -ano | findstr :9222');
  process.exit(1);
});
