#!/usr/bin/env node
'use strict';
// SubagentStop 验证钩子 — subagent 完成时自动检查代码质量和测试
// 检查项：ruff lint + pyright（Python）、tsc --noEmit（TypeScript）、关联测试

const { execFileSync, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const LESSONS_FILE = '.github/lessons-learned.md';
const MAX_LESSONS = 50;
const MAX_RETRIES = 3;
const RETRY_DIR = '.github/session-logs';

const { appendLog } = require('./session-log');

let input = '';
process.stdin.resume();
process.stdin.setEncoding('utf8');
process.stdin.on('data', d => (input += d));
process.stdin.on('end', () => {
  try { run(); } catch (e) { process.stdout.write('{}'); }
});

function run() {
  let data;
  try { data = JSON.parse(input); } catch { process.stdout.write('{}'); return; }

  // 防止死循环
  if (data.stop_hook_active === true) { process.stdout.write('{}'); return; }

  // 获取变更文件列表
  const changedFiles = getChangedFiles();
  if (changedFiles.length === 0) { process.stdout.write('{}'); return; }

  const pyFiles = changedFiles.filter(f => f.endsWith('.py') && !f.includes('__pycache__'));
  const tsFiles = changedFiles.filter(f => f.endsWith('.ts') || f.endsWith('.tsx'));

  const errors = [];

  // Python: ruff check + pyright
  if (pyFiles.length > 0) {
    const ruffErrors = runRuffCheck(pyFiles);
    if (ruffErrors) errors.push(ruffErrors);

    const pyrightErrors = runPyright(pyFiles);
    if (pyrightErrors) errors.push(pyrightErrors);
  }

  // TypeScript: tsc --noEmit
  if (tsFiles.length > 0) {
    const tscErrors = runTsc();
    if (tscErrors) errors.push(tscErrors);
  }

  // 关联测试
  const testErrors = runRelatedTests(changedFiles);
  if (testErrors) errors.push(testErrors);

  // 构建验证结果摘要
  const agentType = data.agent_type || 'unknown';
  const sessionId = data.sessionId || '';
  const verifyItems = [];
  if (pyFiles.length > 0) verifyItems.push(errors.some(e => e.includes('ruff')) ? 'ruff ✗' : 'ruff ✓');
  if (pyFiles.length > 0) verifyItems.push(errors.some(e => e.includes('pyright')) ? 'pyright ✗' : 'pyright ✓');
  if (tsFiles.length > 0) verifyItems.push(errors.some(e => e.includes('tsc')) ? 'tsc ✗' : 'tsc ✓');
  if (errors.some(e => e.includes('pytest'))) verifyItems.push('pytest ✗');
  else if (changedFiles.some(f => f.startsWith('backend/'))) verifyItems.push('pytest ✓');
  if (errors.some(e => e.includes('vitest'))) verifyItems.push('vitest ✗');
  else if (changedFiles.some(f => f.startsWith('frontend/'))) verifyItems.push('vitest ✓');

  // 写入审计日志
  appendLog(sessionId, 'SubagentStop', {
    Agent: agentType,
    变更文件: changedFiles.slice(0, 8).join(', '),
    验证结果: verifyItems.join(' | ') || '无检查项',
    状态: errors.length > 0 ? '❌ 验证失败' : '✅ 通过',
  });

  if (errors.length > 0) {
    const summary = errors.join('\n\n');
    const agentId = data.agent_id || 'unknown';

    // 重试计数
    const retryCount = incrementRetry(sessionId, agentId);

    // ① 硬保障：自动写入 lessons-learned.md
    recordLesson(data, summary);

    if (retryCount >= MAX_RETRIES) {
      // 降级：不再 block，通知用户人工介入
      appendLog(sessionId, 'SubagentStop（⚠️ 人工降级）', {
        Agent: agentType,
        重试次数: `${retryCount}/${MAX_RETRIES}`,
        原因: '验证反复失败，已降级到人工处理',
      });

      // 清理该 agent 的重试计数器
      clearRetry(sessionId, agentId);

      process.stdout.write(JSON.stringify({
        systemMessage: `[subagent-verify] ⚠️ 验证已失败 ${retryCount} 次，自动修复放弃，请人工检查以下问题：\n${summary}`,
      }));
    } else {
      // 正常 block，让 subagent 继续修
      const memoryHint = '\n\n修复完成后，请用 memory tool 将本次教训归纳写入 /memories/repo/python-notes.md（技术踩坑）或相应记忆文件，防止同类错误再次发生。';

      process.stdout.write(JSON.stringify({
        hookSpecificOutput: {
          hookEventName: 'SubagentStop',
          decision: 'block',
          reason: `[subagent-verify] 验证未通过（第 ${retryCount}/${MAX_RETRIES} 次，超过将降级人工），请修复：\n${summary}${memoryHint}`,
        },
      }));
    }
  } else {
    // 验证通过，清理重试计数器
    const agentId = data.agent_id || 'unknown';
    clearRetry(sessionId, agentId);
    process.stdout.write('{}');
  }
}

/** 获取 git 工作区变更文件（staged + unstaged + untracked） */
function getChangedFiles() {
  try {
    const staged = execSync('git diff --cached --name-only', {
      encoding: 'utf8', timeout: 10000, windowsHide: true,
    }).trim();
    const unstaged = execSync('git diff --name-only', {
      encoding: 'utf8', timeout: 10000, windowsHide: true,
    }).trim();
    const all = `${staged}\n${unstaged}`.split('\n').filter(Boolean);
    // 去重 + 只保留存在的文件
    return [...new Set(all)].filter(f => fs.existsSync(f));
  } catch {
    return [];
  }
}

/** ruff check（仅检查，不修复） */
function runRuffCheck(files) {
  try {
    execFileSync('ruff', ['check', '--no-fix', ...files], {
      encoding: 'utf8', timeout: 30000, windowsHide: true,
      stdio: ['pipe', 'pipe', 'pipe'],
    });
    return null; // 无错误
  } catch (e) {
    const output = (e.stdout || '') + (e.stderr || '');
    if (!output.trim()) return null;
    return `**ruff check 失败:**\n\`\`\`\n${truncate(output, 500)}\n\`\`\``;
  }
}

/** pyright 类型检查（仅检查变更文件） */
function runPyright(files) {
  try {
    execFileSync('pyright', ['--outputjson', ...files], {
      encoding: 'utf8', timeout: 60000, windowsHide: true,
      stdio: ['pipe', 'pipe', 'pipe'],
    });
    return null;
  } catch (e) {
    // pyright --outputjson 返回 JSON 格式
    try {
      const result = JSON.parse(e.stdout || '{}');
      const diags = (result.generalDiagnostics || [])
        .filter(d => d.severity === 'error')
        .slice(0, 10)
        .map(d => `  ${d.file}:${d.range?.start?.line || '?'} - ${d.message}`)
        .join('\n');
      if (!diags) return null;
      return `**pyright 类型错误:**\n\`\`\`\n${diags}\n\`\`\``;
    } catch {
      // JSON 解析失败，回退纯文本
      const output = (e.stdout || '') + (e.stderr || '');
      if (!output.trim()) return null;
      return `**pyright 错误:**\n\`\`\`\n${truncate(output, 500)}\n\`\`\``;
    }
  }
}

/** TypeScript 类型检查（项目级） */
function runTsc() {
  const tsconfigPath = path.join('frontend', 'tsconfig.app.json');
  if (!fs.existsSync(tsconfigPath)) return null;

  try {
    execFileSync('npx', ['tsc', '--noEmit', '-p', tsconfigPath], {
      encoding: 'utf8', timeout: 60000, windowsHide: true,
      cwd: 'frontend',
      stdio: ['pipe', 'pipe', 'pipe'],
    });
    return null;
  } catch (e) {
    const output = (e.stdout || '') + (e.stderr || '');
    if (!output.trim()) return null;
    // 只取前 10 行错误
    const lines = output.trim().split('\n').filter(l => l.includes('error TS')).slice(0, 10).join('\n');
    if (!lines) return null;
    return `**tsc 类型错误:**\n\`\`\`\n${lines}\n\`\`\``;
  }
}

/** 查找并运行关联测试 */
function runRelatedTests(changedFiles) {
  const pyTestFiles = findPythonTestFiles(changedFiles);
  const tsTestFiles = findTsTestFiles(changedFiles);

  const errors = [];

  // pytest
  if (pyTestFiles.length > 0) {
    try {
      execFileSync('python', ['-m', 'pytest', '-x', '--tb=short', '-q', ...pyTestFiles], {
        encoding: 'utf8', timeout: 90000, windowsHide: true,
        cwd: 'backend',
        stdio: ['pipe', 'pipe', 'pipe'],
      });
    } catch (e) {
      const output = (e.stdout || '') + (e.stderr || '');
      if (output.includes('FAILED') || output.includes('ERROR')) {
        errors.push(`**pytest 失败:**\n\`\`\`\n${truncate(output, 800)}\n\`\`\``);
      }
    }
  }

  // vitest
  if (tsTestFiles.length > 0) {
    try {
      execFileSync('npx', ['vitest', 'run', '--reporter=verbose', ...tsTestFiles], {
        encoding: 'utf8', timeout: 90000, windowsHide: true,
        cwd: 'frontend',
        stdio: ['pipe', 'pipe', 'pipe'],
      });
    } catch (e) {
      const output = (e.stdout || '') + (e.stderr || '');
      if (output.includes('FAIL') || output.includes('Error')) {
        errors.push(`**vitest 失败:**\n\`\`\`\n${truncate(output, 800)}\n\`\`\``);
      }
    }
  }

  return errors.length > 0 ? errors.join('\n\n') : null;
}

/**
 * Python 源文件 → 测试文件映射
 * backend/app/services/foo.py → backend/tests/services/test_foo.py
 * backend/app/api/v1/foo.py   → backend/tests/api/test_foo.py
 * backend/app/tasks/foo.py    → backend/tests/tasks/test_foo.py
 * backend/app/core/foo.py     → backend/tests/unit/test_foo.py
 * backend/app/models/foo.py   → backend/tests/unit/test_foo.py
 */
function findPythonTestFiles(changedFiles) {
  const testFiles = [];
  for (const f of changedFiles) {
    if (!f.endsWith('.py') || !f.startsWith('backend/app/')) continue;
    const basename = path.basename(f);
    if (basename.startsWith('__')) continue;

    const testName = `test_${basename}`;
    const relPath = f.replace('backend/app/', '');
    let testDir;

    if (relPath.startsWith('services/')) testDir = 'backend/tests/services';
    else if (relPath.startsWith('api/')) testDir = 'backend/tests/api';
    else if (relPath.startsWith('tasks/')) testDir = 'backend/tests/tasks';
    else testDir = 'backend/tests/unit';

    const candidate = path.join(testDir, testName);
    if (fs.existsSync(candidate)) testFiles.push(candidate);
  }
  return [...new Set(testFiles)];
}

/**
 * TypeScript 源文件 → 测试文件映射
 * foo.ts   → foo.test.ts 或 __tests__/foo.test.ts
 * foo.tsx  → foo.test.tsx 或 __tests__/foo.test.tsx
 */
function findTsTestFiles(changedFiles) {
  const testFiles = [];
  for (const f of changedFiles) {
    if (!f.startsWith('frontend/src/') || (!f.endsWith('.ts') && !f.endsWith('.tsx'))) continue;
    if (f.includes('.test.') || f.includes('__tests__') || f.includes('test-utils')) continue;

    const dir = path.dirname(f);
    const ext = path.extname(f);
    const base = path.basename(f, ext);

    // 同级 .test 文件
    const sameDir = path.join(dir, `${base}.test${ext}`);
    if (fs.existsSync(sameDir)) { testFiles.push(sameDir); continue; }

    // __tests__ 目录
    const testsDir = path.join(dir, '__tests__', `${base}.test${ext}`);
    if (fs.existsSync(testsDir)) { testFiles.push(testsDir); continue; }

    // .tsx 源 → .test.ts（无 x）
    if (ext === '.tsx') {
      const altSameDir = path.join(dir, `${base}.test.ts`);
      if (fs.existsSync(altSameDir)) { testFiles.push(altSameDir); continue; }
      const altTestsDir = path.join(dir, '__tests__', `${base}.test.ts`);
      if (fs.existsSync(altTestsDir)) testFiles.push(altTestsDir);
    }
  }
  return [...new Set(testFiles)];
}

function truncate(str, maxLen) {
  if (str.length <= maxLen) return str;
  return str.slice(0, maxLen) + '\n... (截断)';
}

/** 将验证失败记录追加到 .github/lessons-learned.md */
function recordLesson(hookData, errorSummary) {
  try {
    const now = new Date().toISOString().replace('T', ' ').slice(0, 19);
    const agentType = hookData.agent_type || 'unknown';
    // 提取错误类别
    const categories = [];
    if (errorSummary.includes('ruff')) categories.push('lint');
    if (errorSummary.includes('pyright')) categories.push('类型错误');
    if (errorSummary.includes('tsc')) categories.push('TS类型错误');
    if (errorSummary.includes('pytest')) categories.push('测试失败');
    if (errorSummary.includes('vitest')) categories.push('测试失败');
    const category = categories.join(', ') || '验证失败';

    // 提取涉及的文件（从错误摘要中匹配文件路径）
    const fileMatches = errorSummary.match(/(?:backend|frontend)\/[\w/./-]+\.\w+/g) || [];
    const files = [...new Set(fileMatches)].slice(0, 5).join(', ') || '未知';

    // 构造条目
    const entry = [
      `## ${now} | ${category}`,
      `- **Agent**: ${agentType}`,
      `- **文件**: ${files}`,
      `- **摘要**: ${truncate(errorSummary.replace(/```[\s\S]*?```/g, '[代码块]').replace(/\n/g, ' '), 200)}`,
      '',
    ].join('\n');

    // 确保目录存在
    const dir = path.dirname(LESSONS_FILE);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    // 读取现有内容或创建头部
    let existing = '';
    if (fs.existsSync(LESSONS_FILE)) {
      existing = fs.readFileSync(LESSONS_FILE, 'utf8');
    } else {
      existing = '# 自动记录的教训\n\n> 由 SubagentStop hook 自动写入。验证失败时记录错误类型和上下文。\n\n';
    }

    // 追加新条目（在头部之后插入，新条目在最前面）
    const headerEnd = existing.indexOf('\n## ');
    let newContent;
    if (headerEnd >= 0) {
      newContent = existing.slice(0, headerEnd) + '\n' + entry + existing.slice(headerEnd);
    } else {
      newContent = existing + entry;
    }

    // 截断：最多保留 MAX_LESSONS 条
    const sections = newContent.split(/(?=^## \d{4}-)/m);
    if (sections.length > MAX_LESSONS + 1) { // +1 for header
      newContent = sections.slice(0, MAX_LESSONS + 1).join('');
    }

    fs.writeFileSync(LESSONS_FILE, newContent, 'utf8');
  } catch {
    // 写入失败不阻塞主流程
  }
}

/** 重试计数器文件路径 */
function retryFile(sessionId, agentId) {
  const safe = (sessionId + '_' + agentId).replace(/[^a-zA-Z0-9_-]/g, '_');
  return path.join(RETRY_DIR, `.retry-${safe}`);
}

/** 读取并递增重试次数，返回递增后的值 */
function incrementRetry(sessionId, agentId) {
  const file = retryFile(sessionId, agentId);
  let count = 0;
  try {
    if (!fs.existsSync(RETRY_DIR)) fs.mkdirSync(RETRY_DIR, { recursive: true });
    if (fs.existsSync(file)) count = parseInt(fs.readFileSync(file, 'utf8'), 10) || 0;
  } catch { /* ignore */ }
  count += 1;
  try { fs.writeFileSync(file, String(count), 'utf8'); } catch { /* ignore */ }
  return count;
}

/** 清除重试计数器 */
function clearRetry(sessionId, agentId) {
  try { fs.unlinkSync(retryFile(sessionId, agentId)); } catch { /* ignore */ }
}
