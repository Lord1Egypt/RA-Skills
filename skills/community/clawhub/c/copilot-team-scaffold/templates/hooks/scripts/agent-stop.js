#!/usr/bin/env node
'use strict';
// planning-with-files: Stop hook
// + AGENTS.md 同步检查

const fs = require('fs');
const path = require('path');
const { findActivePlanFile } = require('./planning-paths');
const { appendLog, getLogFile, LOG_DIR } = require('./session-log');

const EDITS_FILE = path.join('.github', 'session-logs', '.code-edits');

let input = '';
process.stdin.resume();
process.stdin.setEncoding('utf8');
process.stdin.on('data', d => (input += d));
process.stdin.on('end', () => {
  try { run(); } catch { process.stdout.write('{}'); }
});

function run() {
  // Prevent infinite continuation loops
  let data = {};
  try {
    data = JSON.parse(input);
    if (data.stop_hook_active === true) { process.stdout.write('{}'); return; }
  } catch {}

  const sessionId = data.sessionId || '';

  // --- AGENTS.md 同步检查 ---
  const agentsWarning = checkAgentsSync();

  // 写入 session 结束摘要
  writeSessionSummary(sessionId);

  const planFile = findActivePlanFile();
  if (!planFile) {
    // 无活跃计划，但仍需检查 AGENTS.md 同步
    if (agentsWarning) {
      process.stdout.write(JSON.stringify({
        hookSpecificOutput: { hookEventName: 'Stop', decision: 'block', reason: agentsWarning },
      }));
      return;
    }
    process.stdout.write('{}');
    return;
  }

  let content;
  try { content = fs.readFileSync(planFile, 'utf8'); } catch { process.stdout.write('{}'); return; }

  const total = (content.match(/### Phase/g) || []).length;
  if (total === 0) { process.stdout.write('{}'); return; }

  // Try **Status:** format first
  let complete = (content.match(/\*\*Status:\*\* complete/g) || []).length;
  let inProgress = (content.match(/\*\*Status:\*\* in_progress/g) || []).length;
  let pending = (content.match(/\*\*Status:\*\* pending/g) || []).length;

  // Fallback: [complete] inline format
  if (complete === 0 && inProgress === 0 && pending === 0) {
    complete = (content.match(/\[complete\]/g) || []).length;
    inProgress = (content.match(/\[in_progress\]/g) || []).length;
    pending = (content.match(/\[pending\]/g) || []).length;
  }

  if (complete === total) {
    // 全部阶段完成 → 归档
    const doneFile = planFile.replace(/task_plan\.md$/, 'task_plan.done.md');
    try { fs.renameSync(planFile, doneFile); } catch {}
    appendLog(sessionId, 'PlanArchived', { plan: planFile.replace(/\\/g, '/') });

    if (agentsWarning) {
      process.stdout.write(JSON.stringify({
        hookSpecificOutput: { hookEventName: 'Stop', decision: 'block', reason: agentsWarning },
      }));
      return;
    }
    process.stdout.write('{}');
    return;
  }

  const planDir = path.dirname(planFile).replace(/\\/g, '/');
  let reason = `[planning-with-files] Task incomplete (${complete}/${total} phases done). Read ${planDir}/task_plan.md and continue working on the remaining phases.`;
  if (agentsWarning) {
    reason += '\n' + agentsWarning;
  }

  process.stdout.write(JSON.stringify({
    hookSpecificOutput: { hookEventName: 'Stop', decision: 'block', reason },
  }));
}

/**
 * 检查被修改的代码文件所在模块是否有对应的 AGENTS.md 也被修改。
 * 返回提醒消息或 null。
 */
function checkAgentsSync() {
  let edits;
  try { edits = fs.readFileSync(EDITS_FILE, 'utf8').trim(); } catch { return null; }
  if (!edits) return null;

  const editedFiles = [...new Set(edits.split('\n').filter(Boolean))];

  // 分离代码文件和 AGENTS.md 文件
  const codeFiles = editedFiles.filter(f => !/AGENTS\.md$/i.test(f));
  const agentsEdited = new Set(editedFiles.filter(f => /AGENTS\.md$/i.test(f)).map(f => path.dirname(f.replace(/\\/g, '/'))));

  if (codeFiles.length === 0) return null;

  // 找出代码文件所在的模块目录（向上查找最近的 AGENTS.md 所在目录）
  const moduleDirs = new Set();
  for (const f of codeFiles) {
    const normalized = f.replace(/\\/g, '/');
    const moduleDir = findModuleDir(normalized);
    if (moduleDir) moduleDirs.add(moduleDir);
  }

  // 检查哪些模块被修改了代码但 AGENTS.md 未更新
  const missing = [];
  for (const dir of moduleDirs) {
    if (!agentsEdited.has(dir)) {
      missing.push(dir + '/AGENTS.md');
    }
  }

  if (missing.length === 0) return null;

  return `[agents-sync] 以下模块的代码已修改，但 AGENTS.md 未同步更新：\n${missing.map(m => '  - ' + m).join('\n')}\n请检查是否需要更新这些 AGENTS.md（如功能/接口/数据模型有变更）。`;
}

/**
 * 向上查找文件所在的最近模块目录（即包含 AGENTS.md 的最近祖先目录）。
 */
function findModuleDir(filePath) {
  let dir = path.dirname(filePath);
  const maxDepth = 10;
  for (let i = 0; i < maxDepth; i++) {
    const agentsPath = path.join(dir.replace(/\//g, path.sep), 'AGENTS.md');
    try {
      if (fs.existsSync(agentsPath)) {
        return dir;
      }
    } catch {}
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return null;
}

/** 分析当前会话日志，写入结束摘要 */
function writeSessionSummary(sessionId) {
  try {
    const logFile = getLogFile(sessionId);
    if (!fs.existsSync(logFile)) return;

    const content = fs.readFileSync(logFile, 'utf8');

    const agentStarts = (content.match(/## \d{2}:\d{2}:\d{2} \| SubagentStart/g) || []).length;
    const agentStops = (content.match(/## \d{2}:\d{2}:\d{2} \| SubagentStop/g) || []).length;
    const failures = (content.match(/❌ 验证失败/g) || []).length;

    const times = content.match(/## (\d{2}:\d{2}:\d{2})/g) || [];
    let duration = '未知';
    if (times.length >= 2) {
      const first = times[0].match(/(\d{2}):(\d{2}):(\d{2})/);
      const last = times[times.length - 1].match(/(\d{2}):(\d{2}):(\d{2})/);
      if (first && last) {
        const secs = (parseInt(last[1]) * 3600 + parseInt(last[2]) * 60 + parseInt(last[3]))
                   - (parseInt(first[1]) * 3600 + parseInt(first[2]) * 60 + parseInt(first[3]));
        if (secs > 0) {
          const m = Math.floor(secs / 60);
          const s = secs % 60;
          duration = m > 0 ? `${m}m${s}s` : `${s}s`;
        }
      }
    }

    appendLog(sessionId, 'Stop（Session 摘要）', {
      总时长: duration,
      Subagent调用: `${agentStarts} 次`,
      验证失败: failures > 0 ? `${failures} 次` : '0',
    });
  } catch {}
}
