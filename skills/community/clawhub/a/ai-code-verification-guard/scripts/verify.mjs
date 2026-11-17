#!/usr/bin/env node
/**
 * 确定性验证脚本 —— 裁决者是工具，不是模型。
 *
 * 用法:
 *   node verify.mjs snapshot   修改前执行，记录当前行为类检查的基线
 *   node verify.mjs run        修改后执行，运行全部检查并对比基线
 *
 * 退出码: 0 = PASS / PASS_WITH_UNVERIFIED | 1 = FAIL / REGRESSION | 2 = UNVERIFIED
 * 零依赖，不安装任何包，不改动项目源码（仅在 .verification/ 下写基线）。
 */

import { execSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const root = process.cwd();
const baselineDir = join(root, '.verification');
const baselineFile = join(baselineDir, 'baseline.json');
const mode = process.argv[2] || 'run';

const notes = [];

function tail(str, n = 10) {
  const lines = String(str).trim().split(/\r?\n/).filter(Boolean);
  return lines.slice(-n).join('\n');
}

function runCmd(cmd) {
  try {
    // maxBuffer 默认仅 1MB，测试运行器的输出动辄数 MB，超限会中途杀掉子进程造成假 FAIL
    const out = execSync(cmd, { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], timeout: 600000, maxBuffer: 64 * 1024 * 1024 });
    return { status: 'pass', output: out };
  } catch (err) {
    const text = String((err && err.stderr) || '') + String((err && err.stdout) || '') + String((err && err.message) || '');
    // 9009 = Windows cmd 的 command-not-found 专用退出码；Store 应用别名 stub（如未安装的 python）
    // 失败时 stderr 近乎为空，关键词匹配不到，必须按退出码兜底，否则环境缺失会被误判为 FAIL
    if (
      (err && (err.code === 'ENOENT' || err.status === 9009)) ||
      /not recognized|CommandNotFound|不是内部或外部命令|was not found/i.test(text)
    ) {
      return { status: 'unverified', output: text };
    }
    return { status: 'fail', output: text };
  }
}

