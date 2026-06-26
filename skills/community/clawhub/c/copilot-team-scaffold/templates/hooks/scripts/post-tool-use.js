#!/usr/bin/env node
'use strict';
// planning-with-files: Post-tool-use hook
// + AGENTS.md 门控状态追踪
// + 代码编辑追踪（用于 Stop 时检查 AGENTS.md 同步）

const fs = require('fs');
const path = require('path');
const { describeActiveLocation } = require('./planning-paths');

const GATE_FILE = path.join('.github', 'session-logs', '.agents-gate');
const EDITS_FILE = path.join('.github', 'session-logs', '.code-edits');
const WRITE_TOOLS = ['replace_string_in_file', 'create_file', 'multi_replace_string_in_file'];
const CODE_EXTS = ['.py', '.ts', '.tsx', '.js', '.jsx'];

let input = '';
process.stdin.resume();
process.stdin.setEncoding('utf8');
process.stdin.on('data', d => (input += d));
process.stdin.on('end', () => {
  try { run(); } catch { process.stdout.write('{}'); }
});

function run() {
  let data;
  try { data = JSON.parse(input); } catch { data = {}; }

  const toolName = data.tool_name || data.toolName || '';

  // 检测 read_file 是否读取了 AGENTS.md → 打开门控
  if (toolName === 'read_file') {
    const params = data.tool_input || data.toolInput || data.input || {};
    const filePath = params.filePath || params.file_path || '';
    if (/AGENTS\.md$/i.test(filePath)) {
      try { fs.writeFileSync(GATE_FILE, filePath + '\n', { flag: 'a' }); } catch {}
    }
  }

  // 追踪代码文件编辑 + AGENTS.md 编辑
  if (WRITE_TOOLS.includes(toolName)) {
    const files = getTargetFiles(toolName, data.tool_input || data.toolInput || data.input || {});
    for (const f of files) {
      const normalized = f.replace(/\\/g, '/');
      if (/AGENTS\.md$/i.test(normalized) || isCodeFile(normalized)) {
        try { fs.writeFileSync(EDITS_FILE, normalized + '\n', { flag: 'a' }); } catch {}
      }
    }

    // 创建代码文件后检查目录是否有 AGENTS.md
    if (toolName === 'create_file') {
      for (const f of files) {
        if (isCodeFile(f)) {
          const dir = path.dirname(f);
          const agentsPath = path.join(dir, 'AGENTS.md');
          try {
            if (!fs.existsSync(agentsPath)) {
              const planDir = describeActiveLocation();
              const msg = `[agents-sync] 新文件 ${path.basename(f)} 所在目录没有 AGENTS.md（${dir.replace(/\\/g, '/')}）。如果这是新模块，请创建 AGENTS.md。\n[planning-with-files] If this completes a phase, update the planning files in ${planDir}.`;
              process.stdout.write(JSON.stringify({
                hookSpecificOutput: { hookEventName: 'PostToolUse', additionalContext: msg },
              }));
              return;
            }
          } catch {}
        }
      }
    }
  }

  const planDir = describeActiveLocation();
  const msg = `[planning-with-files] File updated. If this completes a phase, update the planning files in ${planDir}.`;

  process.stdout.write(JSON.stringify({
    hookSpecificOutput: { hookEventName: 'PostToolUse', additionalContext: msg },
  }));
}

/** 从工具参数中提取所有目标文件路径 */
function getTargetFiles(toolName, params) {
  if (toolName === 'multi_replace_string_in_file') {
    return (params.replacements || []).map(r => r.filePath || '').filter(Boolean);
  }
  const f = params.filePath || params.file_path || '';
  return f ? [f] : [];
}

function isCodeFile(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return CODE_EXTS.includes(ext);
}
