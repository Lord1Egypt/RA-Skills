/**
 * path-guard.js — [AUDIT-FIX M-03] 文件路径安全校验
 * 防止路径遍历攻击，确保所有 fs 写入在允许目录内
 */

const path = require('path');

// 允许的根目录（读）
// [v6.0.52 M2-followup] 把项目自身根目录纳入白名单：心虫读写 VERSION/config/formulas/memory/src 等自身文件属合法操作，
// 仅拦截越界到项目外的路径（/etc /home /root 等）。原白名单只含 data/tmp，导致正常文件全被判越界（warn 刷屏 / enforce 崩溃）。
// [v6.5.5 AUDIT-FIX P2-3] 读允许项目根；写操作额外受限（见 WRITE_DENY_PREFIXES），禁止覆盖源码/配置/可执行文件
const PROJECT_ROOT = path.resolve(__dirname, '..', '..'); // src/core -> 项目根
const _os = require('os');
const _homeHeartflow = path.resolve(_os.homedir(), '.heartflow');
const _homeHermesHeartflow = path.resolve(_os.homedir(), '.hermes', 'heartflow');
const ALLOWED_ROOTS = [
  PROJECT_ROOT,
  _homeHeartflow,                                   // [v6.0.53 N1] 部署数据目录 ~/.heartflow（M2 尾巴）
  _homeHermesHeartflow,                             // [v6.2.3] 实际运行时路径 ~/.hermes/heartflow（审计 M-3）
  path.resolve(process.cwd(), 'data'),
  path.resolve(process.cwd(), 'tmp'),
  path.resolve('/tmp'),
];

// [v6.5.5 AUDIT-FIX P2-3] 写操作禁止覆盖的路径前缀/后缀（防意外或恶意覆盖引擎源码与配置）
// 读操作不受此限制（心虫需读 src/ config/ 等自身文件）；写操作仅允许 data/tmp/显式数据目录及 .enc/.jsonl 记忆文件
const WRITE_DENY_PREFIXES = [
  path.join(PROJECT_ROOT, 'src'),
  path.join(PROJECT_ROOT, 'bin'),
  path.join(PROJECT_ROOT, 'mcp'),
  path.join(PROJECT_ROOT, 'scripts'),
  path.join(PROJECT_ROOT, 'config'),
];
const WRITE_DENY_SUFFIXES = ['.js', '.py', '.ts', '.json', '.md', '.yaml', '.yml', '.toml'];
// 允许写的记忆/数据文件后缀（位于允许根内的 data 目录）
const WRITE_ALLOW_SUFFIXES = ['.enc', '.jsonl', '.txt', '.log', '.csv'];

/**
 * 校验文件路径安全性（读）
 * @param {string} filePath - 待校验路径
 * @param {string[]} [extraRoots] - 额外允许的根目录
 * @returns {{ safe: boolean, resolved: string, reason?: string }}
 */
function guardPath(filePath, extraRoots = []) {
  if (!filePath || typeof filePath !== 'string') {
    return { safe: false, resolved: '', reason: 'path must be a non-empty string' };
  }
  
  const resolved = path.resolve(filePath);
  const roots = [...ALLOWED_ROOTS, ...extraRoots.map(r => path.resolve(r))];
  
  // 检查路径遍历（path.resolve 已规范化 ..，此处为防御性保留）
  if (resolved.includes('..')) {
    return { safe: false, resolved, reason: 'path traversal detected' };
  }

  // 检查是否在允许目录内（真正的安全防线）
  const allowed = roots.some(root => resolved.startsWith(root + path.sep) || resolved === root);
  if (!allowed) {
    return { safe: false, resolved, reason: `path outside allowed roots: ${resolved}` };
  }
  
  return { safe: true, resolved };
}

/**
 * 校验写操作的额外限制（防覆盖源码/配置）
 * @param {string} resolvedPath - 已通过 guardPath 的绝对路径
 * @returns {{ safe: boolean, reason?: string }}
 */
function guardWritePath(resolvedPath) {
  // 拒绝写受保护的源码/配置目录
  for (const denyPrefix of WRITE_DENY_PREFIXES) {
    if (resolvedPath.startsWith(denyPrefix + path.sep) || resolvedPath === denyPrefix) {
      return { safe: false, reason: `write to protected path denied: ${resolvedPath}` };
    }
  }
  // 拒绝写可执行/配置类后缀（除非是允许的记忆数据后缀）
  const ext = path.extname(resolvedPath).toLowerCase();
  if (WRITE_DENY_SUFFIXES.includes(ext) && !WRITE_ALLOW_SUFFIXES.includes(ext)) {
    return { safe: false, reason: `write to ${ext} file denied (protected suffix): ${resolvedPath}` };
  }
  return { safe: true };
}

/**
 * 安全的 fs.writeFileSync 包装
 */
function safeWriteSync(filePath, content, encoding = 'utf8', extraRoots = []) {
  const { safe, resolved, reason } = guardPath(filePath, extraRoots);
  if (!safe) throw new Error(`path-guard: ${reason}`);
  const wguard = guardWritePath(resolved);
  if (!wguard.safe) throw new Error(`path-guard: ${wguard.reason}`);
  const fs = require('../utils/safe-fs');
  return fs.writeFileSync(resolved, content, encoding);
}

/**
 * 安全的 fs.readFileSync 包装
 */
function safeReadSync(filePath, encoding = 'utf8', extraRoots = []) {
  const { safe, resolved, reason } = guardPath(filePath, extraRoots);
  if (!safe) throw new Error(`path-guard: ${reason}`);
  const fs = require('../utils/safe-fs');
  return fs.readFileSync(resolved, encoding);
}

module.exports = { guardPath, guardWritePath, safeWriteSync, safeReadSync, ALLOWED_ROOTS };