function changedFiles() {
  try {
    const out = execSync('git diff --name-only', { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    const files = out.trim().split(/\r?\n/).filter(Boolean);
    return files.length > 0 ? files : null;
  } catch {
    return null;
  }
}

function gitAutocrlfEnabled() {
  try {
    const out = execSync('git config core.autocrlf', { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    return out.trim().toLowerCase() === 'true';
  } catch {
    return false;
  }
}

function detectChecks() {
  const checks = [];
  const has = (p) => existsSync(join(root, p));

  if (has('package.json')) {
    let pkg = {};
    try { pkg = JSON.parse(readFileSync(join(root, 'package.json'), 'utf8')); } catch { notes.push('package.json 解析失败'); }
    const scripts = pkg.scripts || {};

    // monorepo 感知：仅声明守卫覆盖范围，不遍历子包（成本不可控且各包需独立可验证）
    if (pkg.workspaces || has('pnpm-workspace.yaml') || has('lerna.json')) {
      notes.push('检测到 monorepo workspace，仅执行根级检查，子包自身检查不在守卫范围');
    }

    // 检查类脚本探测规则（基于 42 个流行包的命名实证）：
    // 命名五花八门（lint / check:lint / typecheck / check:type / format:check…），
    // 以命令内容识别为主、脚本名为辅；绝不执行修改型（--fix/--write）或常驻型（--watch/-w）脚本。
    // 注意：裸 lint 也可能是 --fix（如 sequelize），必须看内容；standard-version 是发版工具需防误匹配。
    // watch 陷阱：vitest 不带 run/--run 就是 watch 模式（挂死风险）；--watch 同理
    const isWatchTrap = (cmd) => {
      const c = cmd.toLowerCase();
      return /--watch(?![\w-])/.test(c) || (/vitest/.test(c) && !/\brun\b(?!-)/.test(c));
    };
    const isUnsafe = (key, cmd) => {
      const s = `${key} ${cmd}`.toLowerCase();
      return (
        /--fix|--write|autofix/.test(s) ||
        /--watch(?:\s|$)|(?:^|\s)-w(?:\s|$)/.test(s) ||
        /(^|[:._-])(fix|write|watch|tdd)($|[:._-])/.test(key.toLowerCase()) ||
        isWatchTrap(String(cmd))
      );
    };
    const classify = (key, cmd) => {
      const k = key.toLowerCase();
      const c = cmd.toLowerCase();
      if (/\beslint\b|\bstylelint\b|\bstandard(?![\w-])|\bbiome check\b|\bgts lint\b/.test(c)) return 'lint';
      if (/\bprettier\b/.test(c) && /--check/.test(c)) return 'format';
      // tsc 同时被构建/代码生成脚本使用（emit 写盘），build-ish 键名的一律不当作类型检查
      const isBuildish = /^(pre|post)?(build|compile|bundle|package|prepare)(?=$|[:._-])|^generate|^gen(?=$|[:._-])|(^|[:._-])(bench|benchmark)($|[:._-])/.test(k);
      if (!isBuildish && /\btsc\b|\btsgo\b|\bdtslint\b|\btype-?check\b|\bcheck-?types\b/.test(c)) return 'typecheck';
      if (k === 'lint' || /^(ci|test):lint$/.test(k)) return 'lint';
      if (/^type-?check$|^check-?types$/.test(k) || /^(check|ci|test):type/.test(k)) return 'typecheck';
      if (/^format-?check$|^prettier-?check$|^(check|ci|test):format$/.test(k)) return 'format';
      if (k === 'check') return 'check';
      return null;
    };

    // vitest 默认 watch；单命令 vitest 脚本可确定性改走本地 vitest.mjs + run（语义不变，仅关 watch）。
    // 优先选带 unit 的子集脚本（如 vue 的 test-unit），避免全量套件里的 e2e 因缺构建而误报。
    const candidates = [];
    const vitestRunCmd = (cmd) => {
      const c = cmd.trim();
      if (/[&|;]/.test(c) || /\be2e\b|\bbrowser\b|\bcypress\b|\bplaywright\b/.test(c)) return null;
      const m = c.match(/^(?:[a-z@./-]*\s*)?vitest\b\s*(.*)$/);
      if (!m || !has('node_modules/vitest/vitest.mjs')) return null;
      return ('node node_modules/vitest/vitest.mjs run ' + m[1].replace(/^run\b(?!-)\s*/, '')).trimEnd();
    };
    if (scripts.test) {
      const t = String(scripts.test);
      if (!isWatchTrap(t)) {
        candidates.push({ key: 'test', cat: 'test', cmd: t, canonical: true });
      } else {
        const unitSiblingKey = Object.keys(scripts).find((k) => {
          if (k === 'test' || !/^test[:_-]/i.test(k)) return false;
          const s = String(scripts[k]);
          return /unit/i.test(s) && !!vitestRunCmd(s);
        });
        const direct = vitestRunCmd(t);
        if (unitSiblingKey) {
          const fixed = vitestRunCmd(String(scripts[unitSiblingKey]));
          notes.push(`test 脚本为 watch 模式，改用等价 run 模式脚本 "${unitSiblingKey}"`);
          candidates.push({ key: 'test', cat: 'test', cmd: fixed, exec: fixed });
        } else if (direct) {
          notes.push('test 脚本为 vitest watch 模式，已确定性改走 vitest run');
          candidates.push({ key: 'test', cat: 'test', cmd: direct, exec: direct });
        } else {
          notes.push(`test 脚本疑似 watch 模式（"${t}"），跳过以防挂死`);
        }
      }
    }
    for (const [key, cmd] of Object.entries(scripts)) {
      if (key === 'test') continue;
      // "-only"/":only" 后缀脚本依赖手动前置步骤（如 vue 的 test-dts-only 需先 build-dts），单跑必挂
      if (/(^|[:._-])only$/.test(key.toLowerCase())) {
        notes.push(`脚本 "${key}" 疑似部分执行脚本（-only 后缀），依赖手动前置步骤，跳过`);
        continue;
      }
      const cat = classify(key, String(cmd));
      if (cat && !isUnsafe(key, String(cmd))) candidates.push({ key, cat, cmd: String(cmd) });
    }
    // 裸 check 通常是项目自己的总门禁，优先采用并折叠 check:* 子项，避免重复执行
    const hasComposite = candidates.some((c) => c.key === 'check');
    const queued = new Set();
    for (const c of candidates) {
      if (hasComposite && c.key !== 'check' && /^check($|:)/.test(c.key.toLowerCase())) continue;
      if (queued.has(c.cmd)) continue;
      queued.add(c.cmd);
      const dup = checks.filter((x) => x.name === c.cat).length;
      // exec 存在时优先使用（vitest watch 翻转后的直调命令），否则翻转会退化回 npm run test 的 watch 陷阱
      checks.push({ name: dup > 0 ? `${c.cat}:${dup + 1}` : c.cat, cmd: c.exec || (c.canonical ? 'npm test' : `npm run ${c.key}`) });
    }

    // Windows autocrlf 检出把文本行尾改为 CRLF，prettier 等格式检查会对全新克隆系统性假失败
    if (checks.some((x) => x.name === 'format') && gitAutocrlfEnabled()) {
      notes.push('git autocrlf 已启用（文本以 CRLF 检出），格式类检查可能出现环境性假失败；建议以 -c core.autocrlf=false 重新检出');
    }

    // 兜底类型检查：仅在项目没有自己的类型检查脚本、也没有总门禁时才自作主张
    if (!checks.some((x) => /^type/.test(x.name) || x.name === 'check') && has('tsconfig.json') && existsSync(join(root, 'node_modules', 'typescript'))) {
      checks.push({ name: 'typecheck', cmd: 'npx tsc --noEmit' });
    }
  }

  if (has('go.mod')) {
    checks.push({ name: 'build', cmd: 'go build ./...' });
    checks.push({ name: 'vet', cmd: 'go vet ./...' });
    checks.push({ name: 'test', cmd: 'go test ./...' });
  }

  if (has('Cargo.toml')) {
    checks.push({ name: 'check', cmd: 'cargo check' });
    checks.push({ name: 'test', cmd: 'cargo test' });
  }

  if (has('pyproject.toml') || has('requirements.txt')) {
    checks.push({ name: 'syntax', cmd: 'python -m compileall -q .' });
    checks.push({ name: 'pytest', cmd: 'python -m pytest -q' });
  }

  // 兜底：无生态标识的原生 JS 项目（含演示项目这类裸目录）
  if (checks.length === 0) {
    let entries = [];
    try {
      entries = readdirSync(root).filter((f) => statSync(join(root, f)).isFile() && /\.(m|c)?js$/.test(f));
    } catch { /* 不可读则保持为空 */ }
    const testFiles = entries.filter((f) => /\.(test|spec)\.(m|c)?js$/.test(f) || /^test[-_].*\.(m|c)?js$/.test(f));
    const srcFiles = entries.filter((f) => !testFiles.includes(f));
    for (const f of srcFiles) checks.push({ name: `syntax:${f}`, cmd: `node --check "${f}"`, syntax: true });
    if (testFiles.length > 0) {
      checks.push({ name: 'test', cmd: `node --test ${testFiles.map((f) => `"${f}"`).join(' ')}` });
    }
  }

  return checks;
}

function emitVerdict(results, verdict, extraLines = []) {
  const scope = changedFiles();
  const lines = ['=== VERIFY VERDICT（工具裁决，转述不得改写结论） ==='];
  lines.push(scope ? `scope: ${scope.length} 个变更文件 -> ${scope.join(', ')}` : 'scope: 非 git 仓库或无未提交变更');
  for (const r of results) {
    lines.push(`[${r.status}] ${r.name}`);
    if (r.output) lines.push(tail(r.output));
  }
  for (const n of notes) lines.push(`[note] ${n}`);
  for (const e of extraLines) lines.push(e);
  lines.push(`RESULT: ${verdict}`);
  lines.push('=== END VERDICT ===');
  console.log(lines.join('\n'));
}

const checks = detectChecks();

if (checks.length === 0) {
  emitVerdict([], 'UNVERIFIED', ['未识别到任何项目结构、检查命令或测试文件']);
  process.exit(2);
}

if (mode === 'snapshot') {
  const baseline = {};
  const results = [];
  for (const c of checks) {
    if (c.syntax) continue; // 基线只记录行为类检查
    const r = runCmd(c.cmd);
    baseline[c.name] = r.status;
    results.push({ name: c.name, status: r.status, output: tail(r.output) });
  }
  if (results.length === 0) notes.push('没有行为类检查可记录基线（只有语法检查）');
  mkdirSync(baselineDir, { recursive: true });
  // 尾换行：避免基线文件本身被项目的 prettier 等格式检查标记
  writeFileSync(baselineFile, JSON.stringify({ savedAt: new Date().toISOString(), checks: baseline }, null, 2) + '\n');
  emitVerdict(results, 'SNAPSHOT', ['基线已保存到 .verification/baseline.json']);
  process.exit(0);
}

// mode === 'run'
const results = checks.map((c) => {
  const r = runCmd(c.cmd);
  return { name: c.name, status: r.status, output: tail(r.output) };
});

const extra = [];
let baselineData = null;
if (existsSync(baselineFile)) {
  try { baselineData = JSON.parse(readFileSync(baselineFile, 'utf8')); } catch { notes.push('基线文件损坏，跳过对比'); }
}
if (baselineData && baselineData.checks) {
  for (const r of results) {
    if (baselineData.checks[r.name] === 'pass' && r.status === 'fail') {
      extra.push(`[regression] ${r.name}: 基线通过 -> 现在失败`);
    }
  }
}

const hasFail = results.some((r) => r.status === 'fail');
const hasUnverified = results.some((r) => r.status === 'unverified');
const allUnverified = results.every((r) => r.status === 'unverified');
const hasRegression = extra.some((e) => e.startsWith('[regression]'));

let verdict = 'PASS';
if (hasRegression) verdict = 'REGRESSION';
else if (hasFail) verdict = 'FAIL';
else if (allUnverified) verdict = 'UNVERIFIED';
else if (hasUnverified) verdict = 'PASS_WITH_UNVERIFIED';

if (verdict === 'REGRESSION' || verdict === 'FAIL') extra.push('处置：修复后重跑 run，PASS 前禁止报告完成');
else if (verdict === 'UNVERIFIED') extra.push('处置：如实向用户列出无法验证的原因，禁止报告完成');
else if (verdict === 'PASS_WITH_UNVERIFIED') extra.push('处置：可报告完成，但必须逐项转述 unverified 条目');

emitVerdict(results, verdict, extra);
process.exit(verdict === 'PASS' || verdict === 'PASS_WITH_UNVERIFIED' ? 0 : verdict === 'UNVERIFIED' ? 2 : 1);
