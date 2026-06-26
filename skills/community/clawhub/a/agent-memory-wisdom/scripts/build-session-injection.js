#!/usr/bin/env node
/**
 * 会话注入构建器
 * 会话开始前自动组装上下文注入
 *
 * 用法: node build-session-injection.js
 * 输出: 注入内容文本（JSON格式）
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const SNAPSHOT_PATH = path.join(WORKSPACE, 'memory/SNAPSHOT.md');
const BUFFER_PATH = path.join(WORKSPACE, 'memory/工作缓冲区.md');

function readFile(p) {
  try { return fs.readFileSync(p, 'utf8'); } catch { return null; }
}

function extractKeyInfo(snapshot) {
  const lines = snapshot.split('\n').filter(l => l.trim());
  const info = {
    用户信息: [],
    当前任务: [],
    最近结论: [],
    待办: []
  };

  let currentSection = null;
  lines.forEach(line => {
    if (line.includes('📌') && line.includes('信息')) currentSection = '用户信息';
    else if (line.includes('📋') && line.includes('当前任务')) currentSection = '当前任务';
    else if (line.includes('🧠') && line.includes('最近')) currentSection = '最近结论';
    else if (line.includes('待办')) currentSection = '待办';
    else if (line.startsWith('- ') && currentSection) {
      info[currentSection].push(line.slice(2));
    }
  });

  return info;
}

function buildInjection() {
  const snapshot = readFile(SNAPSHOT_PATH);
  const buffer = readFile(BUFFER_PATH);

  if (!snapshot) {
    console.log(JSON.stringify({ error: 'SNAPSHOT not found', injection: '' }));
    return;
  }

  const info = extractKeyInfo(snapshot);

  const injection = `【当前会话上下文】

【用户】${info.用户信息.join(' | ') || '未知'}

【进行中】${info.当前任务.join(', ') || '无'}

【待办】${info.待办.join(', ') || '无'}

【最近关键结论】
${info.最近结论.slice(0, 5).join('\n')}

${buffer ? '【工作缓冲】' + buffer.slice(0, 500) + '...' : ''}
`;

  console.log(JSON.stringify({
    injection: injection.trim(),
    timestamp: new Date().toISOString(),
    sources: { snapshot: !!snapshot, buffer: !!buffer }
  }, null, 2));
}

buildInjection();
