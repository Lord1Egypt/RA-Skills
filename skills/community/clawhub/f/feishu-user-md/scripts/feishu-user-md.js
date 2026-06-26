#!/usr/bin/env node

/**
 * Feishu User.md Reader
 * 动态读取 USER.md，解析任务清单和触发指令，格式化为飞书消息
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const USER_MD = path.join(os.homedir(), '.openclaw/workspace/USER.md');

function readUserMd() {
  try {
    if (!fs.existsSync(USER_MD)) {
      return { error: 'USER.md 文件不存在' };
    }
    const content = fs.readFileSync(USER_MD, 'utf8');
    return parseUserMd(content);
  } catch (err) {
    return { error: `读取失败: ${err.message}` };
  }
}

function parseUserMd(content) {
  const result = {
    scheduled: [],
    tasks: [],
    triggers: {},
    total: 0
  };

  // 解析"常规任务清单"表格
  const taskRows = content.match(/\|\s*\d+\s*\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|/g);
  if (taskRows) {
    result.total = taskRows.length;
    taskRows.forEach(row => {
      const cells = row.split('|').map(c => c.trim()).filter(c => c);
      if (cells.length >= 6) {
        result.tasks.push({
          num: cells[0],
          name: cells[1],
          freq: cells[2],
          skill: cells[3].replace(/`/g, ''),
          desc: cells[5]
        });
      }
    });
  }

  // 解析"定时自动化"表格
  const scheduleSection = content.match(/日常自动化[\s\S]*?\n\n/);
  if (scheduleSection) {
    const timeRows = scheduleSection[0].match(/\|\s*\*\*[\d:]+\*\*\s*\|[^|]+\|[^|]+\|/g);
    if (timeRows) {
      timeRows.forEach(row => {
        const cells = row.split('|').map(c => c.trim()).filter(c => c);
        if (cells.length >= 3) {
          result.scheduled.push({
            time: cells[0].replace(/\*\*/g, ''),
            name: cells[1],
            skill: cells[2].replace(/`/g, '')
          });
        }
      });
    }
  }

  // 解析"手动触发指令"表格 → 动态构建触发词映射
  const triggerSection = content.match(/手动触发指令[\s\S]*?(?=\n---|\n##|$)/);
  if (triggerSection) {
    const triggerRows = triggerSection[0].match(/\|\s*[^|\n]+\s*\|\s*[^|\n]+\s*\|/g);
    if (triggerRows) {
      triggerRows.forEach(row => {
        const cells = row.split('|').map(c => c.trim()).filter(c => c);
        if (cells.length >= 2 && !cells[0].includes('---') && !cells[0].includes('任务')) {
          const taskName = cells[0];
          const trigger = cells[1].split('/')[0].trim().replace(/"/g, '');
          result.triggers[taskName] = trigger;
        }
      });
    }
  }

  return result;
}

/**
 * 按用途分类任务
 */
function categorize(tasks) {
  const categories = {
    '内容创作': ['图片提示词', 'API图片', '知识漫画', '信息图', 'infographic'],
    '小红书运营': ['小红书'],
    '内容发布': ['公众号', 'Markdown转HTML', '微信'],
    '工具': ['翻译', '图片压缩', '网页转', 'MySQL', 'url'],
    '新闻与SEO': ['新闻', 'SEO'],
    '日常管理': ['清理', 'token', '对话', '周报', '日历', '任务', '飞书']
  };

  const result = {};
  const used = new Set();

  for (const [cat, keywords] of Object.entries(categories)) {
    const matched = tasks.filter(t =>
      keywords.some(kw => t.name.includes(kw) || t.desc.includes(kw)) && !used.has(t.num)
    );
    if (matched.length > 0) {
      result[cat] = matched;
      matched.forEach(t => used.add(t.num));
    }
  }

  const remaining = tasks.filter(t => !used.has(t.num));
  if (remaining.length > 0) {
    result['其他'] = remaining;
  }

  return result;
}

function formatForFeishu(data) {
  if (data.error) {
    return `❌ 错误: ${data.error}`;
  }

  let msg = `📋 您的任务清单（共${data.total}项）\n\n`;

  // 定时任务
  if (data.scheduled.length > 0) {
    msg += `【定时自动化】\n`;
    data.scheduled.forEach(t => {
      msg += `• ${t.time} ${t.name}\n`;
    });
    msg += '\n';
  }

  // 按类别输出手动任务
  const grouped = categorize(data.tasks);
  for (const [cat, tasks] of Object.entries(grouped)) {
    msg += `【${cat}】\n`;
    tasks.forEach(t => {
      const trigger = data.triggers[t.name];
      msg += trigger
        ? `• ${t.name} - 说"${trigger}"\n`
        : `• ${t.name}\n`;
    });
    msg += '\n';
  }

  msg += `💡 直接发送任务关键词即可触发`;
  return msg;
}

function main() {
  const command = process.argv[2];

  if (command === 'read') {
    console.log(formatForFeishu(readUserMd()));
  } else if (command === 'json') {
    console.log(JSON.stringify(readUserMd(), null, 2));
  } else {
    console.log(`
Feishu User.md Reader - 飞书任务清单查询

用法:
  node feishu-user-md.js read    读取并格式化输出
  node feishu-user-md.js json    读取并输出JSON
`);
  }
}

main();
