#!/usr/bin/env node
/**
 * 每日记忆 AI 整理器
 * 读取原始记忆文件 → AI 分析提炼 → 生成结构化记忆（保留原始备份）
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 渠道配置
const CHANNEL_CONFIG = {
  feishu: { dir: 'feishu', label: '飞书' },
  webui: { dir: 'webui', label: 'WebUI' },
  dingtalk: { dir: 'dingtalk', label: '钉钉' },
  weixin: { dir: 'weixin', label: '微信' },
  qqbot: { dir: 'qqbot', label: 'QQ' }
};

// 配置
const CONFIG = {
  workspaceDir: process.env.WORKSPACE_DIR || '/home/admin/.openclaw/workspace',
  memoryDir: process.env.WORKSPACE_DIR 
    ? path.join(process.env.WORKSPACE_DIR, 'memory')
    : '/home/admin/.openclaw/workspace/memory',
  backupDir: process.env.WORKSPACE_DIR 
    ? path.join(process.env.WORKSPACE_DIR, 'memory', 'raw-backup')
    : '/home/admin/.openclaw/workspace/memory/raw-backup'
};

function getTodayStr() {
  const now = new Date();
  return now.toISOString().split('T')[0];
}

function getYesterdayStr() {
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  return yesterday.toISOString().split('T')[0];
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function safeRead(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf-8');
  } catch (e) {
    return null;
  }
}

/**
 * 调用 AI 分析对话，生成结构化记忆
 */
async function refineMemory(rawContent, channel, date) {
  const truncatedContent = rawContent.substring(0, 12000);
  
  const prompt = `你是学习秘书，负责整理${channel}渠道的每日学习记录。

【原始对话记录】
${truncatedContent}

【任务】
分析以上对话，提取结构化内容：
1. **主题**（1-5 个）- 今天主要聊了哪些话题，每个主题的核心内容。注意：晨间启动检查等系统行为不是对话主题，应合并或跳过。
2. **决策**（0-5 个）- 做了什么重要选择，选项对比，最终决策及理由。⚠️ 保留原始对话中的完整考虑因素，不要过度压缩。
3. **踩坑**（0-5 个）- 遇到了什么问题，怎么解决的，教训是什么
4. **新概念**（0-5 个）- 学到了什么新术语/新方法。⚠️ 提取所有技术术语，不限于用户明确定义的。
5. **金句/洞见**（0-5 条）- ⚠️ 必须是有方法论价值的洞见，不是对话引用。例如"配置写在脚本里，自包含更易维护"这种有方法论价值的算金句；"你问得对：这个改动其实不难"这种对话引用不算。

【输出格式】只返回 JSON，不要其他文字：
{
  "topics": [
    {
      "title": "主题名称",
      "description": "一句话说明",
      "keyPoints": ["要点 1", "要点 2"],
      "tasks": {"P0": [], "P1": [], "P2": []}
    }
  ],
  "decisions": [
    {
      "decision": "决策点",
      "options": [
        {"option": "选项 A", "factors": "考虑因素", "result": "选/不选"}
      ]
    }
  ],
  "pitfalls": [
    {
      "problem": "问题描述",
      "solution": "解决方案",
      "lesson": "教训"
    }
  ],
  "concepts": [
    {
      "term": "术语",
      "definition": "定义",
      "scenario": "应用场景"
    }
  ],
  "insights": ["金句 1", "金句 2"]
}
`;

  try {
    // 方式 4：直接调用 dashscope API（cron 环境可用）
    const apiKey = 'REDACTED-SECRET';
    const apiUrl = 'https://coding.dashscope.aliyuncs.com/v1/chat/completions';
    
    const requestBody = {
      model: 'kimi-k2.5',
      messages: [
        { role: 'system', content: '你是一个学习秘书，负责整理每日学习记录。只返回 JSON 格式，不要其他文字。' },
        { role: 'user', content: prompt }
      ],
      temperature: 0.7,
      max_tokens: 8192
    };
    
    const curlCmd = `curl -s -X POST '${apiUrl}' \
      -H 'Authorization: Bearer ${apiKey}' \
      -H 'Content-Type: application/json' \
      -d '${JSON.stringify(requestBody).replace(/'/g, "'\\''")}'`;
    
    const result = execSync(curlCmd, {
      encoding: 'utf-8',
      timeout: 120000,
      maxBuffer: 100 * 1024 * 1024
    });
    
    const response = JSON.parse(result);
    const content = response.choices?.[0]?.message?.content || '';
    
    // 提取 JSON
    const jsonMatch = content.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      return JSON.parse(jsonMatch[0]);
    }
    
    console.error('⚠️ 未找到 JSON，返回空结构');
    return { topics: [], decisions: [], pitfalls: [], concepts: [], insights: [] };
  } catch (e) {
    console.error('❌ AI 分析失败:', e.message);
    return { topics: [], decisions: [], pitfalls: [], concepts: [], insights: [] };
  }
}

/**
 * 生成结构化记忆文件
 */
