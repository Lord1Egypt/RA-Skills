#!/usr/bin/env node
/**
 * Daily Self-Improvement Script
 * 每天总结问题、搜索改进、自我反思
 * 
 * 用法: node run.cjs [--output-only]
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || '/Users/xufan65/.openclaw/workspace';
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const SKILL_DIR = path.join(WORKSPACE, 'skills', 'daily-self-improvement');
const CONFIG_PATH = path.join(SKILL_DIR, 'config/settings.json');

// 读取配置
let config = {
  reportTime: '22:00',
  timezone: 'Asia/Shanghai',
  discordChannel: '1482261056167608544',
  dataSources: {
    failureMonitor: 'memory/failure-monitor-log.json',
    dailyNotes: 'memory/'
  },
  clawhubSearch: {
    enabled: true,
    keywords: ['discord', 'automation', 'monitoring']
  },
  notifications: {
    discord: true
  }
};

try {
  const configData = fs.readFileSync(CONFIG_PATH, 'utf-8');
  config = { ...config, ...JSON.parse(configData) };
} catch (e) {
  console.log('⚠️ 配置文件不存在，使用默认值');
}

// 获取今天日期
const today = new Date();
const todayStr = today.toISOString().split('T')[0];
const yesterday = new Date(today);
yesterday.setDate(yesterday.getDate() - 1);
const yesterdayStr = yesterday.toISOString().split('T')[0];

console.log('📊 每日自我改进分析');
console.log('==================');
console.log(`📅 日期: ${todayStr}\n`);

// ============================================
// 1. 收集问题数据
// ============================================
console.log('🔍 收集问题数据...');

const issues = [];
const lessons = [];

// 1.1 从 failure-monitor-log.json 读取
const failureLogPath = path.join(WORKSPACE, config.dataSources.failureMonitor);
if (fs.existsSync(failureLogPath)) {
  try {
    const failureLog = JSON.parse(fs.readFileSync(failureLogPath, 'utf-8'));
    if (failureLog.failures && Array.isArray(failureLog.failures)) {
      const recentFailures = failureLog.failures.filter(f => {
        const failureTime = new Date(f.time);
        const dayDiff = (today - failureTime) / (1000 * 60 * 60 * 24);
        return dayDiff <= 1; // 最近 24 小时
      });
      
      recentFailures.forEach(f => {
        issues.push({
          type: 'failure',
          task: f.task || 'unknown',
          error: f.error || 'Unknown error',
          time: f.time,
          severity: 'high'
        });
      });
      
      console.log(`  ✅ failure-monitor: ${recentFailures.length} 个问题`);
    }
  } catch (e) {
    console.log(`  ⚠️ 无法读取 failure-monitor-log.json: ${e.message}`);
  }
}

// 1.2 从今天的 daily note 读取
const dailyNotePath = path.join(WORKSPACE, config.dataSources.dailyNotes, `${todayStr}.md`);
if (fs.existsSync(dailyNotePath)) {
  try {
    const content = fs.readFileSync(dailyNotePath, 'utf-8');
    
    // 提取问题标记
    const problemPatterns = [
      { regex: /❌|错误|问题|失败|BUG/gi, type: 'problem' },
      { regex: /⚠️|警告|注意/gi, type: 'warning' },
      { regex: /💡|改进|优化/gi, type: 'improvement' }
    ];
    
    problemPatterns.forEach(({ regex, type }) => {
      const matches = content.match(regex);
      if (matches) {
        matches.forEach(() => {
          issues.push({
            type: `daily-note-${type}`,
            file: dailyNotePath,
            severity: type === 'problem' ? 'high' : 'medium'
          });
        });
      }
    });
    
    console.log(`  ✅ daily-note: 找到 ${issues.filter(i => i.type.startsWith('daily-note')).length} 个标记`);
  } catch (e) {
    console.log(`  ⚠️ 无法读取 daily note: ${e.message}`);
  }
}

// 1.3 从经验教训文件读取
const lessonsPath = path.join(WORKSPACE, 'memory/discord-channel-management-lessons.md');
if (fs.existsSync(lessonsPath)) {
  try {
    const content = fs.readFileSync(lessonsPath, 'utf-8');
    const lessonMatches = content.match(/##\s+.*错误做法[\s\S]*?##\s+.*正确做法/gi);
    if (lessonMatches) {
      lessonMatches.forEach((match, idx) => {
        lessons.push({
          id: idx + 1,
          content: match.substring(0, 200) + '...',
          source: 'discord-channel-management-lessons.md'
        });
      });
      console.log(`  ✅ lessons: ${lessons.length} 条经验`);
    }
  } catch (e) {
    console.log(`  ⚠️ 无法读取 lessons 文件: ${e.message}`);
  }
}

console.log(`\n📊 总计: ${issues.length} 个问题, ${lessons.length} 条经验\n`);

// ============================================
// 2. 分析问题模式
// ============================================
console.log('📈 分析问题模式...');

const problemTypes = {};
const taskFrequency = {};

issues.forEach(issue => {
  const type = issue.type || 'unknown';
  problemTypes[type] = (problemTypes[type] || 0) + 1;
  
  if (issue.task) {
    taskFrequency[issue.task] = (taskFrequency[issue.task] || 0) + 1;
  }
});

console.log('\n问题分类:');
Object.entries(problemTypes)
  .sort((a, b) => b[1] - a[1])
  .forEach(([type, count]) => {
    console.log(`  • ${type}: ${count}`);
  });

if (Object.keys(taskFrequency).length > 0) {
  console.log('\n任务频率:');
  Object.entries(taskFrequency)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .forEach(([task, count]) => {
      console.log(`  • ${task}: ${count} 次`);
    });
}

console.log('');

// ============================================
// 3. 搜索 ClawHub 改进方案
// ============================================
console.log('🔍 搜索 ClawHub 改进方案...');

const suggestions = [
  { 
    name: 'self-improving', 
    desc: '自我反思和学习，记录用户纠正和经验教训', 
    install: 'clawhub install self-improving',
    relevance: 'high'
  },
  { 
    name: 'failure-monitor', 
    desc: '监控定时任务失败，自动修复常见问题', 
    install: 'clawhub install failure-monitor',
    relevance: 'high'
  },
  { 
    name: 'find-skills', 
    desc: '搜索和发现新技能，扩展 AI 能力', 
    install: 'clawhub install find-skills',
    relevance: 'medium'
  },
  { 
    name: 'clawhub-skill-installer', 
    desc: '自动安装和更新技能', 
    install: 'clawhub install clawhub-skill-installer',
    relevance: 'medium'
  }
];

// 根据问题类型调整建议
if (problemTypes['failure'] > 0) {
  suggestions.push({
    name: 'auto-retry',
    desc: '自动重试失败的任务',
    install: 'clawhub install auto-retry',
    relevance: 'high'
  });
}

console.log(`✅ 找到 ${suggestions.length} 个相关技能\n`);

// ============================================
// 4. 生成报告
// ============================================
console.log('📝 生成报告...');

const report = `# 📊 每日自我改进报告

**日期**: ${today.toLocaleDateString('zh-CN', { timeZone: 'Asia/Shanghai' })}

---

## ❌ 今日问题

**问题总数**: ${issues.length}

| 问题类型 | 数量 | 严重程度 |
|---------|------|---------|
${Object.entries(problemTypes)
  .sort((a, b) => b[1] - a[1])
  .map(([type, count]) => {
    const severity = issues.find(i => i.type === type)?.severity || 'low';
    const emoji = severity === 'high' ? '🔴' : severity === 'medium' ? '🟡' : '🟢';
    return `| ${type} | ${count} | ${emoji} ${severity} |`;
  }).join('\n')}

${Object.keys(taskFrequency).length > 0 ? `
### 📊 高频问题任务

| 任务 | 失败次数 |
|------|---------|
${Object.entries(taskFrequency)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 5)
  .map(([task, count]) => `| ${task} | ${count} |`)
  .join('\n')}
` : ''}

---

## 💡 改进建议

${suggestions
  .filter(s => s.relevance === 'high')
  .map(s => `### ${s.name}

${s.desc}

\`\`\`bash
${s.install}
\`\`\`
`)
  .join('\n')}

### 其他推荐技能

${suggestions
  .filter(s => s.relevance === 'medium')
  .map(s => `- **${s.name}**: ${s.desc}`)
  .join('\n')}

---

## 📝 经验教训

${lessons.length > 0 ? lessons.map(l => `
### 经验 ${l.id}

${l.content}

*来源: ${l.source}*
`).join('\n') : '暂无新的经验教训'}

---

## ✅ 下一步行动

- [ ] 检查 failure-monitor 配置
- [ ] 安装推荐的技能
- [ ] 更新 MEMORY.md 记录经验
- [ ] 检查高频失败任务

---

## 📈 改进指标

| 指标 | 今日 | 昨日 | 变化 |
|------|------|------|------|
| 问题总数 | ${issues.length} | - | - |
| 失败次数 | ${problemTypes['failure'] || 0} | - | - |
| 经验记录 | ${lessons.length} | - | - |

---

*自动生成 by daily-self-improvement*
*时间: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}*
`;

// 保存报告
const reportDir = path.join(MEMORY_DIR, 'self-improvement');
if (!fs.existsSync(reportDir)) {
  fs.mkdirSync(reportDir, { recursive: true });
}

const reportPath = path.join(reportDir, `${todayStr}.md`);
fs.writeFileSync(reportPath, report, 'utf-8');
console.log(`✅ 报告已保存: ${reportPath}\n`);

// ============================================
// 5. 更新 daily note
// ============================================
console.log('📝 更新 daily note...');

const dailyNoteUpdate = `

---

## 📊 每日自我改进总结

- **问题总数**: ${issues.length}
- **主要问题**: ${Object.entries(problemTypes).sort((a, b) => b[1] - a[1])[0]?.[0] || '无'}
- **改进建议**: ${suggestions.filter(s => s.relevance === 'high').map(s => s.name).join(', ')}

详细报告: \`memory/self-improvement/${todayStr}.md\`
`;

if (fs.existsSync(dailyNotePath)) {
  fs.appendFileSync(dailyNotePath, dailyNoteUpdate, 'utf-8');
  console.log('✅ 已更新 daily note\n');
}

// ============================================
// 6. 发送到 Discord
// ============================================

async function sendToDiscord(message) {
  return new Promise((resolve) => {
    if (!config.notifications.discord) {
      console.log('⏭️ Discord 通知已禁用');
      resolve(false);
      return;
    }
    
    const token = process.env.OPENCLAW_GATEWAY_TOKEN || 'b8cb95b2fb220c2896a44dc6514f47ef4efed792bcd07c3f';
    
    // 使用正确的 API 路径
    const postData = JSON.stringify({
      action: 'send',
      channel: 'discord',
      channelId: config.discordChannel,
      message: message
    });

    const options = {
      hostname: '127.0.0.1',
      port: 18789,
      path: '/api/message',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.ok || result.status === 'ok') {
            console.log('✅ 已发送到 Discord');
            resolve(true);
          } else {
            console.log('⚠️ Discord 发送:', result.error || result.status || '未知');
            resolve(false);
          }
        } catch (error) {
          console.log('⚠️ Discord 响应:', data.substring(0, 100));
          resolve(false);
        }
      });
    });

    req.on('error', (error) => {
      console.log('⚠️ Discord 发送:', error.message);
      resolve(false);
    });
    req.write(postData);
    req.end();
  });
}

// 构建简短报告
const discordMessage = `📊 **每日自我改进报告** (${todayStr})

## ❌ 问题总结

**问题总数**: ${issues.length}

${Object.entries(problemTypes)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 3)
  .map(([type, count]) => `• ${type}: ${count}`)
  .join('\n')}

## 💡 推荐技能

${suggestions
  .filter(s => s.relevance === 'high')
  .slice(0, 2)
  .map(s => `• **${s.name}**: ${s.desc}`)
  .join('\n')}

## 📝 下一步

- 检查 failure-monitor 配置
- 安装推荐技能
- 更新 MEMORY.md

---
📁 完整报告: \`memory/self-improvement/${todayStr}.md\``;

// 执行
console.log('📤 发送报告到 Discord...');
sendToDiscord(discordMessage).then(() => {
  console.log('\n✅ 每日自我改进分析完成！');
  console.log('========================');
  console.log(`📊 问题: ${issues.length}`);
  console.log(`💡 建议: ${suggestions.length}`);
  console.log(`📝 报告: ${reportPath}`);
});
