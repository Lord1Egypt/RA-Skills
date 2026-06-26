#!/usr/bin/env node
'use strict';
// Pre-tool-use hook:
// 1. AGENTS.md 门控 — 写代码文件前必须先读过 AGENTS.md
// 2. 新模块目录 AGENTS.md 强制创建 — create_file 到无 AGENTS.md 的目录时阻断
// 3. planning-with-files — 条件注入 plan 上下文

const fs = require('fs');
const path = require('path');
const { findActivePlanFile } = require('./planning-paths');

const GATE_FILE = path.join('.github', 'session-logs', '.agents-gate');
const WRITE_TOOLS = ['replace_string_in_file', 'create_file', 'multi_replace_string_in_file'];
const CODE_EXTS = ['.py', '.ts', '.tsx'];

let input = '';
process.stdin.resume();
process.stdin.setEncoding('utf8');
process.stdin.on('data', d => (input += d));
process.stdin.on('end', () => {
  try { run(); } catch { process.stdout.write('{}'); }
});

function run() {
  let data = {};
  try { data = JSON.parse(input); } catch {}

  const toolName = data.tool_name || data.toolName || '';
  const params = data.tool_input || data.toolInput || data.input || {};

  // --- AGENTS.md 门控 ---
  if (WRITE_TOOLS.includes(toolName)) {
    const filePath = getTargetFile(toolName, params);
    if (filePath && isCodeFile(filePath) && !isGateOpen()) {
      process.stdout.write(JSON.stringify({
        hookSpecificOutput: {
          hookEventName: 'PreToolUse',
          permissionDecision: 'deny',
          reason: '[agents-gate] 请先读取目标模块的 AGENTS.md（read_file），了解模块约束后再修改代码文件。',
        },
      }));
      return;
    }

    // --- 新模块目录 AGENTS.md 强制创建 ---
    if (toolName === 'create_file' && filePath && isCodeFile(filePath)) {
      if (hasParentAgentsMd(filePath) && !hasAgentsMd(filePath)) {
        process.stdout.write(JSON.stringify({
          hookSpecificOutput: {
            hookEventName: 'PreToolUse',
            permissionDecision: 'deny',
            reason: `[agents-gate] 目标目录没有 AGENTS.md：${path.dirname(filePath).replace(/\\/g, '/')}\n请先用 create_file 创建该目录的 AGENTS.md（模块功能、技术栈、接口定义、数据模型、注意事项），再创建代码文件。`,
          },
        }));
        return;
      }
    }
  }

  // --- planning-with-files 上下文注入 ---
  if (!process.env.PLANNING_WITH_FILES_PLAN_DIR) {
    process.stdout.write('{}');
    return;
  }

  const planFile = findActivePlanFile();
  if (!planFile) { process.stdout.write('{}'); return; }

  let context = '';
  try {
    context = fs.readFileSync(planFile, 'utf8').split('\n').slice(0, 30).join('\n');
  } catch {}

  if (!context) {
    process.stdout.write(JSON.stringify({
      hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: 'allow' },
    }));
    return;
  }

  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      permissionDecision: 'allow',
      additionalContext: context,
    },
  }));
}

/** 从工具参数中提取目标文件路径 */
function getTargetFile(toolName, params) {
  if (toolName === 'multi_replace_string_in_file') {
    const replacements = params.replacements || [];
    return replacements[0] ? (replacements[0].filePath || '') : '';
  }
  return params.filePath || params.file_path || '';
}

/** 判断是否为代码文件 */
function isCodeFile(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return CODE_EXTS.includes(ext);
}

/** 检查 AGENTS.md 门控是否已打开（文件非空 = 已读过） */
function isGateOpen() {
  try {
    const content = fs.readFileSync(GATE_FILE, 'utf8');
    return content.trim().length > 0;
  } catch {
    return true;
  }
}

/**
 * 检查父目录是否有 AGENTS.md —— 用于判断当前目录是否属于"模块级目录体系"。
 * 如果父目录有 AGENTS.md，说明兄弟目录也应有，当前目录缺失则需创建。
 */
function hasParentAgentsMd(filePath) {
  const dir = path.dirname(filePath);
  const parent = path.dirname(dir);
  try { return fs.existsSync(path.join(parent, 'AGENTS.md')); } catch { return false; }
}

/** 检查文件所在目录是否已有 AGENTS.md */
function hasAgentsMd(filePath) {
  const dir = path.dirname(filePath);
  try { return fs.existsSync(path.join(dir, 'AGENTS.md')); } catch { return false; }
}
