#!/usr/bin/env node
/**
 * generate-exam-v2.js
 * 每周考题生成器 V2 — AI 智能出题，直接输出 Markdown
 */
const http = require('http');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  API_KEY: process.env.EXAM_API_KEY || 'sk-CHWajNDqg9gT1NQRCYJzY2KpsD7PZlMDmeHC9xV8XtAdZWV8',
  API_HOST: '219.152.187.110', API_PORT: 13001,
  API_PATH: '/v1/chat/completions', MODEL: 'deepseek-v4-pro',
  MAX_TOKENS: 16384, TEMPERATURE: 0.7,
  MAX_RETRIES: 3, RETRY_DELAY_MS: 2000, TIMEOUT_MS: 300000,
};

const DATA_FILE = '/home/admin/.openclaw/workspace/memory/exam-questions/last-week-data.json';
const EXAMS_DIR = '/home/admin/.openclaw/workspace/memory/exam-questions';

function httpPost(options, data) {
  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
      let body = ''; res.on('data', c => body += c);
      res.on('end', () => { try { resolve(JSON.parse(body)); } catch(e) { reject(new Error(e.message)); } });
    });
    req.setTimeout(CONFIG.TIMEOUT_MS, () => { req.destroy(); reject(new Error('timeout')); });
    req.on('error', reject);
    req.write(JSON.stringify(data)); req.end();
  });
}

async function callAI(messages, retries = 0) {
  try {
    const r = await httpPost({
      hostname: CONFIG.API_HOST, port: CONFIG.API_PORT, path: CONFIG.API_PATH, method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${CONFIG.API_KEY}` },
    }, { model: CONFIG.MODEL, messages, max_tokens: CONFIG.MAX_TOKENS, temperature: CONFIG.TEMPERATURE });
    return r?.choices?.[0]?.message?.content || '';
  } catch(e) {
    if (retries < CONFIG.MAX_RETRIES) {
      console.error(`⚠️ 重试 ${retries+1}: ${e.message}`);
      await new Promise(r => setTimeout(r, CONFIG.RETRY_DELAY_MS));
      return callAI(messages, retries+1);
    }
    throw e;
  }
}

async function main() {
  if (!fs.existsSync(DATA_FILE)) { console.error('❌ 无数据'); process.exit(1); }
  const d = JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
  const s = d.stats || {}, m = d.meta || {};

  const topics = (d.topics||[]).map(t => `- ${t.title}${t.detail ? ': '+t.detail : ''}`).join('\n');
  const pits = (d.pitfalls||[]).map(p => `- ${p.problem} | 解决:${p.solution||'?'} | 教训:${p.lesson||'?'}`).join('\n');
  const concs = (d.concepts||[]).map(c => `- ${c.term} | ${c.definition||''} | ${c.scenario||''}`).join('\n');
  const secs = (d.sessionSections||[]).slice(0,12).map(sec => {
    const preview = sec.content.substring(0, 800).replace(/\n/g, ' ');
    return `- [${sec.channel}] ${sec.date} ${sec.title}: ${preview}`;
  }).join('\n');

  const isSparse = s.activeDays < 3 || s.totalTopics < 5;
  const extraRule = isSparse
    ? `\n⚠️ 本周学习内容稀疏（${s.activeDays}天/${s.totalTopics}主题），请生成 12~15 道基于学习内容的题 + 5~8 道 AI 扩展题。AI 扩展题主题：提示词工程、Agent 架构、AI 安全、AI 近期进展。AI 扩展题标注 [AI扩展]。`
    : '\n本周学习内容充足，全部基于学习内容出题。';

  const prompt = `你是学习考官，基于以下学习记录生成 20 道考题。直接输出 Markdown，不要 JSON。

## 出题规则
- 总 20 道：15 单选 + 5 多选
- 禁止填空题、实操题、纯记忆题（如"XX是多少"）
- 禁止套模板——每道题必须考察不同知识点，干扰项必须看似合理
- 优先从决策过程、踩坑、新概念中出题
- 每道题带 4 个选项（单选）或 4 个选项（多选）
- 答案和解析折叠在 <details> 中${extraRule}

## 上周数据
活跃 ${s.activeDays} 天 | 主题 ${s.totalTopics} | 踩坑 ${s.totalPitfalls} | 概念 ${s.totalConcepts}

### 主题
${topics || '(无)'}

### 踩坑
${pits || '(无)'}

### 概念
${concs || '(无)'}

### 对话记录
${secs || '(无)'}

## 输出格式
📝 第 ${m.weekNum} 周学习测试
📚 测试范围：${m.startStr} ~ ${m.endStr}
📊 题目数量：20 道（15 单选 + 5 多选）
⏰ 截止时间：下周二 24:00
---
## 单选题（15 道）
（15 道独立单选题，带选项 A/B/C/D）
---
## 多选题（5 道）
（5 道独立多选题，带选项 A/B/C/D 等）
---
<details>
<summary>📎 答案与解析</summary>
（所有题的答案和解析）
</details>
---
直接输出以上内容，不要额外解释。`;

  console.error(`📝 Prompt: ${prompt.length} 字符s → AI...`);
  const content = await callAI([{ role: 'user', content: prompt }]);

  const weekLabel = `${m.year || new Date().getFullYear()}-W${m.weekNum}`;
  const outFile = path.join(EXAMS_DIR, `${weekLabel}-exam.md`);
  fs.mkdirSync(EXAMS_DIR, { recursive: true });
  fs.writeFileSync(outFile, content, 'utf-8');
  console.error(`✅ ${outFile}`);
  console.log(content);
}

main().catch(e => { console.error(`❌ ${e.message}`); process.exit(1); });