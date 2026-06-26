#!/usr/bin/env node

/**
 * API 快速测试工具
 */

const https = require('https');
const http = require('http');

const args = process.argv.slice(2);
const urlIndex = args.indexOf('--url');
const methodIndex = args.indexOf('--method');
const authIndex = args.indexOf('--auth');
const bodyIndex = args.indexOf('--body');

if (urlIndex === -1) {
  console.log(`
📖 API 快速测试工具

用法:
  node test.js --url <URL> [--method <方法>] [--auth <认证>] [--body <JSON>]

参数:
  --url      API 地址
  --method   HTTP 方法 (GET/POST/PUT/DELETE, 默认 GET)
  --auth     认证 (bearer:TOKEN / basic:USER:PASS / apikey:KEY_NAME:KEY)
  --body     请求体 (JSON 字符串)

示例:
  node test.js --url https://api.example.com/users
  node test.js --url https://api.example.com/users --method POST --body '{"name":"Test"}'
  node test.js --url https://api.example.com/users --auth bearer:YOUR_TOKEN
`);
  process.exit(0);
}

const url = args[urlIndex + 1];
const method = methodIndex !== -1 ? args[methodIndex + 1].toUpperCase() : 'GET';
const auth = authIndex !== -1 ? args[authIndex + 1] : null;
const body = bodyIndex !== -1 ? args[bodyIndex + 1] : null;

// 解析 URL
const urlObj = new URL(url);
const isHttps = urlObj.protocol === 'https:';
const lib = isHttps ? https : http;

// 构建请求头
const headers = {
  'Content-Type': 'application/json'
};

// 添加认证
if (auth) {
  const [type, ...parts] = auth.split(':');
  if (type === 'bearer') {
    headers['Authorization'] = `Bearer ${parts[0]}`;
  } else if (type === 'basic') {
    const credentials = Buffer.from(`${parts[0]}:${parts[1]}`).toString('base64');
    headers['Authorization'] = `Basic ${credentials}`;
  } else if (type === 'apikey') {
    headers[parts[0]] = parts[1];
  }
}

const startTime = Date.now();

const options = {
  hostname: urlObj.hostname,
  port: urlObj.port || (isHttps ? 443 : 80),
  path: urlObj.pathname + urlObj.search,
  method: method,
  headers: headers
};

console.log(`\n📊 API 测试报告\n`);
console.log(`URL: ${url}`);
console.log(`Method: ${method}`);

const req = lib.request(options, (res) => {
  let data = '';

  res.on('data', chunk => {
    data += chunk;
  });

  res.on('end', () => {
    const time = Date.now() - startTime;

    console.log(`Status: ${res.statusCode} ${res.statusMessage}`);
    console.log(`Time: ${time}ms\n`);

    console.log('Response:');
    try {
      const json = JSON.parse(data);
      console.log(JSON.stringify(json, null, 2));
    } catch {
      console.log(data);
    }

    // 判断测试结果
    const isSuccess = res.statusCode >= 200 && res.statusCode < 300;
    console.log(`\n${isSuccess ? '✅ 测试通过' : '❌ 测试失败'}\n`);
  });
});

req.on('error', (error) => {
  const time = Date.now() - startTime;
  console.log(`Time: ${time}ms\n`);
  console.log(`❌ 请求失败: ${error.message}\n`);
});

// 发送请求体
if (body && ['POST', 'PUT', 'PATCH'].includes(method)) {
  req.write(body);
}

req.end();
