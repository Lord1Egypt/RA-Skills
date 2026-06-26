#!/usr/bin/env node
/**
 * generate-summary-v2.js
 * 每周学习汇总生成器 V2 — AI 智能生成周报
 * 替代原来的 shell 模板拼接
 */
const http = require('http');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  API_KEY: process.env.EXAM_API_KEY || 'sk-CHWajNDqg9gT1NQRCYJzY2KpsD7PZlMDmeHC9xV8XtAdZWV8',
  API_HOST: '219.152.187.110', API_PORT: 13001,
  API_PATH: '/v1/chat/completions', MODEL: 'deepseek-v4-pro',
  MAX_TOKENS: 8192, TEMPERATURE: 0.7,
  MAX_RETRIES: 3, RETRY_DELAY_MS: 2000, TIMEOUT_MS: 180000,
};

const WORKSPACE = '/home/admin/.openclaw/workspace';
const DATA_FILE = path.join(WORKSPACE, 'memory/exam-questions/last-week-data.json');

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

async function callAI(prompt, retries = 0) {
  try {
    const r = await httpPost({
      hostname: CONFIG.API_HOST, port: CONFIG.API_PORT, path: CONFIG.API_PATH, method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${CONFIG.API_KEY}` },
    }, { model: CONFIG.MODEL, messages: [{ role: 'user', content: prompt }], max_tokens: CONFIG.MAX_TOKENS, temperature: CONFIG.TEMPERATURE });
    return r?.choices?.[0]?.message?.content || '';
  } catch(e) {
    if (retries < CONFIG.MAX_RETRIES) { await new Promise(r => setTimeout(r, CONFIG.RETRY_DELAY_MS)); return callAI(prompt, retries+1); }
    throw e;
  }
}

async function main() {
  if (!fs.existsSync(DATA_FILE)) { console.error('no data'); process.exit(1); }
  const d = JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
  const s = d.stats || {}, m = d.meta || {};

  // Build prompt with raw data
  const topicsStr = (d.topics||[]).map(t => `- ${t.title}${t.detail ? ': '+t.detail : ''}`).join('\n');
  const pitStr = (d.pitfalls||[]).map(p => `- ${p.problem} | 解决: ${p.solution||'?'} | 教训: ${p.lesson||'?'}`).join('\n');
  const concStr = (d.concepts||[]).map(c => `- ${c.term} | ${c.definition||''} | ${c.scenario||''}`).join('\n');
  const quoteStr = (d.quotes||[]).slice(0,10).map(q => `> "${q}"`).join('\n');
  const secStr = (d.sessionSections||[]).slice(0,15).map(sec => `- [${sec.channel}] ${sec.date}: ${sec.title}`).join('\n');

  const prompt = `你是 Elon，自我提升部经理。基于以下上周学习数据生成学习周报（纯 Markdown，不要 JSON）。

## 数据
活跃 ${s.activeDays} 天，${s.totalTopics} 主题，${s.totalPitfalls} 踩坑，${s.totalConcepts} 概念，${s.totalQuotes} 金句

### 主题
${topicsStr || '(无)'}

### 决策
${(d.decisions||[]).map(dd => `- ${dd.decision} → ${dd.choice} | 理由: ${dd.reason||'?'}`).join('\n') || '(无)'}

### 踩坑
${pitStr || '(无)'}

### 概念
${concStr || '(无)'}

### 金句
${quoteStr || '(无)'}

### 对话记录
${secStr || '(无)'}

## 要求
生成 Markdown 周报，结构：
# 第${m.weekNum}周学习周报（${m.startStr}~${m.endStr}）
## 📊 本周概览（表格）
## 📚 核心主题（每个一段，含决策/数据/踩坑）
## 📋 本周重要决策（表格）
## ⚠️ 本周踩坑汇总（表格）
## 🧠 本周新概念（表格）
## 💬 本周金句
## 🔮 Elon 经理点评（亮点/问题/P0P1P2建议）

${s.activeDays < 3 ? '⚠️ 本周内容稀疏，不注水，简短如实写。' : ''}
直接输出 Markdown，不要代码块包裹。`;

  console.error(`📝 Prompt: ${prompt.length} 字符，调用 AI...`);
  const content = await callAI(prompt);
  
  const outDir = path.join(WORKSPACE, 'memory/learning-summaries');
  fs.mkdirSync(outDir, { recursive: true });
  const outFile = path.join(outDir, `${m.year || new Date().getFullYear()}-W${m.weekNum}-summary.md`);
  fs.writeFileSync(outFile, content, 'utf-8');
  console.error(`✅ 周报: ${outFile}`);
  console.log(content);
}

main().catch(e => { console.error(`❌ ${e.message}`); process.exit(1); });
