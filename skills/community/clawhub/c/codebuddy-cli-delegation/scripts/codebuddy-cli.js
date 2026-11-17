#!/usr/bin/env node
/**
 * 干净环境启动「独立 CodeBuddy CLI」—— 不要直接跑裸命令。
 *
 * 为什么存在这个文件：
 *   Agent 宿主（WorkBuddy / VS Code 扩展 / 桌面端）向子进程注入一批环境变量，
 *   其中两类致命，会让独立 CLI 挂死不退出（0 字节输出、300s 无反应）：
 *     ① *_SERVICE_PROXY_URL / SERVER__PORT
 *        CLI 会去 bind 宿主已占用的端口 → EADDRINUSE 未捕获异常 → 永久挂死
 *     ② *_CONFIG_DIR / 产品身份变量（如 ACC_PRODUCT_CONFIG_PATH）
 *        CLI 会读宿主的配置目录与凭据 → 技能错位 / 假报「未登录」（但其实登录着）
 *
 * 为什么用 Node 而不是 shell：
 *   ① 跨平台：Windows / macOS / Linux 同一个文件，process.platform 分流即可
 *   ② 装了 CodeBuddy CLI 就必然有 Node（它本身就是 Node 应用，入口带 #!/usr/bin/env node）
 *      ⇒ 「有 Node」这个前提是白送的，不用额外探测
 *   ③ 白名单友好：SkillHub 上传只允许 .md/.txt/.json/.yaml/.yml/.js/.cjs/.mjs/
 *      .ts/.py/.sh/.png/.jpg/.svg —— .js 在内，.ps1/.bat/.cmd 都不在
 *   ④ 不受 shell 方言/ 编码陷阱影响（前几轮在 .sh/.ps1 上踩过 UTF-8 BOM、
 *      路径语义、sed 静默失效等坑，见 SKILL.md 的「各平台特有坑」）
 *
 * 用法：
 *   node scripts/codebuddy-cli.js -p "你的指令" --model hy3 --effort high
 *   或先chmod +x 再直接 ./codebuddy-cli.js -p "..."
 *
 * 所有参数原样透传给 CLI。
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

// ── ① 剥离宿主注入的环境变量 ────────────────────────────────────────────
const PREFIXES = ['CODEBUDDY_', 'WORKBUDDY_', 'CLIENT_INFO_'];
// 不带前缀、但落在 CLI 环境白名单里的一组（最容易漏）
const EXACT = [
  'NODE_OPTIONS',
  'SANDBOX_CENTER_IPC_ADDRESS',
  'SERVER__PORT',
  'SERVER__HOST',
  'ACC_PRODUCT_CONFIG_PATH',
  'ACC_PRODUCT_CONFIG',
  'ACC_PRODUCT_CONFIG_V2',
  'ACC_PRODUCT_CONFIG_V3',
  'CLAUDE_SESSION_ID',
  'CODEBUDDY_CONVERSATION_MESSAGE_ID',
  'CODEBUDDY_CONVERSATION_REQUEST_ID',
  'CODEBUDDY_TOOL_CALL_ID',
];

// 剥离规则的唯一例外：这是「指向一个 bash 可执行文件」的路径提示，不含端口 / 配置目录 /
// 产品身份，正是本脚本在 ② 里自己要设置的变量。宿主若已给了**真实存在**的路径，直接沿用
// （比重新探测更准 —— 便携版 Git / 用户目录自装 / conda 环境这类非标准位置探测不到）；
// 不存在（陈旧、或从别的机器复制来的）则丢弃，交给 ② 自行探测。
const KEEP_IF_EXISTS = 'CODEBUDDY_CODE_GIT_BASH_PATH';

const cleanEnv = Object.assign({}, process.env);
for (const key of Object.keys(cleanEnv)) {
  if (key === KEEP_IF_EXISTS) continue;
  if (PREFIXES.some((p) => key.startsWith(p)) || EXACT.includes(key)) {
    delete cleanEnv[key];
  }
}
// 例外变量仍须过存在性校验：只有「CLI 真能用上」的才留
if (cleanEnv[KEEP_IF_EXISTS] && !fs.existsSync(cleanEnv[KEEP_IF_EXISTS])) {
  delete cleanEnv[KEEP_IF_EXISTS];
}

// ── ② Windows：让 CLI 走 Git Bash 而不是退化成 PowerShell ──────────────
// 策略：① PATH 里找 bash.exe（最稳，装在哪都命中）
//       ② 兜底扫几个常见的 Git for Windows 安装根（含非 C 盘）
// 注意：不能只试 C:\Program Files —— 实测存在装在 D 盘等其它盘符的机器。
// ⚠️ 守卫 MUST 与上面 ① 操作**同一个对象**（cleanEnv）。历史 bug：剥离改的是 cleanEnv，
//    守卫却读 process.env ⇒ 宿主已注入该变量时整块探测被跳过，而该变量又已被剥离，
//    两个来源同时落空 ⇒ CLI 只能自行探测并失败 → stderr 提示 Git Bash not detected。
if (process.platform === 'win32' && !cleanEnv.CODEBUDDY_CODE_GIT_BASH_PATH) {
  const isWinBash = (p) => /[\\/]bash\.exe$/i.test(p);

  // ① 先扫 PATH（纯 fs 操作，无进程派生）
  const pathDirs = (process.env.PATH || '').split(path.delimiter).filter(Boolean);
  for (const dir of pathDirs) {
    for (const rel of [path.join('bin', 'bash.exe'), path.join('usr', 'bin', 'bash.exe')]) {
      const p = path.join(dir, rel);
      if (fs.existsSync(p)) {
        cleanEnv.CODEBUDDY_CODE_GIT_BASH_PATH = p;
        break;
      }
    }
    if (cleanEnv.CODEBUDDY_CODE_GIT_BASH_PATH) break;
  }

  // ② 兜底：各盘根下的常见安装位置
  if (!cleanEnv.CODEBUDDY_CODE_GIT_BASH_PATH) {
    const roots = [];
    for (const base of [process.env.ProgramFiles, process.env['ProgramFiles(x86)'], process.env.LOCALAPPDATA]) {
      if (base) roots.push(base);
    }
    // Git for Windows 常装在非系统盘（如 D:\Program Files\Git）
    for (const drive of 'CDEFG') roots.push(`${drive}:\\Program Files`);

    const rels = [
      path.join('Git', 'bin', 'bash.exe'),
      path.join('Git', 'usr', 'bin', 'bash.exe'),
      path.join('Programs', 'Git', 'bin', 'bash.exe'),
    ];
    outer: for (const root of roots) {
      for (const rel of rels) {
        const p = path.join(root, rel);
        if (fs.existsSync(p)) {
          cleanEnv.CODEBUDDY_CODE_GIT_BASH_PATH = p;
          break outer;
        }
      }
    }
  }

  // ③ 兜底：PATH 上任何目录里的 bash.exe
  if (!cleanEnv.CODEBUDDY_CODE_GIT_BASH_PATH) {
    for (const dir of pathDirs) {
      try {
        for (const f of fs.readdirSync(dir)) {
          const p = path.join(dir, f);
          if (isWinBash(p) && fs.statSync(p).isFile()) {
            cleanEnv.CODEBUDDY_CODE_GIT_BASH_PATH = p;
            break;
          }
        }
      } catch (_) { /* 不可访问目录跳过 */ }
      if (cleanEnv.CODEBUDDY_CODE_GIT_BASH_PATH) break;
    }
  }
}

