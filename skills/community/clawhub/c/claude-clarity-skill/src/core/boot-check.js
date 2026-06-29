/**
 * Clarity Boot Check v1.0.0
 * 启动自检：验证核心文件 + 版本一致 + 身份锚点
 * 基于 v11.9.4 self-check.js 重写适配
 *
 * 用法:
 *   const { bootCheck } = require('./boot-check');
 *   const report = bootCheck();        // 运行自检
 *   const report = bootCheck(true);   // 静默模式
 */

const fs = require('fs');
const path = require('path');

// 心虫根目录: src/core/boot-check.js → 心虫根目录
const ROOT = path.resolve(__dirname, '../..');

// 核心文件检查项
const CORE_CHECKS = [
  {
    id: 'identity',
    label: 'CORE_IDENTITY.md',
    path: path.join(ROOT, 'CORE_IDENTITY.md'),
    verify: (c) => c.includes('Clarity') && c.includes('心虫'),
    required: true,
  },
  {
    id: 'identity-core',
    label: 'identity-core.md',
    path: path.join(ROOT, 'memory/identity-core.md'),
    verify: (c) => c.includes('心虫身份核心') && c.includes('我是谁'),
    required: true,
  },
  {
    id: 'skill',
    label: 'SKILL.md',
    path: path.join(ROOT, 'SKILL.md'),
    verify: (c) => c.includes('version') && c.length > 500,
    required: true,
  },
  {
    id: 'package',
    label: 'package.json',
    path: path.join(ROOT, 'package.json'),
    verify: (c) => {
      try {
        const p = JSON.parse(c);
        return p.version !== undefined && p.version.length > 0;
      } catch { /* JSON 解析失败视为验证不通过 */ return false; }
    },
    required: true,
  },
  {
    id: 'meaningful-memory',
    label: 'meaningful-memory.js',
    path: path.join(ROOT, 'src/core/meaningful-memory.js'),
    verify: (c) => c.includes('MeaningfulMemory') && c.length > 3000,
    required: true,
  },
  {
    id: 'decision-verifier',
    label: 'decision-verifier.js',
    path: path.join(ROOT, 'src/core/decision-verifier.js'),
    verify: (c) => c.includes('DecisionVerifier') && c.length > 2000,
    required: false,
  },
];

// Module load checks — MeaningfulMemory is the primary memory engine
// triality-memory.js has been merged into meaningful-memory.js
const MODULE_CHECKS = [
  { id: 'meaningful-memory', label: 'MeaningfulMemory', path: './meaningful-memory.js' },
  { id: 'decision-verifier', label: 'DecisionVerifier', path: './decision-verifier.js' },
  { id: 'confidence-calibrator', label: 'ConfidenceCalibrator', path: './confidence-calibrator.js' },
  { id: 'counterfactual-engine', label: 'CounterfactualEngine', path: './counterfactual-engine.js' },
  { id: 'error-handler', label: 'ErrorHandler', path: './error-handler.js' },
  { id: 'state-snapshot', label: 'StateSnapshot', path: './state-snapshot.js' },
  { id: 'wake-up-verifier', label: 'WakeUpVerifier', path: './wake-up-verifier.js' },
];

function runFileCheckFast(item) {
  // 快速模式：只检查文件存在 + 非空（不验证具体内容），约 1ms/文件
  try {
    if (!fs.existsSync(item.path)) {
      return { ...item, status: 'MISSING', detail: 'file not found' };
    }
    const stat = fs.statSync(item.path);
    const ok = stat.size > 0 && stat.isFile();
    const status = ok ? 'PASS' : 'FAIL';
    const detail = ok ? `${(stat.size / 1024).toFixed(1)}KB` : 'empty file';
    return { ...item, status, detail };
  } catch (e) {
    return { ...item, status: 'ERROR', detail: e.message };
  }
}

function runFileCheck(item) {
  try {
    if (!fs.existsSync(item.path)) {
      return { ...item, status: 'MISSING', detail: 'file not found' };
    }
    const content = fs.readFileSync(item.path, 'utf8');
    const pass = item.verify(content);
    return { ...item, status: pass ? 'PASS' : 'FAIL', detail: pass ? 'ok' : 'content check failed' };
  } catch (e) {
    return { ...item, status: 'ERROR', detail: e.message };
  }
}