function generateStructuredMemory(channel, date, analysis, rawContent) {
  const channelName = CHANNEL_CONFIG[channel]?.label || channel;
  
  let content = `# 记忆档案 - ${date}

**渠道：** ${channelName}  
**日期：** ${date}  
**整理时间：** ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}  
**原始记录：** ${date}.raw.md

---

## 📊 今日概览

| 类型 | 数量 |
|------|------|
| 主题 | ${analysis.topics.length} 个 |
| 决策 | ${analysis.decisions.length} 个 |
| 踩坑 | ${analysis.pitfalls.length} 个 |
| 新概念 | ${analysis.concepts.length} 个 |
| 金句 | ${analysis.insights.length} 条 |

---

## 📚 核心主题

${analysis.topics.length > 0 ? analysis.topics.map((topic, i) => `### ${i + 1}. ${topic.title}

**说明：** ${topic.description}

**要点：**
${topic.keyPoints && topic.keyPoints.length > 0 ? topic.keyPoints.map(kp => `- ${kp}`).join('\n') : '- 暂无详细记录'}

---
`).join('\n') : '*今日无明确主题记录*'}

## 📋 重要决策

${analysis.decisions.length > 0 ? analysis.decisions.map((d, i) => `### ${i + 1}. ${d.decision}

| 选项 | 考虑因素 | 结果 |
|------|---------|------|
${d.options.map(o => `| ${o.option} | ${o.factors} | ${o.result} |`).join('\n')}

---
`).join('\n') : '*今日无重要决策*'}

## ⚠️ 踩坑记录

${analysis.pitfalls.length > 0 ? analysis.pitfalls.map((p, i) => `### ${i + 1}. ${p.problem}

**解决方案：** ${p.solution || '暂无'}

**教训：** ${p.lesson || '暂无'}

---
`).join('\n') : '*今日无踩坑记录*'}

## 🧠 新概念

${analysis.concepts.length > 0 ? analysis.concepts.map((c, i) => `### ${i + 1}. ${c.term}

**定义：** ${c.definition || '暂无'}

**应用场景：** ${c.scenario || '暂无'}

---
`).join('\n') : '*今日无新概念*'}

## 💬 金句 / 洞见

${analysis.insights.length > 0 ? analysis.insights.map(insight => `> "${insight}"`).join('\n\n') : '*今日无金句*'}

---

## 📎 原始对话记录

<details>
<summary>点击查看原始对话（未整理）</summary>

\`\`\`
${rawContent.substring(0, 5000)}
${rawContent.length > 5000 ? '\n... (省略后续内容)' : ''}
\`\`\`

</details>

---

*💃 金银 Planet · 自我提升部*
`;

  return content;
}

/**
 * 处理单个渠道的记忆整理
 */
async function processChannel(channel, memoryDir, date) {
  const rawFile = path.join(memoryDir, `${date}.md`);
  const rawContent = safeRead(rawFile);
  
  if (!rawContent) {
    console.error(`[${channel}] 未找到记忆文件：${rawFile}`);
    return false;
  }
  
  console.error(`[${channel}] 找到记忆文件，共 ${rawContent.length} 字符`);
  
  // 备份原始记录
  ensureDir(CONFIG.backupDir);
  const backupFile = path.join(CONFIG.backupDir, `${date}-${channel}.raw.md`);
  fs.writeFileSync(backupFile, rawContent, 'utf-8');
  console.error(`[${channel}] 原始记录已备份：${backupFile}`);
  
  // AI 分析提炼
  console.error(`[${channel}] 正在调用 AI 分析...`);
  const analysis = await refineMemory(rawContent, channel, date);
  console.error(`[${channel}] AI 分析完成：${analysis.topics.length} 个主题，${analysis.decisions.length} 个决策`);
  
  // 生成结构化记忆
  const structuredContent = generateStructuredMemory(channel, date, analysis, rawContent);
  fs.writeFileSync(rawFile, structuredContent, 'utf-8');
  console.error(`[${channel}] ✅ 结构化记忆已生成：${rawFile}`);
  
  return true;
}

/**
 * 主函数
 */
async function main() {
  const date = getTodayStr(); // 处理当天的记忆（cron 23:59 执行，当天已近结束）
  console.error('=== 每日记忆 AI 整理 ===');
  console.error(`处理日期：${date}`);
  console.error('');
  
  let hasContent = false;
  
  for (const [chKey, chConfig] of Object.entries(CHANNEL_CONFIG)) {
    const fullDir = path.join(CONFIG.memoryDir, chConfig.dir);
    console.error(`【${chConfig.label} 渠道】`);
    if (await processChannel(chKey, fullDir, date)) {
      hasContent = true;
    }
    console.error('');
  }
  
  if (!hasContent) {
    console.error('昨天没有记忆记录，跳过整理');
    process.exit(0);
  }
  
  console.error('✅ 每日记忆整理完成');
}

// 执行
if (require.main === module) {
  main().catch(e => {
    console.error('❌ 错误:', e);
    process.exit(1);
  });
}

module.exports = { refineMemory, generateStructuredMemory, processChannel };