// ── ③ 定位 CodeBuddy CLI ───────────────────────────────────────────────
// 策略（按可靠性）：
//   1. 环境变量 CODEBUDDY_CLI_ENTRY 显式指定
//   2. PATH 上有 codebuddy / codebuddy-code → 用它
//   3. 从 wrapper 所在目录反推真实 js 入口（npm 生成的 wrapper 内容形如
//      "%dp0%/node_modules/@tencent-ai/codebuddy-code/bin/codebuddy"，
//      相对自身解析 ⇒ 与「谁在跑 npm」无关，比问 npm root -g 可靠）
//   4. 兜底问 npm root -g
const PKG_SUBPATH = path.join(
  'node_modules', '@tencent-ai', 'codebuddy-code', 'bin', 'codebuddy'
);

function fromWrapper(wrapperPath) {
  // 向上两级找 packageRoot（<prefix>/bin/codebuddy 或 <prefix>/codebuddy）
  const dir = path.dirname(wrapperPath);
  const candidates = [
    path.join(dir, PKG_SUBPATH),                    // <prefix>/<...>
    path.join(dir, '..', PKG_SUBPATH),              // <prefix>/bin/../<...>
  ];
  return candidates.find((p) => fs.existsSync(p)) || null;
}

// 兜底：扫几个npm 全局安装的常见位置。
// ⚠️ 不用 `npm root -g` 命令 —— 它需要进程派生（Windows 上实测 EBUSY），
//    而且它随「当前用哪个 npm」而变（干净环境下常指向另一个 node 的目录）。
//    这些是 npm 的标准落点，直接 fs 探测更稳。
function fromNpmRoot() {
  const roots = [];
  if (process.env.npm_config_prefix) roots.push(process.env.npm_config_prefix);
  if (process.env.APPDATA) roots.push(path.join(process.env.APPDATA, 'npm'));
  if (process.env.HOME) {
    roots.push(path.join(process.env.HOME, '.npm-global'));
    roots.push(path.join(process.env.HOME, '.local'));
  }
  roots.push('/usr/local/lib/node_modules');
  roots.push('/opt/homebrew/lib/node_modules');
  if (process.env.HOME) roots.push(path.join(process.env.HOME, '.nvm', 'current', 'lib', 'node_modules'));

  for (const root of roots) {
    const p = path.join(root, '@tencent-ai', 'codebuddy-code', 'bin', 'codebuddy');
    if (fs.existsSync(p)) return p;
  }
  return null;
}

