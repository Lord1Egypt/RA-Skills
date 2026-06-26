// daily-briefing handler
// 定时早报生成 Skill

const SKILL_NAME = 'daily-briefing';

async function handle(text, context) {
  const config = loadConfig();
  const topic = detectTopic(text);
  
  // 生成早报内容
  const report = await generateBriefing(topic, config);
  
  // 推送到飞书
  if (config.feishu_chat_id) {
    await sendToFeishu(report, config.feishu_chat_id);
    return '📰 早报已生成并推送！';
  }
  
  return report;
}

function detectTopic(text) {
  const topics = {
    '财经': 'finance',
    '科技': 'tech', 
    'AI': 'ai',
    '股市': 'stock',
    '综合': 'general'
  };
  for (const [key, value] of Object.entries(topics)) {
    if (text.includes(key)) return value;
  }
  return 'general';
}

function loadConfig() {
  try {
    const fs = require('fs');
    const path = require('path');
    const configPath = path.join(__dirname, '../config.json');
    return fs.existsSync(configPath) ? JSON.parse(fs.readFileSync(configPath)) : {};
  } catch { return {}; }
}

async function sendToFeishu(content, chatId) {
  // 调用飞书消息推送
  const { message } = require('openart');
  await message.send({ channel: 'feishu', target: chatId, message: content });
}

module.exports = { handle };