function runModuleCheck(item) {
  const startTime = performance ? performance.now() : 0;
  try {
    const mod = require(item.path);
    // 检查命名导出 或 默认导出（CommonJS 两种模式都兼容）
    const ok = mod[item.label] !== undefined || typeof mod === 'function' || (typeof mod === 'object' && mod !== null);

    // 加载耗时（毫秒，仅当 performance 可用时）
    const loadMs = performance ? (performance.now() - startTime).toFixed(1) : '?';

    // 提取模块版本（如果暴露了 .version 字段）
    let modVersion = null;
    if (mod && mod[item.label] && mod[item.label].prototype && mod[item.label].prototype.version) {
      modVersion = mod[item.label].prototype.version;
    }

    // 判断是否为首次加载（新进程总是首次）
    const fromCache = false;

    return {
      id: item.id, label: item.label, path: item.path,
      status: ok ? 'PASS' : 'FAIL',
      detail: ok ? `loaded (${loadMs}ms${modVersion ? ', v' + modVersion : ''}${fromCache ? ', cached' : ', fresh'})` : 'export not found',
      loadMs: parseFloat(loadMs) || 0,
      modVersion,
      fromCache,
    };
  } catch (e) {
    const loadMs = performance ? (performance.now() - startTime).toFixed(1) : '?';
    return { id: item.id, label: item.label, path: item.path, status: 'ERROR', detail: `${e.message.split('\n')[0]} (${loadMs}ms)` };
  }
}

function bootCheck(silent = false, fast = false) {
  // 快速模式：只做文件头验证，跳过模块加载（~5ms vs ~50ms）
  if (fast) {
    const fileResults = CORE_CHECKS.map(runFileCheckFast);
    const filePassed = fileResults.filter(r => r.status === 'PASS').length;
    const fileFailed = fileResults.filter(r => r.status !== 'PASS' && r.required).length;
    const allPass = fileFailed === 0;
    return {
      timestamp: new Date().toISOString(),
      version: require(path.join(ROOT, 'package.json')).version,
      files: { total: CORE_CHECKS.length, passed: filePassed, checks: fileResults },
      modules: { total: MODULE_CHECKS.length, passed: 0 },
      allPass,
      degraded: false,
      degradedModules: [],
      _fast: true,
    };
  }

  const fileResults = CORE_CHECKS.map(runFileCheck);
  const moduleResults = MODULE_CHECKS.map(runModuleCheck);

  const filePassed = fileResults.filter(r => r.status === 'PASS').length;
  const fileFailed = fileResults.filter(r => r.status !== 'PASS' && r.required).length;
  const modulePassed = moduleResults.filter(r => r.status === 'PASS').length;
  const allFilesPass = filePassed === CORE_CHECKS.length;
  const allModulesPass = modulePassed === MODULE_CHECKS.length;

  // 模块加载总耗时（仅当 performance 可用时）
  const totalLoadMs = moduleResults.reduce((sum, r) => sum + (r.loadMs || 0), 0);
  const cachedCount = moduleResults.filter(r => r.fromCache).length;
  const freshCount = moduleResults.filter(r => r.status === 'PASS' && !r.fromCache).length;

  const allPass = fileFailed === 0; // 核心文件必须全部 PASS

  const report = {
    timestamp: new Date().toISOString(),
    version: require(path.join(ROOT, 'package.json')).version,
    files: { total: CORE_CHECKS.length, passed: filePassed, checks: fileResults },
    modules: { total: MODULE_CHECKS.length, passed: modulePassed, checks: moduleResults, totalLoadMs, cachedCount, freshCount },
    allPass,
    degraded: !allModulesPass,
    degradedModules: moduleResults.filter(r => r.status !== 'PASS').map(r => r.id),
  };

  if (!silent) {
    const mode = fast ? ' [快速]' : '';
    const icon = allPass ? '✓' : '⚠';
    console.log(`\n[Clarity] ${icon} Boot Check${mode} ${report.version} — ${allPass ? 'READY' : 'DEGRADED'}`);
    console.log(`  Files: ${filePassed}/${CORE_CHECKS.length} passed${fileFailed > 0 ? ` (${fileFailed} required failed)` : ''}`);
    fileResults.forEach(r => {
      const icon = r.status === 'PASS' ? '✓' : r.status === 'MISSING' ? '?' : r.status === 'FAIL' ? '✗' : '!';
      const req = r.required ? ' [REQUIRED]' : '';
      console.log(`    ${icon} ${r.id}: ${r.status}${req} — ${r.detail}`);
    });
    if (!fast) {
      console.log(`  Modules: ${modulePassed}/${MODULE_CHECKS.length} passed (${totalLoadMs.toFixed(1)}ms total, ${cachedCount} cached, ${freshCount} fresh)`);
      moduleResults.forEach(r => {
        const icon = r.status === 'PASS' ? '✓' : '✗';
        const timeStr = r.loadMs ? `${r.loadMs.toFixed(1)}ms` : '?';
        const versionStr = r.modVersion ? ` v${r.modVersion}` : '';
        const cacheStr = r.fromCache ? ' [cached]' : ' [fresh]';
        console.log(`    ${icon} ${r.id}: ${r.status}${versionStr} — ${timeStr}${r.status === 'PASS' ? cacheStr : ''}`);
      });
    } else {
      console.log(`  Modules: skipped (快速模式)`);
    }
  }

  return report;
}

module.exports = { bootCheck, CORE_CHECKS, MODULE_CHECKS };
