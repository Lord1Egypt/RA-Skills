#!/usr/bin/env node

/**
 * WeChat Automation - 企业微信自动化技能
 * 
 * 用法:
 *   clawhub wechat send --text "消息内容"
 *   clawhub wechat send --markdown "**标题**\n\n内容"
 */

const https = require('https');
const http = require('http');

// 配置
const WEBHOOK_URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send';

/**
 * 发送企业微信消息
 * @param {Object} options
 * @param {string} options.webhookKey - 企业微信 Webhook Key
 * @param {string} options.text - 消息内容
 * @param {boolean} options.markdown - 是否使用 Markdown 格式
 * @param {string} options.chatid - 目标群聊 ID（可选）
 * @param {Array} options.mentioned_list - 需要@的用户列表（可选）
 */
async function sendMessage(options) {
  const { webhookKey, text, markdown = false, chatid, mentioned_list = [] } = options;

  if (!webhookKey) {
    throw new Error('缺少 webhookKey，请使用 clawhub config set wechat.webhook_key YOUR_KEY 设置');
  }

  if (!text) {
    throw new Error('缺少消息内容');
  }

  const payload = {
    msgtype: markdown ? 'markdown' : 'text'
  };

  if (markdown) {
    payload.markdown = { content: text };
  } else {
    payload.text = {
      content: text,
      mentioned_list: mentioned_list.length > 0 ? mentioned_list : ['@all']
    };
  }

  if (chatid) {
    payload.chatid = chatid;
  }

  return new Promise((resolve, reject) => {
    const url = `${WEBHOOK_URL}?key=${webhookKey}`;
    const data = JSON.stringify(payload);

    const req = https.request(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
      }
    }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          if (result.errcode === 0) {
            resolve(result);
          } else {
            reject(new Error(`企业微信 API 错误：${result.errmsg}`));
          }
        } catch (e) {
          reject(new Error(`解析响应失败：${body}`));
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

/**
 * CLI 入口
 */
async function main() {
  const args = process.argv.slice(2);
  
  // 解析参数
  const options = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--text' && args[i + 1]) {
      options.text = args[++i];
    } else if (args[i] === '--markdown') {
      options.markdown = true;
    } else if (args[i] === '--webhook-key' && args[i + 1]) {
      options.webhookKey = args[++i];
    } else if (args[i] === '--chatid' && args[i + 1]) {
      options.chatid = args[++i];
    }
  }

  if (!options.text) {
    console.error('用法：clawhub wechat send --text "消息内容" [--markdown] [--webhook-key KEY]');
    process.exit(1);
  }

  try {
    const result = await sendMessage(options);
    console.log('✅ 消息发送成功！');
    console.log('消息 ID:', result.msgid);
  } catch (error) {
    console.error('❌ 发送失败:', error.message);
    process.exit(1);
  }
}

// 导出 API
module.exports = { sendMessage };

// 如果是直接执行
if (require.main === module) {
  main();
}