// ⚠️ 不要用 `where` / `command -v` 去找 codebuddy：
//   实测在Windows 上 spawnSync(cmd.exe, ['/c','where',...]) 会返回 EBUSY
//   （宿主沙箱/安全策略会拦「进程派生另一个进程」）；
//   而 Node 自己按 PATH 逐目录探测纯fs 操作，不会触发任何进程派生，最稳。
//   代价是要注意 PATHEXT（Windows 上命令是 codebuddy.cmd / .exe，不是无扩展名那个）。
function which(name) {
  const isWin = process.platform === 'win32';
  const dirs = (process.env.PATH || '').split(path.delimiter).filter(Boolean);
  const exts = isWin
    ? (process.env.PATHEXT || '.COM;.EXE;.BAT;.CMD').split(';')
    : [''];
  const bases = isWin ? [name, ...exts.map((e) => name + e.toLowerCase())] : [name];

  for (const dir of dirs) {
    for (const base of bases) {
      const p = path.join(dir, base);
      try {
        if (fs.existsSync(p) && fs.statSync(p).isFile()) return p;
      } catch (_) { /* 不可访问的目录直接跳过 */ }
    }
  }
  return null;
}

// ⚠️ MSYS / Git Bash 下 which 返回的是 /d/DevelopEnvironment/... 这种形式，
//    而 Node 的 fs.existsSync 认不了 ⇒ 必须归一化成 Windows 盘符形式，
//    否则「文件明明在」但探测结果为false。这是 .js 版独有的跨平台坑。
function toNativePath(p) {
  if (!p) return p;
  if (process.platform !== 'win32') return p;
  if (/^[A-Za-z]:[\\/]/.test(p)) return p;                 // 已是盘符形式
  const m = /^\/([A-Za-z])\/(.*)$/.exec(p);                // /d/xxx
  if (m) return m[1].toUpperCase() + ':\\' + m[2].replace(/\//g, '\\');
  return p;
}

function locate() {
  if (process.env.CODEBUDDY_CLI_ENTRY) {
    return process.env.CODEBUDDY_CLI_ENTRY;
  }
  for (const name of ['codebuddy', 'codebuddy-code']) {
    const w = which(name);
    if (w) {
      const native = toNativePath(w);
      const real = fromWrapper(native) || fromWrapper(w);
      // 找到真实 js 入口就用它（交给 node 跑）；否则直接用 wrapper
      return real || native;
    }
  }
  return fromNpmRoot();
}

const entry = locate();
if (!entry) {
  process.stderr.write(
    '找不到 CodeBuddy CLI。\n' +
    '  安装：npm install -g @tencent-ai/codebuddy-code\n' +
    '  或设环境变量 CODEBUDDY_CLI_ENTRY=<真实路径>/bin/codebuddy\n'
  );
  process.exit(127);
}

// ── ④ 组装参数并启动 ────────────────────────────────────────────────────

// 参数风格翻译：让本脚本同时接受「PowerShell 习惯的具名参数」与「CLI 原生短/长参数」。
// 起因：.ps1 版用 -Prompt/-Model/-Effort，.js 版原样透传，导致两种写法混用时报
//      "error: unknown option '-Prompt'" —— 纯透传对 PowerShell 用户不友好。
// 这里只翻译 CLI 认识的那几个，未识别的参数原样透传（未来 CLI 新增参数仍可用）。
const ALIAS = {
  '-Prompt': '-p',
  '-prompt': '-p',
  '-Model': '--model',
  '-model': '--model',
  '-Effort': '--effort',
  '-effort': '--effort',
  '-MaxTurns': '--max-turns',
  '-Max-turns': '--max-turns',
  '-OutputFormat': '--output-format',
  '-Output-format': '--output-format',
  '-PermissionMode': '--permission-mode',
  '-permission-mode': '--permission-mode',
};

const raw = process.argv.slice(2);
const passthrough = [];
for (const a of raw) {
  // 只翻译独立的参数项（不带值），避免误改用户的提示词内容
  passthrough.push(Object.prototype.hasOwnProperty.call(ALIAS, a) ? ALIAS[a] : a);
}

// 只加载项目级设置（project），避开用户级 hooks 在无头运行下掐死进程（见 SKILL.md §四）
const args = ['--setting-sources', 'project', ...passthrough];

// bootstrap 与本脚本同目录；存在时把技能约定追加进 system prompt
const bootstrap = path.join(__dirname, 'skills-bootstrap.md');
if (fs.existsSync(bootstrap)) {
  args.push('--append-system-prompt', fs.readFileSync(bootstrap, 'utf8'));
}

const r = spawnSync(process.execPath, [entry, ...args], {
  stdio: 'inherit',
  env: cleanEnv,
});

if (r.error) {
  process.stderr.write('启动 CodeBuddy CLI 失败：' + r.error.message + '\n');
  process.exit(1);
}
process.exit(r.status === null ? 1 : r.status);