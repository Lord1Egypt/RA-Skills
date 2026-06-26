#!/usr/bin/env node
'use strict';
// planning-with-files: Session start hook — Node.js port of session-start.sh

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { findActivePlanFile } = require('./planning-paths');
const { appendLog, cleanupLogs } = require('./session-log');

let input = '';
process.stdin.resume();
process.stdin.setEncoding('utf8');
process.stdin.on('data', d => (input += d));
process.stdin.on('end', () => {
  try { run(); } catch { process.stdout.write('{}'); }
});

function run() {
  // 解析输入获取 sessionId
  let sessionId = '';
  try {
    const data = JSON.parse(input);
    sessionId = data.sessionId || '';
  } catch {}

  // 初始化 AGENTS.md 门控状态（空 = 未读）+ 代码编辑追踪文件
  const GATE_FILE = path.join('.github', 'session-logs', '.agents-gate');
  const EDITS_FILE = path.join('.github', 'session-logs', '.code-edits');
  try {
    const gateDir = path.dirname(GATE_FILE);
    if (!fs.existsSync(gateDir)) fs.mkdirSync(gateDir, { recursive: true });
    fs.writeFileSync(GATE_FILE, '', 'utf8');
    fs.writeFileSync(EDITS_FILE, '', 'utf8');
  } catch {}

  // 记录 SessionStart 到审计日志
  const planFile = findActivePlanFile();
  appendLog(sessionId, 'SessionStart', {
    活跃计划: planFile ? path.dirname(planFile).replace(/\\/g, '/') : '无',
  });

  // 清理过期日志文件
  cleanupLogs();

  const SKILL_DIR = '.github/skills/planning-with-files';
  let context = '';

  if (planFile) {
    const planDir = path.dirname(planFile);
    // Try session catchup via Python
    const catchupScript = path.join(SKILL_DIR, 'scripts', 'session-catchup.py');
    if (fs.existsSync(catchupScript)) {
      for (const py of ['python3', 'python']) {
        try {
          context = execFileSync(py, [catchupScript, process.cwd(), planDir], {
            encoding: 'utf8', timeout: 10000, windowsHide: true,
            stdio: ['pipe', 'pipe', 'pipe'],
          }).trim();
          if (context) break;
        } catch {}
      }
    }
    // Fallback: read plan header
    if (!context) {
      try {
        context = fs.readFileSync(planFile, 'utf8').split('\n').slice(0, 5).join('\n');
      } catch {}
    }
  } else {
    // No plan — inject SKILL.md
    const skillPath = path.join(SKILL_DIR, 'SKILL.md');
    if (fs.existsSync(skillPath)) {
      try { context = fs.readFileSync(skillPath, 'utf8'); } catch {}
    }
  }

  if (!context) { process.stdout.write('{}'); return; }

  // 注入趋势分析（高频错误类别摘要）
  const trendContext = getTrendAnalysis();
  if (trendContext) {
    context += '\n\n---\n' + trendContext;
  }

  // 注入最近的教训记录
  const lessonsContext = getRecentLessons(10);
  if (lessonsContext) {
    context += '\n\n---\n' + lessonsContext;
  }

  process.stdout.write(JSON.stringify({
    hookSpecificOutput: { hookEventName: 'SessionStart', additionalContext: context },
  }));
}

/** 读取 .github/lessons-learned.md 最近 N 条教训 */
function getRecentLessons(count) {
  const lessonsFile = '.github/lessons-learned.md';
  if (!fs.existsSync(lessonsFile)) return '';
  try {
    const content = fs.readFileSync(lessonsFile, 'utf8');
    const sections = content.split(/(?=^## \d{4}-)/m).slice(1, count + 1);
    if (sections.length === 0) return '';
    return `[lessons-learned] 最近 ${sections.length} 条验证教训（避免重犯）：\n` + sections.join('');
  } catch {
    return '';
  }
}

/** 分析最近 7 天的教训趋势，返回高频错误类别摘要 */
function getTrendAnalysis() {
  const lessonsFile = '.github/lessons-learned.md';
  if (!fs.existsSync(lessonsFile)) return '';
  try {
    const content = fs.readFileSync(lessonsFile, 'utf8');
    const sections = content.split(/(?=^## \d{4}-)/m).slice(1);
    if (sections.length === 0) return '';

    const cutoff = Date.now() - 7 * 86400000;
    const categoryCounts = {};
    const agentCounts = {};

    for (const sec of sections) {
      // 解析日期：## 2026-04-28 12:34:56 | category1, category2
      const headerMatch = sec.match(/^## (\d{4}-\d{2}-\d{2}) [\d:]+ \| (.+)/);
      if (!headerMatch) continue;

      const entryDate = new Date(headerMatch[1] + 'T00:00:00').getTime();
      if (entryDate < cutoff) break; // 条目按时间倒序，遇到超期即停

      const cats = headerMatch[2].split(',').map(c => c.trim()).filter(Boolean);
      for (const cat of cats) {
        categoryCounts[cat] = (categoryCounts[cat] || 0) + 1;
      }

      // 解析 Agent
      const agentMatch = sec.match(/\*\*Agent\*\*: (.+)/);
      if (agentMatch) {
        const agent = agentMatch[1].trim();
        agentCounts[agent] = (agentCounts[agent] || 0) + 1;
      }
    }

    const totalErrors = Object.values(categoryCounts).reduce((a, b) => a + b, 0);
    if (totalErrors === 0) return '';

    // 按频次降序排列
    const topCategories = Object.entries(categoryCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([cat, count]) => `${cat}(${count}次)`)
      .join(', ');

    const topAgents = Object.entries(agentCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3)
      .map(([agent, count]) => `${agent}(${count}次)`)
      .join(', ');

    let summary = `[trend] ⚡ 近7天验证失败 ${totalErrors} 次 — 高频问题: ${topCategories}`;
    if (topAgents) summary += ` | 涉及 Agent: ${topAgents}`;
    summary += '\n请在开发中重点关注上述类别，避免重犯。';
    return summary;
  } catch {
    return '';
  }
}
