#!/usr/bin/env node

/**
 * 钉钉群聊机器人消息推送 - Skill 核心模块
 * 
 * 可独立运行，也被 skill 系统调用
 */

import crypto from 'crypto';
import https from 'https';
import http from 'http';
import { URL } from 'url';
import fs from 'fs';
import path from 'path';
import os from 'os';

// ===== 配置管理 =====
function loadConfig() {
  // 默认配置
  const defaultConfig = {
    webhook: process.env.DINGTALK_WEBHOOK || '',
    secret: process.env.DINGTALK_SECRET || ''
  };

  // 尝试从配置文件加载
  const configPaths = [
    path.join(os.homedir(), '.config', 'dingtalk-push', 'config.json'),
    path.join(process.cwd(), '.dingtalk-push.json'),
    path.join(__dirname, 'config.json')
  ];

  for (const configPath of configPaths) {
    try {
      if (fs.existsSync(configPath)) {
        const fileConfig = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
        return { ...defaultConfig, ...fileConfig };
      }
    } catch (e) {
      // 忽略配置文件错误
    }
  }

  return defaultConfig;
}

// 生成签名
function generateSign(secret, timestamp) {
  const signStr = `${timestamp}\n${secret}`;
  const hmac = crypto.createHmac('sha256', secret);
  hmac.update(signStr);
  return encodeURIComponent(hmac.digest('base64'));
}

// 发送消息
export async function sendDingTalkMessage(options = {}) {
  const config = loadConfig();
  
  if (!config.webhook) {
    throw new Error('请配置 DINGTALK_WEBHOOK 环境变量或配置文件');
  }

  const {
    message = 'Hello from DingTalk!',
    title = '通知',
    type = 'info',
    atMobiles = [],
    isAtAll = false
  } = options;

  // 根据类型获取emoji
  const emojis = { info: 'ℹ️', success: '✅', warning: '⚠️', error: '❌' };
  const emoji = emojis[type] || 'ℹ️';
  
  // 格式化时间
  const time = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
  
  // 构建Markdown消息
  const markdownText = `### ${emoji} ${title}\n\n${message}\n\n> ⏰ ${time}`;

  // 构建请求URL
  let url = config.webhook;
  
  // 如果有加签密钥，生成签名
  if (config.secret) {
    const timestamp = Date.now();
    const sign = generateSign(config.secret, timestamp);
    const separator = url.includes('?') ? '&' : '?';
    url = `${url}${separator}timestamp=${timestamp}&sign=${sign}`;
  }

  // 解析URL
  const urlObj = new URL(url);
  const isHttps = urlObj.protocol === 'https:';
  const lib = isHttps ? https : http;

  // 构建消息体
  const msgData = {
    msgtype: 'markdown',
    markdown: {
      title: `${emoji} ${title}`,
      text: markdownText
    }
  };

  // 添加@设置
  if (atMobiles.length > 0) {
    msgData.at = { atMobiles, isAtAll: false };
  } else if (isAtAll) {
    msgData.at = { isAtAll: true };
  }

  // 发送请求
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(msgData);

    const req = lib.request({
      hostname: urlObj.hostname,
      port: urlObj.port || (isHttps ? 443 : 80),
      path: urlObj.pathname + urlObj.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.errcode === 0) {
            resolve({
              success: true,
              messageId: result.msg_id,
              timestamp: new Date().toISOString()
            });
          } else {
            reject(new Error(`钉钉API错误: ${result.errmsg}`));
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

// ===== CLI 入口 =====
function parseArgs() {
  const args = process.argv.slice(2);
  const config = {
    message: '',
    title: '',
    type: 'info',
    atMobiles: [],
    isAtAll: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case '-m':
      case '--message':
        config.message = args[++i];
        break;
      case '-t':
      case '--title':
        config.title = args[++i];
        break;
      case '--type':
        config.type = args[++i];
        break;
      case '--at':
        config.atMobiles = args[++i].split(',');
        break;
      case '--all':
        config.isAtAll = true;
        break;
      case '-h':
      case '--help':
        console.log(`
钉钉群聊机器人消息推送

用法: node send.js [选项]

选项:
  -m, --message <text>  消息内容
  -t, --title <text>   消息标题
  --type <type>        消息类型 (info/success/warning/error)
  --at <phones>        @指定人员手机号
  --all                @所有人
  -h, --help           帮助
`);
        process.exit(0);
    }
  }

  return config;
}

// 主函数
async function main() {
  const args = parseArgs();
  
  if (!args.message) {
    // 测试模式
    console.log('📤 发送测试消息...');
  }

  try {
    const result = await sendDingTalkMessage({
      message: args.message || '🧪 钉钉推送技能测试成功！',
      title: args.title || '测试通知',
      type: args.type,
      atMobiles: args.atMobiles,
      isAtAll: args.isAtAll
    });
    
    console.log('✅ 发送成功!');
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('❌ 发送失败:', error.message);
    process.exit(1);
  }
}

// 如果直接运行
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export default { sendDingTalkMessage };
