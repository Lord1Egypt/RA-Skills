#!/usr/bin/env node
/**
 * 解析 OpenClaw 会话文件 (.jsonl)
 * 提取 Web UI 渠道的对话记录
 */

const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  sessionsDir: '/home/admin/.openclaw/agents/main/sessions'
};

/**
 * 获取今天的日期字符串
 */
function getTodayStr() {
  const now = new Date();
  return now.toISOString().split('T')[0];
}

/**
 * 从消息文本识别渠道
 * @param {string} text - 消息文本
 * @returns {string} - 渠道标识: 'feishu' | 'webui' | 'dingtalk' | 'weixin' | 'qqbot'
 */
function detectChannel(text) {
  // 飞书：System: [时间] Feishu[default] ...
  if (/Feishu\[default\]/.test(text)) return 'feishu';
  // QQ机器人
  if (/QQBot\[default\]|qqbot/i.test(text)) return 'qqbot';
  // 企业微信
  if (/WeCom|wecom|企业微信/.test(text)) return 'weixin';
  // 钉钉
  if (/DingTalk|dingtalk|钉钉/.test(text)) return 'dingtalk';
  // 默认：webui/webchat 或其他
  return 'webui';
}

/**
 * 解析 .jsonl 文件，分离各渠道消息
 * @param {string} filePath - jsonl 文件路径
 * @param {string} dateStr - 日期过滤 (YYYY-MM-DD)
 * @returns {Object} - { feishu: [], webui: [], dingtalk: [], weixin: [], qqbot: [] }
 */
function parseJsonl(filePath, dateStr) {
  if (!fs.existsSync(filePath)) {
    return {};
  }

  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n').filter(line => line.trim());
  
  const channels = {};
  
  for (const line of lines) {
    try {
      const record = JSON.parse(line);
      
      // 只提取消息类型
      if (record.type === 'message' && record.message) {
        const msg = record.message;
        const timestamp = record.timestamp || '';
        
        // 检查是否是指定日期
        if (dateStr && !timestamp.startsWith(dateStr)) {
          continue;
        }
        
        // 提取文本内容
        let text = '';
        if (msg.content && Array.isArray(msg.content)) {
          for (const item of msg.content) {
            if (item.type === 'text') {
              text += item.text;
            }
          }
        } else if (typeof msg.content === 'string') {
          text = msg.content;
        }
        
        // 只保留有内容的
        if (text.trim()) {
          const channel = detectChannel(text);
          if (!channels[channel]) channels[channel] = [];
          
          const messageObj = {
            role: msg.role,  // 'user' 或 'assistant'
            content: text.trim(),
            channel: channel,
            timestamp: timestamp,
            time: timestamp ? new Date(timestamp).toLocaleString('zh-CN') : ''
          };
          
          channels[channel].push(messageObj);
        }
      }
    } catch (e) {
      // 解析失败，跳过
      continue;
    }
  }
  
  return channels;
}

/**
 * 获取最新的会话文件
 */
function getLatestSessionFile() {
  const sessionsDir = CONFIG.sessionsDir;
  
  if (!fs.existsSync(sessionsDir)) {
    return null;
  }
  
  const files = fs.readdirSync(sessionsDir)
    .filter(f => f.endsWith('.jsonl'))
    .map(f => {
      const fullPath = path.join(sessionsDir, f);
      const stat = fs.statSync(fullPath);
      return { file: f, path: fullPath, mtime: stat.mtime };
    })
    .sort((a, b) => b.mtime - a.mtime);
  
  return files.length > 0 ? files[0].path : null;
}

/**
 * 获取今天的消息（分离各渠道）
 */
function getTodayMessages() {
  const todayStr = getTodayStr();
  const sessionFile = getLatestSessionFile();
  
  if (!sessionFile) {
    console.error('未找到会话文件');
    return {};
  }
  
  console.error(`解析会话文件: ${sessionFile}`);
  const channels = parseJsonl(sessionFile, todayStr);
  
  return channels;
}

/**
 * 格式化消息为对话文本
 */
function formatMessages(messages) {
  if (!messages || messages.length === 0) {
    return '今天暂无对话记录';
  }
  
  let output = '';
  for (const msg of messages) {
    const role = msg.role === 'user' ? '用户' : 'AI';
    // 清理系统元数据，只保留实际内容
    let content = msg.content;
    // 去掉前置的系统前缀（如 Feishu[default] ...）
    const prefixMatch = content.match(/^System:.*?\n\n/);
    if (prefixMatch) {
      content = content.slice(prefixMatch[0].length);
    }
    // 去掉末尾的 Sender (untrusted metadata) 块
    const metaEnd = content.lastIndexOf('Sender (untrusted metadata)');
    if (metaEnd > 0) {
      // 找到 meta 块结束位置：```json ... ```
      const closeTag = content.lastIndexOf('```');
      if (closeTag > metaEnd) {
        content = content.slice(0, metaEnd).trim();
      }
    }
    output += `[${role}] ${content}\n\n`;
  }
  
  return output.trim();
}

// 主函数
function main() {
  const channels = getTodayMessages();
  
  const channelLabels = {
    feishu: '飞书',
    webui: 'WebUI',
    dingtalk: '钉钉',
    weixin: '微信',
    qqbot: 'QQ'
  };
  
  for (const [ch, msgs] of Object.entries(channels)) {
    console.error(`${channelLabels[ch] || ch}: ${msgs.length} 条消息`);
  }
  
  // 输出为 JSON（供其他脚本使用）
  const output = { date: getTodayStr() };
  for (const [ch, msgs] of Object.entries(channels)) {
    output[ch] = {
      count: msgs.length,
      messages: msgs,
      formatted: formatMessages(msgs)
    };
  }
  console.log(JSON.stringify(output, null, 2));
}

// 如果直接运行
if (require.main === module) {
  main();
}

// 导出函数
module.exports = {
  parseJsonl,
  getTodayMessages,
  formatMessages,
  getTodayStr,
  detectChannel
};
