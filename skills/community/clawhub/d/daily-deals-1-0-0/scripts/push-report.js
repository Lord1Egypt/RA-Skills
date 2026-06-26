#!/usr/bin/env node
/**
 * 推送报告到各渠道
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// 读取报告
const reportPath = path.join(__dirname, '../assets/daily-report.txt');
const configPath = path.join(__dirname, '../config/config.json');

// 默认配置
let config = {
  pushChannels: ['console'],
  webhooks: {}
};

// 加载配置
if (fs.existsSync(configPath)) {
  config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

// 推送到微信
async function pushToWechat(content) {
  const webhook = config.webhooks?.wechat;
  if (!webhook) {
    console.log('⚠️ 未配置微信 webhook');
    return;
  }
  
  const data = JSON.stringify({
    msgtype: 'text',
    text: { content }
  });
  
  return new Promise((resolve, reject) => {
    const req = https.request(webhook, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
      }
    }, (res) => {
      console.log('✅ 微信推送成功');
      resolve();
    });
    
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

// 推送到钉钉
async function pushToDingtalk(content) {
  const webhook = config.webhooks?.dingtalk;
  if (!webhook) {
    console.log('⚠️ 未配置钉钉 webhook');
    return;
  }
  
  const data = JSON.stringify({
    msgtype: 'text',
    text: { content }
  });
  
  return new Promise((resolve, reject) => {
    const req = https.request(webhook, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
      }
    }, (res) => {
      console.log('✅ 钉钉推送成功');
      resolve();
    });
    
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

// 主函数
async function main() {
  if (!fs.existsSync(reportPath)) {
    console.error('❌ 报告不存在，请先运行 generate-report.js');
    process.exit(1);
  }
  
  const content = fs.readFileSync(reportPath, 'utf8');
  
  console.log('🚀 开始推送报告...\n');
  
  for (const channel of config.pushChannels) {
    try {
      switch (channel) {
        case 'wechat':
          await pushToWechat(content);
          break;
        case 'dingtalk':
          await pushToDingtalk(content);
          break;
        case 'console':
        default:
          console.log('📱 控制台输出:\n');
          console.log(content);
      }
    } catch (e) {
      console.error(`❌ 推送到 ${channel} 失败:`, e.message);
    }
  }
  
  console.log('\n✅ 推送完成！');
}

main().catch(console.error);
