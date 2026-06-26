// daily-reminder 每日提醒技能
const fs = require('fs');
const path = require('path');

const SKILL_DIR = __dirname;

// 数据文件路径
const FILES = {
  reminders: path.join(SKILL_DIR, 'reminders.json'),
  countdowns: path.join(SKILL_DIR, 'countdowns.json'),
  anniversaries: path.join(SKILL_DIR, 'anniversaries.json')
};

// 初始化数据文件
function initFiles() {
  for (const [key, filePath] of Object.entries(FILES)) {
    if (!fs.existsSync(filePath)) {
      fs.writeFileSync(filePath, JSON.stringify([], null, 2));
    }
  }
}

// 读取数据
function loadData(type) {
  try {
    const data = fs.readFileSync(FILES[type], 'utf-8');
    return JSON.parse(data);
  } catch {
    return [];
  }
}

// 保存数据
function saveData(type, data) {
  fs.writeFileSync(FILES[type], JSON.stringify(data, null, 2));
}

// 解析日期
function parseDate(text) {
  const now = new Date();
  const patterns = [
    /(\d{1,2})月(\d{1,2})日/,
    /(\d{4})-(\d{1,2})-(\d{1,2})/,
    /明天/,
    /今天/,
    /下周/,
    /下周(\d)/
  ];
  
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      if (pattern.toString().includes('明天')) {
        const d = new Date(now);
        d.setDate(d.getDate() + 1);
        return d;
      }
      if (pattern.toString().includes('今天')) {
        return now;
      }
    }
  }
  return null;
}

module.exports = {
  name: 'daily-reminder',
  description: '每日提醒、倒计时、纪念日管理',
  version: '1.0.0',
  author: '黄豆豆',
  
  // 激活条件
  activate(message) {
    const keywords = ['提醒', '倒计时', '纪念日', '查看提醒', '我的提醒'];
    return keywords.some(k => message.includes(k));
  },
  
  async handle(context) {
    const message = context.message || '';
    const lowerMessage = message.toLowerCase();
    
    initFiles();
    
    // 解析提醒设置
    if (lowerMessage.includes('提醒') && !lowerMessage.includes('查看')) {
      return this.setReminder(message);
    }
    
    // 解析倒计时
    if (lowerMessage.includes('倒计时')) {
      return this.setCountdown(message);
    }
    
    // 解析纪念日
    if (lowerMessage.includes('纪念日')) {
      return this.setAnniversary(message);
    }
    
    // 查看所有提醒
    if (lowerMessage.includes('查看提醒') || lowerMessage.includes('我的提醒')) {
      return this.listReminders();
    }
    
    return null;
  },
  
  setReminder(message) {
    const reminders = loadData('reminders');
    const reminder = {
      id: Date.now(),
      text: message,
      created: new Date().toISOString()
    };
    
    reminders.push(reminder);
    saveData('reminders', reminders);
    
    return {
      success: true,
      message: `✅ 提醒已设置！\n内容：${message}\n\n输入"查看提醒"可查看所有提醒`
    };
  },
  
  setCountdown(message) {
    const countdowns = loadData('countdowns');
    const targetText = message.replace(/倒计时[到]?/i, '').trim();
    
    const countdown = {
      id: Date.now(),
      target: targetText,
      created: new Date().toISOString()
    };
    
    countdowns.push(countdown);
    saveData('countdowns', countdowns);
    
    return {
      success: true,
      message: `✅ 倒计时已设置！\n目标：${countdown.target}\n\n输入"查看提醒"可查看倒计时列表`
    };
  },
  
  setAnniversary(message) {
    const anniversaries = loadData('anniversaries');
    const name = message.replace(/纪念日/i, '').replace(/：/g, ':').replace(/:/g, ':').trim();
    
    const anniversary = {
      id: Date.now(),
      name: name,
      created: new Date().toISOString()
    };
    
    anniversaries.push(anniversary);
    saveData('anniversaries', anniversaries);
    
    return {
      success: true,
      message: `✅ 纪念日已记录：${anniversary.name}\n\n输入"查看提醒"可查看所有纪念日`
    };
  },
  
  listReminders() {
    const reminders = loadData('reminders');
    const countdowns = loadData('countdowns');
    const anniversaries = loadData('anniversaries');
    
    let msg = '📋 您的提醒列表：\n\n';
    
    if (reminders.length > 0) {
      msg += '⏰ 定时提醒：\n';
      reminders.forEach((r, i) => {
        msg += `  ${i + 1}. ${r.text}\n`;
      });
    }
    
    if (countdowns.length > 0) {
      msg += '\n⏳ 倒计时：\n';
      countdowns.forEach((c, i) => {
        msg += `  ${i + 1}. ${c.target}\n`;
      });
    }
    
    if (anniversaries.length > 0) {
      msg += '\n🎂 纪念日：\n';
      anniversaries.forEach((a, i) => {
        msg += `  ${i + 1}. ${a.name}\n`;
      });
    }
    
    if (reminders.length === 0 && countdowns.length === 0 && anniversaries.length === 0) {
      msg = '📋 暂无任何提醒\n\n输入"提醒xxx"即可设置定时提醒\n输入"倒计时xxx"设置倒计时\n输入"纪念日xxx"记录纪念日';
    }
    
    return { message: msg };
  }
};
