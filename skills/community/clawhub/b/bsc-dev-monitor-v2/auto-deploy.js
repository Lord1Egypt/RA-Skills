#!/usr/bin/env node

/**
 * ClawHub 自动部署脚本
 * 使用账号密码登录并上传 Skill
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// 登录凭证
const CREDENTIALS = {
  email: 'hefang080@gmail.com',
  password: 'hefang198511633'
};

// Skill 信息
const SKILL_INFO = {
  name: 'bsc-dev-monitor',
  version: '1.0.0',
  description: 'BSC Dev Wallet Monitor - 监控指定地址的代币转出行为',
  price: '0.01',
  currency: 'USDT',
  category: 'Crypto / Trading / Monitor',
  tags: ['bsc', 'monitor', 'trading', 'crypto', 'defi']
};

// Cookie 存储
let sessionCookie = '';

/**
 * HTTP 请求辅助函数
 */
function makeRequest(options, data = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let responseData = '';

      // 保存 cookies
      if (res.headers['set-cookie']) {
        sessionCookie = res.headers['set-cookie'].map(c => c.split(';')[0]).join('; ');
      }

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        try {
          const parsed = JSON.parse(responseData);
          resolve({ statusCode: res.statusCode, data: parsed, headers: res.headers });
        } catch (e) {
          resolve({ statusCode: res.statusCode, data: responseData, headers: res.headers });
        }
      });
    });

    req.on('error', reject);

    if (data) {
      req.write(data);
    }

    req.end();
  });
}

/**
 * 登录 ClawHub
 */
async function login() {
  console.log('🔐 正在登录 ClawHub...\n');

  const loginData = JSON.stringify({
    email: CREDENTIALS.email,
    password: CREDENTIALS.password
  });

  const options = {
    hostname: 'clawhub.ai',
    port: 443,
    path: '/api/auth/login',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(loginData),
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      'Origin': 'https://clawhub.ai',
      'Referer': 'https://clawhub.ai/upload'
    }
  };

  try {
    const response = await makeRequest(options, loginData);

    if (response.statusCode === 200 || response.statusCode === 201) {
      console.log('✅ 登录成功！');
      console.log(`   用户: ${CREDENTIALS.email}\n`);
      return true;
    } else {
      console.log('❌ 登录失败');
      console.log(`   状态码: ${response.statusCode}`);
      console.log(`   响应: ${JSON.stringify(response.data, null, 2)}\n`);
      return false;
    }
  } catch (error) {
    console.error('❌ 登录错误:', error.message);
    console.log('\n💡 可能需要手动登录完成部署\n');
    return false;
  }
}

/**
 * 上传 Skill 文件
 */
async function uploadSkill() {
  console.log('📤 正在上传 Skill...\n');

  const zipPath = '/root/.openclaw/workspace/bsc-dev-monitor-skill.zip';
  const fileData = fs.readFileSync(zipPath);

  // 构建表单数据
  const boundary = `----WebKitFormBoundary${Date.now()}`;
  let postData = '';

  // 添加 Skill 信息
  for (const [key, value] of Object.entries(SKILL_INFO)) {
    postData += `--${boundary}\r\n`;
    postData += `Content-Disposition: form-data; name="${key}"\r\n\r\n`;
    postData += `${value}\r\n`;
  }

  // 添加文件
  postData += `--${boundary}\r\n`;
  postData += `Content-Disposition: form-data; name="file"; filename="bsc-dev-monitor-skill.zip"\r\n`;
  postData += `Content-Type: application/zip\r\n\r\n`;
  const postDataBuffer = Buffer.from(postData);

  const options = {
    hostname: 'clawhub.ai',
    port: 443,
    path: '/api/skills/upload',
    method: 'POST',
    headers: {
      'Content-Type': `multipart/form-data; boundary=${boundary}`,
      'Content-Length': Buffer.byteLength(postData) + fileData.length,
      'Cookie': sessionCookie,
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      'Origin': 'https://clawhub.ai',
      'Referer': 'https://clawhub.ai/upload'
    }
  };

  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        try {
          const result = JSON.parse(responseData);

          if (res.statusCode === 200 || res.statusCode === 201) {
            console.log('✅ 上传成功！');
            console.log(`   Skill: ${SKILL_INFO.name}`);
            console.log(`   版本: ${SKILL_INFO.version}`);
            console.log(`   价格: ${SKILL_INFO.price} ${SKILL_INFO.currency}\n`);

            if (result.skill_url || result.url) {
              console.log(`🔗 Skill 链接: ${result.skill_url || result.url}\n`);
            }

            resolve(result);
          } else {
            console.log('❌ 上传失败');
            console.log(`   状态码: ${res.statusCode}`);
            console.log(`   响应: ${JSON.stringify(result, null, 2)}\n`);
            reject(new Error('Upload failed'));
          }
        } catch (e) {
          console.log('❌ 上传失败');
          console.log(`   响应: ${responseData}\n`);
          reject(new Error('Upload failed'));
        }
      });
    });

    req.on('error', reject);

    // 发送数据和文件
    req.write(postDataBuffer);
    req.write(fileData);
    req.write(`\r\n--${boundary}--\r\n`);
    req.end();
  });
}

/**
 * 主函数
 */
async function main() {
  console.log('🚀 开始部署到 ClawHub...\n');
  console.log('📦 Skill 信息:');
  console.log(`   名称: ${SKILL_INFO.name}`);
  console.log(`   版本: ${SKILL_INFO.version}`);
  console.log(`   价格: ${SKILL_INFO.price} ${SKILL_INFO.currency}`);
  console.log('');

  // 尝试登录
  const loginSuccess = await login();

  if (!loginSuccess) {
    console.log('⚠️  自动登录失败，请手动完成部署');
    console.log('');
    console.log('📋 手动部署步骤:');
    console.log('1. 访问: https://clawhub.ai/upload');
    console.log('2. 登录:');
    console.log(`   邮箱: ${CREDENTIALS.email}`);
    console.log(`   密码: ${CREDENTIALS.password}`);
    console.log('3. 上传文件: /root/.openclaw/workspace/bsc-dev-monitor-skill.zip');
    console.log('4. 填写 Skill 信息');
    console.log('5. 提交审核');
    console.log('');
    return;
  }

  // 上传 Skill
  try {
    await uploadSkill();
    console.log('🎉 部署完成！');
    console.log('');
    console.log('📊 下一步:');
    console.log('   - 等待审核（通常 1-2 小时）');
    console.log('   - 审核通过后用户可以搜索安装');
    console.log('   - 搜索关键词: bsc-dev-monitor');
  } catch (error) {
    console.error('❌ 部署失败:', error.message);
    console.log('\n💡 请手动完成部署\n');
  }
}

// 运行
main().catch(console.error);
