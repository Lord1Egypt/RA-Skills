#!/usr/bin/env node
/**
 * 每日记忆生成器
 * 基于飞书和 Web UI 的对话，AI 分析生成结构化记忆
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { getTodayMessages, formatMessages } = require('./parse-session');

// 渠道配置映射
const CHANNEL_CONFIG = {
  feishu: { dir: 'feishu', label: '飞书' },
  webui: { dir: 'webui', label: 'WebUI' },
  dingtalk: { dir: 'dingtalk', label: '钉钉' },
  weixin: { dir: 'weixin', label: '微信' },
  qqbot: { dir: 'qqbot', label: 'QQ' }
};

// 配置
const CONFIG = {
  memoryDir: process.env.WORKSPACE_DIR 
    ? path.join(process.env.WORKSPACE_DIR, 'memory')
    : '/home/admin/.openclaw/workspace/memory'
};

function getTodayStr() {
  const now = new Date();
  return now.toISOString().split('T')[0];
}

function getNowStr() {
  const now = new Date();
  return now.toTimeString().split(' ')[0].substring(0, 5);
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

async function analyzeConversation(formattedText) {
  const truncatedText = formattedText.substring(0, 6000);
  
  const prompt = `你是学习秘书，负责整理今天的学习记录。

【今天的对话】
${truncatedText}

【任务】
分析以上对话，提取：
1. 主题（1-3 个）- 今天主要聊了哪些话题
2. 决策（0-3 个）- 做了什么重要选择
3. 踩坑（0-3 个）- 遇到了什么问题，怎么解决的
4. 金句（0-3 条）- 用户的原话

【输出格式】只返回 JSON，不要其他文字：
{"themes":[{"title":"...","description":"..."}],"decisions":[{"theme":"...","options":[{"option":"...","consideration":"...","result":"..."}]}],"pitfalls":[{"problem":"...","solution":"...","lesson":"..."}],"golden_quotes":["..."]}
`;

  try {
    const tempFile = `/tmp/daily-memory-prompt-${Date.now()}.txt`;
    fs.writeFileSync(tempFile, prompt, 'utf-8');
    
    const result = execSync(`openclaw agent --agent main --message "$(cat '${tempFile}')" --local 2>&1`, {
      encoding: 'utf-8',
      timeout: 120000,
      maxBuffer: 100 * 1024 * 1024
    });
    
    try { fs.unlinkSync(tempFile); } catch (e) {}
    
    console.error('DEBUG: result length =', result.length);
    
    const jsonMatch = result.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      const parsed = JSON.parse(jsonMatch[0]);
      console.error('DEBUG: parsed themes =', parsed.themes?.length || 0);
      
      return {
        topics: (parsed.themes || []).map(t => ({ title: t.title, tasks: { P0: [], P1: [], P2: [] } })),
        decisions: (parsed.decisions || []).flatMap(d => d.options.map(o => ({ decision: d.theme, choice: o.result, reason: o.consideration }))),
        pitfalls: (parsed.pitfalls || []).map(p => ({ problem: p.problem, solution: p.solution, lesson: p.lesson })),
        insights: parsed.golden_quotes || [],
        concepts: []
      };
    }
    
    console.error('DEBUG: No JSON found in result');
    return { topics: [], decisions: [], pitfalls: [], concepts: [], insights: [] };
  } catch (e) {
    console.error('AI 分析失败:', e.message);
    return { topics: [], decisions: [], pitfalls: [], concepts: [], insights: [] };
  }
}

function generateMemoryContent(channel, date, analysis, rawMessages) {
  const now = getNowStr();
  
  let content = `# ${date} 记忆档案

**渠道：** ${channel === 'feishu' ? '飞书' : 'Web UI'}  
**日期：** ${date}  
**创建时间：** ${now}

---

## 今日概览

- **主题数：** ${analysis.topics.length} 个
- **决策数：** ${analysis.decisions.length} 个
- **踩坑数：** ${analysis.pitfalls.length} 个
- **新概念：** ${analysis.concepts.length} 个
- **金句：** ${analysis.insights.length} 条

---

`;

  if (analysis.topics.length > 0) {
    content += `## 主题\n\n`;
    analysis.topics.forEach((topic, i) => {
      content += `### ${topic.title}\n\n`;
    });
    content += `---\n\n`;
  }

  if (analysis.decisions.length > 0) {
    content += `## 决策\n\n`;
    analysis.decisions.forEach((d, i) => {
      content += `### 决策${i + 1}：${d.decision}\n`;
      content += `- **选择：** ${d.choice}\n`;
      content += `- **理由：** ${d.reason}\n\n`;
    });
    content += `---\n\n`;
  }

  if (analysis.pitfalls.length > 0) {
    content += `## 踩坑\n\n`;
    analysis.pitfalls.forEach((p, i) => {
      content += `### 问题${i + 1}：${p.problem}\n`;
      if (p.solution) content += `- **解决方案：** ${p.solution}\n`;
      if (p.lesson) content += `- **教训：** ${p.lesson}\n`;
      content += '\n';
    });
    content += `---\n\n`;
  }

  if (analysis.insights.length > 0) {
    content += `## 金句\n\n`;
    analysis.insights.forEach((insight, i) => {
      content += `> "${insight}"\n\n`;
    });
    content += `---\n\n`;
  }

  content += `## 原始对话\n\n`;
  content += `<details>\n<summary>点击查看原始对话</summary>\n\n\`\`\`\n`;
  content += rawMessages.substring(0, 2000);
  if (rawMessages.length > 2000) content += '\n... (省略后续内容)';
  content += '\n```\n\n';
  content += `</details>\n\n---\n\n*💃 金银 Planet · 自我提升部*\n`;

  return content;
}

async function processChannel(channelKey, channelConfig, date, messages) {
  if (messages.length === 0) {
    console.error(`${channelConfig.label}：今天没有对话`);
    return false;
  }
  
  console.error(`${channelConfig.label}：找到 ${messages.length} 条消息`);
  const formatted = formatMessages(messages);
  
  console.error(`正在调用 AI 分析 ${channelConfig.label} 对话...`);
  const analysis = await analyzeConversation(formatted);
  
  const memoryContent = generateMemoryContent(channelKey, date, analysis, formatted);
  const memoryDir = path.join(CONFIG.memoryDir, channelConfig.dir);
  ensureDir(memoryDir);
  const memoryFile = path.join(memoryDir, `${date}.md`);
  fs.writeFileSync(memoryFile, memoryContent, 'utf-8');
  
  console.error(`✅ ${channelConfig.label} 记忆已生成：${memoryFile}`);
  return true;
}

async function main() {
  console.error('=== 每日记忆生成 ===\n');
  
  const channels = getTodayMessages();
  let hasContent = false;
  
  for (const [chKey, msgs] of Object.entries(channels)) {
    const chConfig = CHANNEL_CONFIG[chKey] || { dir: chKey, label: chKey };
    console.error(`【${chConfig.label} 渠道】`);
    if (await processChannel(chKey, chConfig, getTodayStr(), msgs)) hasContent = true;
  }
  
  if (!hasContent) {
    console.error('\n今天没有对话记录');
    process.exit(1);
  }
  
  console.error('\n✅ 每日记忆生成完成');
}

if (require.main === module) {
  main().catch(e => {
    console.error('错误:', e);
    process.exit(1);
  });
}

module.exports = { processChannel, getTodayStr };
