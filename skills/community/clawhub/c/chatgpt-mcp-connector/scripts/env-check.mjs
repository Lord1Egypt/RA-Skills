#!/usr/bin/env node
/**
 * 环境自检 + 一键补齐（DevSpace × ChatGPT MCP 接入的前置依赖）
 *
 * 用法：
 *   node env-check.mjs                # 只读自检，打印结果 + 缺失项的安装命令
 *   node env-check.mjs --install      # 自检后，用系统包管理器安装缺失项
 *   node env-check.mjs --json         # 机器可读输出（给 agent 解析）
 *   node env-check.mjs --only node,git  # 配合 --install，只装指定项
 *
 * 检查项：Node / npm / Git / Bash / Tailscale / DevSpace / better-sqlite3 / 包管理器
 *
 * ⚠️ Bash 这一项特意做得比其他项重 —— 因为它是唯一会「静默假绿」的检查：
 *   前几版只按「推荐顺序」列出找到的 bash，于是 Git 装在 D 盘时它会报 ok，
 *   而 DevSpace 实际用的是 `C:\Windows\System32\bash.exe`（WSL 启动器，不是 shell），
 *   在 ChatGPT 那边表现为「bash 接口持续异常」、连 `echo` 都失败。
 *   现在改成：**复刻 DevSpace 真实的解析顺序**（resolveDevspaceBash），以它的结果为准，
 *   并对非 WSL 的 bash 真跑一条命令做冒烟测试（smokeTestBash）。
 *   详见 resolveDevspaceBash() 的注释与 references/cross-platform.md 第二节。
 *
 * 跨平台：Windows / macOS / Linux 都能跑。三平台的差异集中在三处，脚本里都按平台分支处理了 ——
 *   1. 依赖安装方式：winget ｜ brew / port ｜ apt-get / dnf / yum / pacman / zypper / apk
 *   2. shell 解析：Windows 上 DevSpace 强制要 Git Bash（没有兜底）；macOS/Linux 优先 /bin/bash，
 *      找不到会退化成 /bin/sh（所以那时只报警告，不报缺失）
 *   3. Tailscale 的服务模型：Windows 托盘程序 ｜ macOS 菜单栏 App ｜ Linux systemd 守护进程 + --operator
 * 细节见 references/cross-platform.md。
 *
 * ⚠️ 安全约定：默认【不安装任何东西】。只有显式传 --install 才会执行安装命令。
 *    在 agent 场景里，调用方应先跑一次自检、把结果给用户看、征得同意后再加 --install。
 *
 * 容错约定：
 *   - 每项检查独立 try/catch：单项炸掉不影响其他项，也不影响整体出报告。
 *   - 所有外部命令**带超时**（探测 15s / 安装 10min）——挂住的命令会拖死整个自检。
 *   - 只对可恢复失败重试（网络抖动）；ENOENT / EACCES 直接放弃，不浪费时间。
 *   - --install 时单项失败**不中断整轮**，最后统一汇总成功/失败/需手动。
 *   - 退出码反映**自检时**的状态；刚装完但 PATH 未刷新仍返回 1（不报假绿）。
 *
 * 人工介入提醒：
 *   - 部分环节**脚本代替不了**（典型：`tailscale up` 要用户去浏览器授权）。
 *     检测到这类情况时会置 `needsUserAction`，并在最后单独汇总一次 🙋 清单，
 *     方便 agent 明确「该停下来让用户做什么」，而不是自己干等。
 *
 * 退出码：0 = 全部就绪；1 = 有缺失项；2 = 脚本自身出错
 */

import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { existsSync, readFileSync, statSync } from 'node:fs';
import { delimiter, dirname, join } from 'node:path';

const IS_WIN = process.platform === 'win32';
const IS_MAC = process.platform === 'darwin';

// ── 容错：超时上限 ──
// 外部命令挂住会拖死整个自检（agent 场景下表现为任务永不返回）。
// 实测 winget 首次使用、tailscale 未登录、损坏的 bash shim 都可能卡住等输入。
const TIMEOUT_PROBE = 15000; // 版本探测这类快命令
const TIMEOUT_INSTALL = 600000; // npm install / rebuild 可能跑几分钟

const args = process.argv.slice(2);
const WANT_INSTALL = args.includes('--install');
const WANT_JSON = args.includes('--json');
const onlyIdx = args.indexOf('--only');
const ONLY = onlyIdx >= 0 && args[onlyIdx + 1] ? args[onlyIdx + 1].split(',').map((s) => s.trim()) : null;

// ─────────────────────────── 工具函数 ───────────────────────────

/**
 * 执行外部命令（带超时 + 可选重试）。
 *
 * Windows 上 Node 不允许直接 spawn .cmd/.bat（会 EINVAL），必须走 shell；
 * 而 shell 模式下 Node 只是把 cmd + args 用空格拼起来、**不会给带空格的路径加引号**，
 * 于是 "C:\Program Files\...\npm.cmd" 会被从空格处截断。所以这里手动加引号。
 *
 * 容错约定：只对「网络抖动 / 临时占用」这类可恢复失败重试；
 * ENOENT（命令不存在）、EACCES（权限拒绝）重试纯属浪费，直接跳出。
 *
 * @param {string} cmd
 * @param {string[]} [cmdArgs]
 * @param {{timeout?: number, retries?: number}} [opts]
 */
function tryExec(cmd, cmdArgs = ['--version'], opts = {}) {
  const timeout = opts.timeout ?? TIMEOUT_PROBE;
  const retries = opts.retries ?? 0;
  const needsShell = IS_WIN && /\.(cmd|bat)$/i.test(cmd);
  const launch = needsShell ? `"${cmd}"` : cmd;

  let last = null;
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const out = execFileSync(launch, cmdArgs, {
        encoding: 'utf8',
        stdio: ['ignore', 'pipe', 'pipe'],
        windowsHide: true,
        shell: needsShell,
        timeout,
        killSignal: 'SIGKILL',
      });
      return { ok: true, out: String(out).trim(), attempts: attempt + 1 };
    } catch (e) {
      last = e;
      if (e?.code === 'ENOENT' || e?.code === 'EACCES' || e?.code === 'EPERM') break;
    }
  }
  const timedOut = last?.code === 'ETIMEDOUT' || last?.killed === true || last?.signal === 'SIGKILL';
  return { ok: false, err: last, timedOut, attempts: retries + 1 };
}

/** 把 execSync 抛出的错误压成一行可读文本（用于日志/JSON，避免整段堆栈）。 */
function errLine(e) {
  if (!e) return '(无错误对象)';
  if (e.code === 'ETIMEDOUT' || e.killed) return `超时（超过 ${TIMEOUT_PROBE}ms 未返回）`;
  const raw = e.stderr ? String(e.stderr) : String(e.message || e);
  return raw.split('\n').map((s) => s.trim()).filter(Boolean)[0]?.slice(0, 200) || '(无输出)';
}

/**
 * 定位 npm。
 * 必须优先取「当前 Node 同目录」的 npm —— 否则 PATH 里若混有其它 Node 发行版
 * （如某工具自带的运行时），会拿到那个 npm 及其 global root，导致 DevSpace 定位错包。
 */
function npmBin() {
  const adjacent = join(dirname(process.execPath), IS_WIN ? 'npm.cmd' : 'npm');
  if (existsSync(adjacent)) return adjacent;
  return which(IS_WIN ? 'npm.cmd' : 'npm') || which('npm');
}

/** 跨平台 which：在 PATH 里找可执行文件，返回绝对路径。 */
function which(name) {
  const pathEnv = process.env.PATH || '';
  const exts = IS_WIN ? (process.env.PATHEXT || '.EXE;.CMD;.BAT;.COM').split(';').filter(Boolean) : [''];
  for (const dir of pathEnv.split(delimiter).filter(Boolean)) {
    for (const ext of exts) {
      const p = join(dir, name + ext);
      try {
        if (existsSync(p) && statSync(p).isFile()) return p;
      } catch {
        /* 忽略无权限的目录 */
      }
    }
  }
  return null;
}

/** 在候选固定路径里找第一个存在的文件。 */
function firstExisting(paths) {
  for (const p of paths) if (p && existsSync(p)) return p;
  return null;
}

/**
 * 枚举 PATH 上**全部**同名可执行文件（不止第一个）。
 *
 * 走系统自带的查找命令：Windows `where`，macOS / Linux `which -a`。
 * 这是本 skill 的检查原则 —— **判断「装没装」要问系统，不要去看固定安装目录**。
 * 猜目录有两个毛病：① 只能覆盖你事先猜到的位置（Git 装在 D 盘、PortableGit、MSYS2 都会漏）；
 * ② 会把某一台机器的盘符布局写进公开代码里。
 */
function whichAll(name) {
  const out = [];
  const seen = new Set();
  const push = (p) => {
    const v = String(p || '').trim();
    if (!v) return;
    const k = v.toLowerCase();
    if (!seen.has(k)) { seen.add(k); out.push(v); }
  };

  // ① 问系统
  try {
    const r = tryExec(IS_WIN ? 'where' : 'which', IS_WIN ? [name] : ['-a', name], { timeout: TIMEOUT_PROBE });
    if (r.ok) String(r.out).split(/\r?\n/).forEach(push);
  } catch {
    /* 系统没有查找命令（极精简环境）→ 落到下面的 PATH 扫描 */
  }

  // ② 兜底：自己扫一遍 PATH（拿不到 `where` / `which` 的输出时才走这里）
  if (out.length === 0) push(which(name));
  return out;
}

/**
 * 从 PATH 上的每一个 `git` 反推同一份安装里的 Git Bash。
 *
 * Git for Windows 布局固定（`<root>\cmd\git.exe` 与 `<root>\bin\bash.exe` 并存），
 * 但入口不止一个（还有 `<root>\mingw64\bin\git.exe`），所以这里**不假设层级**，
 * 直接逐级向上找 `<祖先目录>\bin\bash.exe`。这样 Git 装在哪个盘都能找到，
 * 而脚本里一个盘符都不用写。
 */
function gitBashCandidates() {
  if (!IS_WIN) return [];
  const out = [];
  for (const gitExe of [...whichAll('git'), ...whichAll('git.exe')]) {
    let dir = dirname(gitExe);
    for (let i = 0; i < 4; i++) {
      const cand = join(dir, 'bin', 'bash.exe');
      if (existsSync(cand)) { out.push(cand); break; }
      const up = dirname(dir);
      if (up === dir || up === '.') break;
      dir = up;
    }
  }
  return out;
}

/**
 * 「约定位置」——**只**保留两类，且都不含盘符字面量：
 *   ① DevSpace 自己会去撞的那两个位置（`%ProgramFiles%\Git\bin`）—— 用来复刻它的行为，见 resolveDevspaceBash()；
 *   ② POSIX 的 `\/bin/bash` 之类标准位置。
 * 其余一律靠 whichAll() / gitBashCandidates() 从命令输出里拿。
 */
function conventionalBashPaths() {
  if (IS_WIN) {
    return [
      process.env.ProgramFiles && join(process.env.ProgramFiles, 'Git', 'bin', 'bash.exe'),
      process.env['ProgramFiles(x86)'] && join(process.env['ProgramFiles(x86)'], 'Git', 'bin', 'bash.exe'),
    ].filter(Boolean);
  }
  return [
    '/bin/bash',          // 绝大多数发行版与 macOS 的标配
    '/usr/bin/bash',
    '/opt/homebrew/bin/bash',  // Homebrew（Apple Silicon）
    '/usr/local/bin/bash',     // Homebrew（Intel）
    '/opt/local/bin/bash',     // MacPorts
  ];
}

function parseVersion(str) {
  const m = String(str || '').match(/(\d+)\.(\d+)(?:\.(\d+))?/);
  return m ? { major: +m[1], minor: +m[2], patch: +(m[3] || 0) } : null;
}

// ─────────────────────────── 各检查项 ───────────────────────────

/** Node：README 要求 >=22.19 <27；cli.js 的 assertSupportedNode 实际为 >=20.12 <27 */
function checkNode() {
  const v = process.versions.node;
  const p = parseVersion(v);
  const item = { id: 'node', name: 'Node.js', required: '>=20.12 <27（README 写 >=22.19 <27）', found: v, path: process.execPath };
  if (!p) { item.status = 'fail'; item.note = '无法解析版本'; return item; }
  if (p.major >= 27) {
    item.status = 'fail';
    item.note = `版本过高（需 <27）。当前 ${v}`;
  } else if (p.major < 20 || (p.major === 20 && p.minor < 12)) {
    item.status = 'fail';
    item.note = `版本过低（需 >=20.12）。当前 ${v}`;
  } else if (p.major === 22 && p.minor >= 19) {
    item.status = 'ok';
    item.note = '符合 README 推荐区间';
  } else if (p.major === 24) {
    item.status = 'ok';
    item.note = '可用（现为 LTS 线）';
  } else {
    item.status = 'warn';
    item.note = `可用但偏旧/非推荐线，建议 22.19+ 或 24 LTS。当前 ${v}`;
  }
  return item;
}

/** npm */
function checkNpm() {
  const bin = npmBin();
  const r = tryExec(bin || 'npm', ['--version']);
  const item = { id: 'npm', name: 'npm', required: '随 Node 安装', found: r.ok ? r.out.split('\n')[0] : null, path: bin };
  if (r.ok) { item.status = 'ok'; }
  else {
    item.status = 'fail';
    item.note = bin
      ? '找到了 npm 但执行失败（Windows 上 .cmd 需要 shell，已处理；仍失败则重装 Node）'
      : 'npm 不在 PATH（重装 Node 或修复 PATH）';
  }
  return item;
}

/** Git —— DevSpace 的 worktree 模式依赖；Windows 上 Git 同时提供 Git Bash */
function checkGit() {
  const bin = which('git') || which('git.exe');
  const r = tryExec(bin || 'git', ['--version']);
  const item = { id: 'git', name: 'Git', required: '任意（worktree 模式必需）', found: r.ok ? r.out : null, path: bin };
  if (r.ok) { item.status = 'ok'; }
  else { item.status = 'fail'; item.note = '未找到 git'; }
  return item;
}

/**
 * 判定「这个 bash 是不是遗留 WSL 启动器」。
 *
 * 与 DevSpace 源码 `pi-coding-agent/dist/utils/shell.js` 里的 `isLegacyWslBashPath()` 同款规则。
 * 这个判定很关键，因为 `C:\Windows\System32\bash.exe` **不是 shell**，它是个只负责转发给
 * `wsl.exe` 的启动器：不读 `-c` 参数、忽略命令内容，直接把 WSL 的错误吐回来。
 */
function isLegacyWslBash(p) {
  return /^[a-z]:\\windows\\(?:system32|sysnative)\\bash\.exe$/i.test(String(p).replace(/\//g, '\\'));
}

/** 微软商店版 WSL 的别名（`...\WindowsApps\bash.exe`）—— 同样是 WSL 入口，不是 shell。 */
function isStoreWslBash(p) {
  return /\\appdata\\local\\microsoft\\windowsapps\\/i.test(String(p).replace(/\//g, '\\'));
}

/**
 * 复刻 **DevSpace 真实的 shell 解析顺序**（源码 `utils/shell.js` → `getShellConfig()`）。
 *
 * 为什么必须单独复刻一遍：`checkBash()` 上面那个 candidates 列表是**给人看的推荐顺序**，
 * 而 DevSpace 只认自己那套死写的顺序，两者**并不等价**。Windows 上真正的顺序是：
 *
 *   ① `%ProgramFiles%\Git\bin\bash.exe`
 *   ② `%ProgramFiles(x86)%\Git\bin\bash.exe`
 *   ③ `where bash.exe` 的第一个命中
 *   ④ 都没有 → 抛 `No bash shell found`
 *
 * 它**不会**去扫 D:/E:/F: 盘。所以「Git for Windows 装在 D 盘」这种再正常不过的安装，
 * 会让 DevSpace 直接落到第 ③ 步 —— 而 `C:\Windows\System32` 在系统 PATH 里，
 * 系统 PATH 又排在用户 PATH 前面，于是命中 `System32\bash.exe`（WSL 启动器），
 * **所有命令必然失败**（`echo` 也一样，因为 shell 根本没起来）。
 *
 * 另外：`settings.json` 里的 `shellPath` 对 `serve` 的 `run_shell` **无效** ——
 * `dist/pi-tools.js` 调的是 `createBashTool(cwd)`，没传 options，所以拿不到 shellPath。
 * 也没有任何 `DEVSPACE_*` 环境变量能指定 shell。结论：**只能从「让真 bash 被找到」入手**。
 */
function resolveDevspaceBash() {
  if (!IS_WIN) {
    // macOS / Linux：/bin/bash 存在即用，根本不看版本
    if (existsSync('/bin/bash')) return { path: '/bin/bash', via: '固定优先 /bin/bash（存在即用）' };
    const onPath = which('bash');
    if (onPath) return { path: onPath, via: 'PATH 上的 bash（本机没有 /bin/bash）' };
    if (existsSync('/bin/sh')) {
      return { path: '/bin/sh', via: '兜底 /bin/sh', degraded: true };
    }
    return { path: null, via: '（找不到任何 shell）', missing: true };
  }

  // Windows 第 ①② 步：DevSpace 源码里就是**写死在 Program Files 下找**的，这里必须照抄，
  // 否则得出的结论会和它不一致。这是全脚本唯一一处「看目录」—— 因为要复刻的不是我们的判断，
  // 而是它自己的行为；路径由 %ProgramFiles% 环境变量推导，不含任何盘符字面量。
  const known = [];
  if (process.env.ProgramFiles) known.push(join(process.env.ProgramFiles, 'Git', 'bin', 'bash.exe'));
  if (process.env['ProgramFiles(x86)']) known.push(join(process.env['ProgramFiles(x86)'], 'Git', 'bin', 'bash.exe'));
  for (const p of known) {
    if (existsSync(p)) return { path: p, via: `固定位置 ${p}` };
  }

  // Windows 第 ③ 步：which() 按 PATH 顺序返回第一个命中，等价于 `where bash.exe` 的第一个
  const onPath = which('bash') || which('bash.exe');
  if (onPath) return { path: onPath, via: 'PATH 命中（= where bash.exe 的第一个）' };

  return { path: null, via: '（找不到任何 bash）', missing: true };
}

/**
 * 从 PATH 上的 `git.exe` 反推同一份安装里的 Git Bash。
 *
 * 这条推导比「猜常见安装盘」靠谱得多 —— 用户把 Git 装到哪个盘都能找到，
 * 而且不会把某一台机器的具体路径写死进脚本。实现复用 `gitBashCandidates()`，
 * 免得两个函数对「git.exe 在第几层」各有一套假设。
 */
function gitBashFromGitExe() {
  return gitBashCandidates()[0] ?? null;
}

/** 把 Windows 路径转成 Git Bash 里能直接用的写法（`D:\a\b` → `/d/a/b`）。 */
function toPosixPath(p) {
  return p.replace(/\\/g, '/').replace(/^([A-Za-z]):/, (_, d) => `/${d.toLowerCase()}`);
}

/**
 * 生成「怎么修」的具体命令。
 *
 * 刻意不写死任何盘符 —— 安装位置由 `gitBashPath` 推导（Git for Windows 布局固定，
 * `<root>\bin\bash.exe` 的上一层就是安装根）。找不到时给占位符，让人自己填。
 */
function bashFixHint(gitBashPath) {
  const root = gitBashPath ? dirname(dirname(gitBashPath)) : null;
  const binDir = root ? join(root, 'bin') : '<你的Git安装目录>\\bin';
  const gitRoot = root ?? '<你的Git安装目录>';
  const lines = [];
  lines.push('修法（按侵入性从低到高，任选其一）：');
  lines.push('  ① 临时：启动 serve 时把 Git 的 bin 前置到 PATH（无需管理员）——');
  lines.push(`     cmd:  set "PATH=${binDir};%PATH%" && devspace serve`);
  lines.push(`     bash: PATH="${toPosixPath(binDir)}:$PATH" devspace serve`);
  lines.push('  ② 一劳永逸：建目录 junction，让 DevSpace 的第 ① 步就能命中（需管理员开一个终端）——');
  lines.push(`     mklink /J "C:\\Program Files\\Git" "${gitRoot}"`);
  lines.push(`     （撤销：rmdir "C:\\Program Files\\Git" —— 只删链接，不动 ${gitRoot} 里的真身）`);
  lines.push('  ③ 又或者把 Git 的 bin 目录前置到【系统】PATH —— 必须是「系统变量」而不是「用户变量」，');
  lines.push('     因为系统 PATH 排在用户 PATH 前面，只加到用户变量里仍然会被 System32 抢先。');
  if (gitBashPath) {
    lines.push(`  另：本机确实存在可用的 Git Bash（${gitBashPath}），只是不在 DevSpace 会找的位置。`);
  } else {
    lines.push('  另：本机没找到可用的 Git Bash，先装一个 Git for Windows：winget install -e --id Git.Git');
  }
  return lines.join('\n');
}

/**
 * 冒烟测试：**真的**用这个 bash 跑一条命令，确认它不只是「文件存在」。
 *
 * 光看路径存在是不够的 —— 这次踩的 `System32\bash.exe` 文件就在那儿、`existsSync` 为真、
 * `--version` 也未必报错，但它根本不是 shell。只有真跑一条命令才能证明它活着，
 * 而这也正是 ChatGPT 那边 shell 工具能不能活的充要条件。
 *
 * 注意：**不要**拿 WSL 入口来做这个测试，那会拉起 wsl.exe（慢、且可能被安全策略拦截）。
 * 调用方要先排除 WSL 分支。
 */
function smokeTestBash(p) {
  try {
    const r = tryExec(p, ['-c', 'echo devspace-bash-ok'], { timeout: TIMEOUT_PROBE });
    return { ok: r.ok && String(r.out).includes('devspace-bash-ok'), detail: r.ok ? String(r.out).trim() : errLine(r.err) };
  } catch (e) {
    return { ok: false, detail: errLine(e) };
  }
}

/** Bash —— DevSpace 执行 shell 命令的硬性要求（纯 PowerShell / cmd 不支持） */
function checkBash() {
  const item = { id: 'bash', name: 'Bash', required: 'Bash 兼容 shell（Git Bash / WSL / MSYS2 / Cygwin）', found: null, path: null };

  // ── 候选从哪来：一律靠「跑命令」，不靠「猜目录」──
  //   ① PATH 上所有 bash：Windows `where bash.exe`，POSIX `which -a bash`
  //   ② 从 PATH 上每一个 `git` 反推出的 Git Bash（Git 装在哪个盘都找得到）
  //   ③ 约定位置：Windows 只留 DevSpace 自己会去撞的 `%ProgramFiles%\Git\bin`（见 resolveDevspaceBash）；
  //      POSIX 留 `/bin/bash` 等标准位置
  // 刻意不写死 C:/D:/E:/F: 这类盘符 —— 那样既查不全（漏 MSYS2、PortableGit、非 C 盘安装），
  // 又会把作者本机的盘符布局带进公开仓库。
  const candidates = [];
  const addCand = (p) => {
    if (p && !candidates.some((x) => x.toLowerCase() === String(p).toLowerCase())) candidates.push(p);
  };
  whichAll('bash').forEach(addCand);
  if (IS_WIN) {
    whichAll('bash.exe').forEach(addCand);
    gitBashCandidates().forEach(addCand);
    addCand(which('bash.exe'));
  } else {
    addCand(which('bash'));
  }
  conventionalBashPaths()
    .filter((p) => {
      try { return existsSync(p); } catch { return false; }
    })
    .forEach(addCand);

  // 分档：数值越小越推荐。这**只影响本脚本的展示顺序**，不决定 DevSpace 实际用哪个 bash ——
  // Windows 上 DevSpace 固定先找 %ProgramFiles%\Git\bin\bash.exe，找不到才扫 PATH；
  // macOS / Linux 上固定优先 /bin/bash，存在就用它，根本不会理我们排的名（见 references/cross-platform.md）。
  // 所以这里把 /bin/bash 排第一，是为了让「展示的那个」和「实际会用的那个」对得上。
  const classify = (p) => {
    const l = p.toLowerCase().replace(/\//g, '\\');
    // —— Windows ——
    if (l.includes('\\git\\bin\\bash')) return { flavor: 'Git Bash', rank: 1 };
    if (l.includes('msys64')) return { flavor: 'MSYS2', rank: 2 };
    if (l.includes('cygwin')) return { flavor: 'Cygwin', rank: 3 };
    if (l.includes('system32\\bash') || l.includes('\\wsl')) return { flavor: 'WSL（Windows Subsystem for Linux）', rank: 4, noExec: true };
    if (l.includes('portablegit')) return { flavor: 'PortableGit（某工具自带的副本）', rank: 9 };
    // —— macOS / Linux ——
    if (p === '/bin/bash') return { flavor: IS_MAC ? 'macOS 系统 Bash（3.2，对 DevSpace 足够）' : '系统 Bash（/bin/bash）', rank: 1 };
    if (p === '/usr/bin/bash') return { flavor: '系统 Bash（/usr/bin/bash）', rank: 2 };
    if (p.startsWith('/opt/homebrew/')) return { flavor: 'Homebrew Bash（Apple Silicon）', rank: 3 };
    if (p.startsWith('/usr/local/')) return { flavor: IS_MAC ? 'Homebrew Bash（Intel）/ 系统 path' : '/usr/local 下的 Bash', rank: 4 };
    if (p.startsWith('/opt/local/')) return { flavor: 'MacPorts Bash', rank: 5 };
    return { flavor: 'Bash', rank: 6 };
  };

  // candidates 里已经含「命令查出来的」+「约定位置」两类，且都已确认存在。
  // 这里不提前 break —— 把所有候选都摆出来，把判断权交给用户。
  const all = candidates.filter((c) => {
    try { return existsSync(c); } catch { return false; }
  });

  if (all.length === 0) {
    // macOS / Linux 上 DevSpace 找不到 bash 会**退化成 /bin/sh**（源码 utils/shell.js 的兜底分支），
    // 所以这里不该报「缺失」把整条流程拦下来 —— 降级成警告，并说清代价。
    // Windows 上没有任何兜底：找不到 bash 就直接抛 "No bash shell found"，shell 工具彻底不可用。
    if (!IS_WIN && existsSync('/bin/sh')) {
      item.status = 'warn';
      item.path = '/bin/sh';
      item.flavor = 'sh（退化兜底）';
      item.found = '（/bin/sh 存在）';
      item.note =
        '没有 bash，DevSpace 会退化成 /bin/sh 执行命令。多数命令仍可用，但 bash 专有语法（数组、`[[ ]]`、进程替换）会失败。' +
        '想补上：Debian/Ubuntu `sudo apt install bash`；Alpine `sudo apk add bash`；macOS `brew install bash`';
      return item;
    }
    item.status = 'fail';
    item.note = IS_WIN
      ? '未找到任何 Bash（`where bash.exe` 没命中，PATH 上也没有）。DevSpace 无法执行 shell 命令 —— ' +
        '装 Git for Windows 即可同时获得 Git + Git Bash；' +
        '若你用 MSYS2 / Cygwin，把它的 `usr\\bin` / `bin` 加进 PATH 后重跑自检'
      : '未找到 bash，也没有 /bin/sh 兜底（极精简容器里常见）。装 bash：Debian/Ubuntu `sudo apt install bash`；Alpine `sudo apk add bash`';
    return item;
  }

  const detailed = all
    .map((p) => {
      const { flavor, rank, noExec } = classify(p);
      let version = null;
      if (noExec) {
        // WSL 入口不要真的去执行：它会拉起 wsl.exe，可能被安全策略拦截，且代价高
        version = '（仅检测到入口，未执行）';
      } else {
        const r = tryExec(p, ['--version']);
        version = r.ok ? r.out.split('\n')[0] : '（执行失败）';
      }
      return { path: p, flavor, rank, version, noExec: !!noExec };
    })
    .sort((a, b) => a.rank - b.rank);

  const best = detailed[0];
  item.candidates = detailed;

  // ── 分界线：以上排序只是「给人看的推荐」，以下才是红黄绿的判据 ──
  // DevSpace 不读我们的推荐顺序，它只会按 getShellConfig() 那套死写顺序去解析。
  // 两者不一致时，必须以「DevSpace 实际会用的那个」为准，否则自检会亮假绿灯：
  // 典型场景 = Git 装在 D 盘（列表里排第一），DevSpace 却落到 System32 的 WSL 启动器上。
  const resolved = resolveDevspaceBash();
  item.devspaceUses = resolved.path;
  item.devspaceVia = resolved.via;
  const gitBashElsewhere = gitBashFromGitExe() ?? detailed.find((d) => d.flavor.startsWith('Git Bash') && !d.noExec)?.path ?? null;

  if (resolved.missing) {
    item.status = 'fail';
    item.path = null;
    item.found = null;
    item.note = IS_WIN
      ? '未找到任何 bash。DevSpace 每次执行 shell 命令都会抛 "No bash shell found" —— Windows 上没有任何兜底。装 Git for Windows 即可同时获得 Git + Git Bash'
      : '未找到 bash，也没有 /bin/sh 兜底（极精简容器里常见）。装 bash：Debian/Ubuntu `sudo apt install bash`；Alpine `sudo apk add bash`';
    return item;
  }

  // 把 item 的展示字段对齐到「实际会被用的那个」，而不是排序第一的那个
  const match = detailed.find((d) => d.path.toLowerCase() === resolved.path.toLowerCase());
  item.path = resolved.path;
  item.found = match ? match.version : '（未在候选列表中执行过）';

  const realPath = String(resolved.path).replace(/\//g, '\\');
  const resolvedIsLegacyWsl = IS_WIN && isLegacyWslBash(resolved.path);
  const resolvedIsStoreWsl = IS_WIN && isStoreWslBash(resolved.path);
  const resolvedIsGitBash = /\\git\\bin\\bash\.exe$/i.test(realPath);

  if (resolvedIsLegacyWsl || resolvedIsStoreWsl) {
    // 这是本脚本能抓到的**最恶劣的一种假绿**：明明装了 Git Bash，DevSpace 却用不上。
    item.status = 'fail';
    item.statusLabel = '[不可用]';
    if (gitBashElsewhere) item.noInstallSuggestion = true;
    item.flavor = 'WSL 入口 —— 不是 shell！';
    item.note =
      `DevSpace 会选中 ${resolved.path}（${resolved.via}），但那是 **WSL 启动器**而不是 shell：\n` +
      '  它不认 `-c` 参数、忽略命令内容，任何命令（连 `echo` 都算）都会立刻失败并返回乱码错误，\n' +
      '  在 ChatGPT 那边表现为「bash 接口持续异常」。\n' +
      '根因：Git Bash 没装在 `%ProgramFiles%\\Git` 下，DevSpace 的第 ① ② 步都落空，掉进第 ③ 步。\n' +
      bashFixHint(gitBashElsewhere);
    return item;
  }

  if (resolved.degraded) {
    item.status = 'warn';
    item.flavor = 'sh（退化兜底）';
    item.note =
      `没有 bash，DevSpace 会退化成 ${resolved.path} 执行命令。多数命令仍可用，` +
      '但 bash 专有语法（数组、`[[ ]]`、进程替换）会失败。' +
      '想补上：Debian/Ubuntu `sudo apt install bash`；Alpine `sudo apk add bash`；macOS `brew install bash`';
    return item;
  }

  if (/portablegit/i.test(realPath)) {
    item.status = 'warn';
    item.flavor = 'PortableGit（某工具自带的副本）';
    item.note =
      'DevSpace 会用一个 PortableGit 副本（通常是某个工具自带的精简分发）。' +
      '它可能缺 coreutils 或没把 `usr/bin` 放进 PATH，表现为「bash 能起来，但 `ls` / `grep` 报 command not found」——' +
      `和「shell 完全起不来」是两回事。建议另装官方 Git for Windows。${gitBashElsewhere ? `（本机另有可用的 Git Bash：${gitBashElsewhere}）` : ''}`;
    return item;
  }

  // 解析出来的既不是 WSL 入口也不是退化 sh —— 可以放心真跑一条命令来验证（不会拉起 wsl.exe）
  const smoke = smokeTestBash(resolved.path);
  if (!smoke.ok) {
    item.status = 'fail';
    item.statusLabel = '[不可用]';
    if (gitBashElsewhere) item.noInstallSuggestion = true;
    item.flavor = `${match?.flavor ?? 'Bash'} —— 文件在，但跑不起来`;
    item.note =
      `DevSpace 会选中 ${resolved.path}（${resolved.via}），但冒烟测试（跑一条 \`echo\`）失败：${smoke.detail}\n` +
      '说明这个 bash 起不来、或缺少必要组件（coreutils 缺失 / PATH 没配好）。ChatGPT 那边的 shell 工具会同样全废。\n' +
      bashFixHint(gitBashElsewhere);
    return item;
  }

  item.status = 'ok';
  item.flavor = resolvedIsGitBash ? 'Git Bash' : (match?.flavor ?? 'Bash');
  item.note = `${item.flavor}（冒烟测试通过）`;
  // 排序第一的 ≠ 实际会用的：说清楚，免得用户以为自检在讲另一个 bash
  if (best.path && best.path.toLowerCase() !== resolved.path.toLowerCase() && !best.noExec) {
    item.note += `；⚠️ 注意 DevSpace 实际会用 ${resolved.path}，而不是列表里排第一的 ${best.path}`;
  }
  if (detailed.length > 1) item.note += `；共发现 ${detailed.length} 个 Bash（见下方列表）`;
  return item;
}

/**
 * Tailscale 未运行 / 未登录时的处置建议。
 *
 * 三个平台的**服务模型都不一样**，不能一句话打发：
 *   Windows —— 客户端是常驻托盘程序，登录靠它自己弹浏览器；
 *   macOS   —— 是 GUI App（菜单栏图标），CLI 还可能藏在 app bundle 里不在 PATH；
 *   Linux   —— 是 systemd 守护进程（tailscaled），且 CLI 默认需要 root，
 *              官方推荐用 `--operator` 把权限交给当前用户，否则后面每条命令都得 sudo。
 */
function tailscaleUpHint() {
  if (IS_WIN) {
    return '启动 Tailscale（Windows 托盘图标）后执行 `tailscale up`，在浏览器里完成授权';
  }
  if (IS_MAC) {
    return '启动 Tailscale App（菜单栏图标）后执行 `tailscale up`；若提示命令不存在，' +
      'CLI 在 /Applications/Tailscale.app/Contents/MacOS/Tailscale（App Store 版不在 PATH 里）';
  }
  return '先确认守护进程在跑（`sudo systemctl enable --now tailscaled`），' +
    '再执行 `sudo tailscale up --operator=$USER` —— 加上 --operator 之后就不用每次 sudo 了';
}

/** Tailscale —— 提供公网 HTTPS 隧道（ChatGPT 够不到 127.0.0.1） */
function checkTailscale() {
  // 先跑命令（Windows `where tailscale`，POSIX `which -a tailscale`）；
  // 只有命令查不到时才回退到约定位置 —— Tailscale 的 Windows 安装器**不把 CLI 写进 PATH**，
  // 所以这层回退是必需的。路径一律由环境变量 / 标准位置推导，不写死盘符。
  const conventional = IS_WIN
    ? [
        process.env.ProgramFiles && join(process.env.ProgramFiles, 'Tailscale', 'tailscale.exe'),
        process.env['ProgramFiles(x86)'] && join(process.env['ProgramFiles(x86)'], 'Tailscale', 'tailscale.exe'),
      ].filter(Boolean)
    : [
        // macOS：Homebrew / 官方 pkg 会装到这两处；独立 App / App Store 版的 CLI 在 bundle 内，不在 PATH
        '/usr/local/bin/tailscale',
        '/opt/homebrew/bin/tailscale',
        '/Applications/Tailscale.app/Contents/MacOS/Tailscale',
        // Linux：官方脚本装到 /usr/bin，发行版包可能在 /usr/sbin，snap 装到 /snap/bin
        '/usr/bin/tailscale',
        '/usr/sbin/tailscale',
        '/snap/bin/tailscale',
      ];
  const bin = whichAll('tailscale')[0] || firstExisting(conventional);
  const item = { id: 'tailscale', name: 'Tailscale', required: '>=1.38.3（1.52 起 CLI 语法变更，建议用新版）', found: null, path: bin };
  if (!bin) {
    item.status = 'fail';
    item.note = '未找到 tailscale CLI（公网隧道必需）';
    return item;
  }
  const r = tryExec(bin, ['version']);
  if (!r.ok) { item.status = 'fail'; item.note = '找到文件但无法执行'; return item; }
  const line = r.out.split('\n')[0].trim();
  item.found = line;
  const p = parseVersion(line);

  let status = 'ok';
  let note = '';
  if (p && (p.major < 1 || (p.major === 1 && p.minor < 38))) {
    status = 'fail';
    note = '版本过低（需 >=1.38.3）';
  } else if (p && p.major === 1 && p.minor < 52) {
    status = 'warn';
    note = '版本 <1.52，serve/funnel 用的是旧 CLI 语法，建议升级';
  }

  // ── 登录态：装了 ≠ 能用 ──
  // `tailscale up` 必须由人去浏览器完成授权，这是整条流程里**第一个必须人工介入**的点。
  // 提前暴露出来，免得 agent 一路跑到开隧道才发现卡在未登录。
  const st = tryExec(bin, ['status', '--json'], { timeout: 10000 });
  let backend = null;
  if (st.ok) {
    try { backend = JSON.parse(st.out).BackendState ?? null; } catch { backend = null; }
  }
  item.backend = backend;

  if (status !== 'fail') {
    if (!backend) {
      status = 'warn';
      note = '读不到运行状态 —— Tailscale 客户端/服务可能没启动';
      item.needsUserAction = tailscaleUpHint();
    } else if (backend !== 'Running') {
      status = 'warn';
      note = `已安装但未登录（BackendState=${backend}）`;
      item.needsUserAction = `${tailscaleUpHint()} —— \`tailscale up\` 会打印一个链接，必须由你用浏览器打开并完成登录授权`;
    } else if (!note) {
      note = '已登录且运行中';
    }
  }

  item.status = status;
  if (note) item.note = note;
  return item;
}

/** DevSpace —— 通过全局 npm root 定位包，而不是靠 shim（shim 在 PATH 残缺时会算错路径） */
function checkDevspace() {
  const item = { id: 'devspace', name: 'DevSpace', required: '@waishnav/devspace', found: null, path: null };
  const npm = npmBin();
  if (!npm) {
    item.status = 'fail';
    item.note = '找不到 npm，先修好 Node/npm';
    return item;
  }
  let root = null;
  const rootRes = tryExec(npm, ['root', '-g']);
  if (!rootRes.ok) {
    item.status = 'fail';
    item.note = `无法执行 \`npm root -g\`：${errLine(rootRes.err)}`;
    return item;
  }
  root = rootRes.out;
  item.globalRoot = root;
  const pkgJson = join(root, '@waishnav', 'devspace', 'package.json');
  if (!existsSync(pkgJson)) {
    item.status = 'fail';
    item.note = `未安装（${root} 下没有 @waishnav/devspace）。安装：npm install -g @waishnav/devspace`;
    return item;
  }
  try {
    const pkg = JSON.parse(readFileSync(pkgJson, 'utf8'));
    item.found = pkg.version;
    item.path = join(root, '@waishnav', 'devspace', 'dist', 'cli.js');
  } catch {
    item.status = 'warn';
    item.note = '找到包但 package.json 解析失败';
    return item;
  }
  item.status = 'ok';
  item.note = '已安装';
  // shim 可用性。
  // Windows：npm 把 shim 直接放在 prefix 根（devspace.cmd），且 POSIX 版 shim 依赖 sed/dirname/uname，
  //          在 PATH 残缺的 shell 里会算错路径 —— 这是 Windows 特有的毛病。
  // macOS/Linux：npm 在 <prefix>/bin 建软链，只要该目录在 PATH 里就没问题（这正是不在 PATH 时最容易被误判成
  //          「装了没用」的情形，所以要把目录算出来告诉用户）。
  if (IS_WIN) {
    if (!existsSync(join(root, '..', 'devspace.cmd')) && !which('devspace.cmd')) {
      item.note = '已安装，但未找到 devspace.cmd shim —— 调用时请直接用 `node <path>/dist/cli.js`';
    }
  } else if (!which('devspace')) {
    // npm 全局 bin = <prefix>/bin，而 <prefix> = 全局 node_modules 的上两级
    const binDir = join(root, '..', '..', 'bin');
    item.note = `已安装，但 PATH 里没有 devspace —— 全局 bin 目录是 ${binDir}，把它加进 PATH，或直接用 \`node ${item.path}\``;
  }
  return item;
}

/** better-sqlite3 原生依赖 —— DevSpace 的状态存储依赖它 */
function checkSqlite(devspaceItem) {
  const item = { id: 'sqlite', name: 'better-sqlite3（DevSpace 原生依赖）', required: '可加载', found: null, path: null };
  if (!devspaceItem.path) { item.status = 'skip'; item.note = 'DevSpace 未安装，跳过'; return item; }
  try {
    const req = createRequire(join(devspaceItem.path, '..', '..', 'package.json'));
    req('better-sqlite3');
    item.status = 'ok';
    item.found = '可加载';
  } catch (e) {
    item.status = 'fail';
    item.found = '加载失败';
    item.note = `多半是原生依赖装在了别的 Node 运行时下。修复：npm rebuild better-sqlite3（${errLine(e)}）`;
  }
  return item;
}

/** 包管理器可用性 —— 决定用什么方式补齐依赖 */
function checkPkgManagers() {
  const out = {};
  if (IS_WIN) {
    const r = tryExec('winget', ['--version']);
    out.winget = r.ok ? r.out : null;
  } else if (IS_MAC) {
    const r = tryExec('brew', ['--version']);
    out.brew = r.ok ? r.out.split('\n')[0] : null;
    // MacPorts 是 macOS 上的另一条路。没有 Homebrew 但有 MacPorts 时至少要认出来，
    // 否则会误导用户以为「这台机器没有任何可用的包管理器」。
    const mp = tryExec('port', ['version']);
    if (mp.ok) out.port = mp.out.split('\n')[0];
  } else {
    for (const m of ['apt-get', 'dnf', 'yum', 'pacman', 'zypper', 'apk']) {
      const r = tryExec(m, ['--version']);
      if (r.ok) out[m] = r.out.split('\n')[0];
    }
  }
  return out;
}

// ─────────────────────────── 安装命令映射 ───────────────────────────

function installCommands(id) {
  const cmds = [];

  const pick = (win, mac, linux) => {
    if (IS_WIN) return win ? [win] : [];
    if (IS_MAC) return mac ? [mac] : [];
    return linux ? [linux] : [];
  };

  if (id === 'node' || id === 'npm') {
    cmds.push(
      ...pick(
        'winget install -e --id OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements',
        'brew install node@22 && brew link --overwrite --force node@22',
        'curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && sudo apt-get install -y nodejs   # Debian/Ubuntu\nsudo dnf install -y nodejs   # Fedora/RHEL\nsudo pacman -S --noconfirm nodejs npm   # Arch'
      )
    );
  }
  if (id === 'git') {
    cmds.push(
      ...pick(
        'winget install -e --id Git.Git --accept-package-agreements --accept-source-agreements',
        'brew install git',
        'sudo apt-get install -y git   # Debian/Ubuntu\nsudo dnf install -y git   # Fedora/RHEL\nsudo pacman -S --noconfirm git   # Arch'
      )
    );
  }
  if (id === 'bash') {
    cmds.push(
      ...pick(
        'winget install -e --id Git.Git --accept-package-agreements --accept-source-agreements   # Git for Windows 自带 Git Bash（推荐）\nwinget install -e --id Microsoft.WSL   # 或者装 WSL',
        'brew install bash',
        // Linux 不给命令：Debian/Ubuntu/Fedora/Arch 都自带 bash，真正缺的是 Alpine 这类精简发行版，
        // 装法按发行版写在 checkBash() 的说明里了。
        // ⚠️ 这里曾经放了一行 `# 一般已自带 bash…` 的注释，结果 --install 把它当命令执行并抛 ENOENT ——
        //    「没有安装方案」必须用空数组表达，不能用注释行占位。
        null
      )
    );
  }
  if (id === 'tailscale') {
    cmds.push(
      ...pick(
        'winget install -e --id Tailscale.Tailscale --accept-package-agreements --accept-source-agreements',
        'brew install --cask tailscale',
        'curl -fsSL https://tailscale.com/install.sh | sh'
      )
    );
  }
  if (id === 'devspace') {
    cmds.push('npm install -g @waishnav/devspace');
  }
  if (id === 'sqlite') {
    cmds.push('npm rebuild better-sqlite3');
  }
  return cmds;
}

/**
 * 执行安装命令时，把命令名解析成真实可执行文件（Windows 上 `npm` 单独一个词跑不起来）。
 * 返回原样说明没解析到 —— 调用方据此判断「这个包管理器本机没有」并跳过，而不是抛 ENOENT。
 */
function resolveExe(tok) {
  if (tok === 'npm' || tok === 'npm.cmd') return npmBin() || tok;
  return which(IS_WIN ? `${tok}.exe` : tok) || which(tok) || tok;
}

// ─────────────────────────── 主流程 ───────────────────────────

const managers = checkPkgManagers();
const nodeItem = checkNode();
const results = [nodeItem, checkNpm(), checkGit(), checkBash(), checkTailscale(), checkDevspace()];
results.push(checkSqlite(results[5]));

const bad = results.filter((r) => r.status === 'fail');
const warns = results.filter((r) => r.status === 'warn');

if (WANT_JSON) {
  console.log(JSON.stringify({ platform: process.platform, managers, results, missing: bad.map((b) => b.id) }, null, 2));
} else {
  console.log('=== 环境自检：DevSpace × ChatGPT MCP 接入前置依赖 ===\n');
  console.log(`平台: ${process.platform}  Node: ${process.versions.node}\n`);

  // 多数项只有 ok/fail/warn 三态，但 bash 有第四态「文件在、却不能用」（WSL 入口 / 起不来），
  // 那时显示「缺失」会误导 —— 允许条目自带 statusLabel 覆盖。
  const icon = (r) => r.statusLabel || ({ ok: '[ok]  ', fail: '[缺失]', warn: '[警告]', skip: '[跳过]' })[r.status] || '[?]';
  for (const r of results) {
    console.log(`${icon(r)} ${r.name}${r.found ? `: ${r.found}` : ''}`);
    if (r.path) console.log(`        路径: ${r.path}`);
    console.log(`        要求: ${r.required}`);
    if (r.globalRoot) console.log(`        全局 root: ${r.globalRoot}`);
    if (r.note) console.log(`        说明: ${r.note}`);
    if (r.needsUserAction) console.log(`        🙋 需要你操作: ${r.needsUserAction}`);
    if (r.candidates) {
      console.log('        发现的 Bash:');
      r.candidates.forEach((c, i) => {
        console.log(`          ${i === 0 ? '★' : ' '} [${c.flavor}] ${c.path}`);
        console.log(`              ${c.version}`);
      });
    }
    console.log('');
  }

  console.log('--- 包管理器 ---');
  if (Object.keys(managers).length) {
    for (const [k, v] of Object.entries(managers)) console.log(`  [ok]   ${k} ${v}`);
  } else {
    console.log('  [缺失] 未找到可用的包管理器（winget / brew / apt 等），需要手动安装依赖');
  }

  // 把「必须人工介入」的点集中报一次 —— 这些脚本替不了，只能提醒用户。
  const manual = results.filter((r) => r.needsUserAction);
  if (manual.length) {
    console.log('\n🙋 以下步骤必须由你亲自完成（脚本代替不了，请先做掉再继续）:');
    for (const m of manual) console.log(`   - ${m.name}：${m.needsUserAction}`);
  }

  const needInstall = [...bad, ...warns.filter((w) => w.id === 'bash' || w.id === 'tailscale')];
  if (needInstall.length === 0 && bad.length === 0) {
    console.log('\n✅ 全部就绪，可以进入下一步：配置 DevSpace + 开隧道。');
  } else if (bad.length > 0) {
    // 「没装」和「装了但用不了」是两种病，分开报 —— 前者重装即可，后者重装是白费。
    const unusable = bad.filter((b) => b.statusLabel);
    const missing = bad.filter((b) => !b.statusLabel);
    if (unusable.length) console.log(`\n❌ 有 ${unusable.length} 项不可用：${unusable.map((b) => b.id).join(', ')}`);
    if (missing.length) console.log(`\n❌ 有 ${missing.length} 项缺失：${missing.map((b) => b.id).join(', ')}`);
    const anyRealInstall = bad.some((b) => !b.noInstallSuggestion);
    console.log(anyRealInstall ? '\n--- 安装命令 ---' : '\n--- 怎么修 ---');
    for (const b of bad) {
      console.log(`\n# ${b.name}`);
      // 「已有可用 bash、只是 DevSpace 找不到」不该建议重装 —— 重装到 C 盘是下策，
      // 用户照着执行会白装一遍，还可能把现有 git 弄成两份。
      if (b.noInstallSuggestion) {
        console.log('  ⛔ 不用重装：本机已经有能用的 bash，问题只是 DevSpace 找不到它。');
        console.log('     按上面「说明」里的修法 ①（临时）或 ②（一劳永逸）让它能被找到即可。');
        continue;
      }
      const cmds = installCommands(b.id);
      if (cmds.length === 0) console.log('  （当前平台没有自动安装方案，请手动安装）');
      else cmds.forEach((c) => console.log('  ' + c));
    }
    if (!WANT_INSTALL) {
      console.log('\n提示：加 --install 让本脚本自动执行上面的命令（本脚本可自行安装的项：devspace、sqlite）。');
    }
  }
  if (warns.length) console.log(`\n⚠️  ${warns.length} 项警告：${warns.map((w) => w.id).join(', ')}`);

  if (WANT_INSTALL) {
    console.log('\n=== 开始安装 ===');
    const targets = (ONLY ? results.filter((r) => ONLY.includes(r.id)) : [...bad, ...warns])
      .filter((r) => r.status === 'fail' || r.status === 'warn');
    if (targets.length === 0) console.log('没有需要安装的项。');

    // 容错：单项失败不中断整轮 —— 继续装后面的，最后统一汇总。
    // 否则「Node 装失败」会连带把 Tailscale 也跳过，用户还得再跑一遍。
    const report = [];
    for (const t of targets) {
      const cmds = installCommands(t.id);
      if (cmds.length === 0) { console.log(`\n[跳过] ${t.name}：无自动安装方案`); report.push({ id: t.id, how: '跳过', ok: null }); continue; }
      for (const c of cmds) {
        // 纯注释行不是命令。曾经在 Linux 上给 bash 返回过一行注释，--install 会拿它当命令跑并抛 ENOENT。
        if (/^\s*#/.test(c)) continue;
        // 含换行（多发行）、或含管道/重定向/sudo 的命令交给用户手动跑，避免 shell 语义不可控
        const isSingle = !c.includes('\n');
        const complex = /[|>&]/.test(c) || /\bsudo\b/.test(c);
        if (!isSingle || complex) {
          console.log(`\n[手动] ${t.name}（请自行执行）:\n  ${c}`);
          report.push({ id: t.id, how: '手动', ok: null });
          continue;
        }
        const parts = c.split(/\s+/);
        const exe = resolveExe(parts[0]);
        // 解析不到可执行文件就别硬跑 —— 明确说「本机没有这个包管理器」，比抛 ENOENT 好读得多。
        // 覆盖三平台：Windows 没 winget、macOS 没 Homebrew/MacPorts、Linux 发行版对不上。
        const resolvable = exe !== parts[0] || existsSync(exe) || !!which(exe);
        if (!resolvable) {
          console.log(`\n[跳过] ${t.name}：本机未找到 \`${parts[0]}\`，无法自动安装（请按上面的「安装命令」手动执行）`);
          report.push({ id: t.id, how: '跳过', ok: null });
          continue;
        }
        // 走网络的安装命令：给长超时 + 重试 1 次（registry 抖动很常见，重试成功率不错）
        const networked = /^(npm|winget|brew|pacman|dnf|yum|apt-get|zypper|apk)$/.test(parts[0]);
        console.log(`\n[执行] ${c}`);
        const r = tryExec(exe, parts.slice(1), {
          timeout: TIMEOUT_INSTALL,
          retries: networked ? 1 : 0,
        });
        if (r.ok) {
          console.log('  ' + (r.out.split('\n').slice(0, 6).join('\n') || '(完成)') + (r.attempts > 1 ? `\n  （第 ${r.attempts} 次尝试成功）` : ''));
          report.push({ id: t.id, how: '自动', ok: true });
        } else {
          console.log(`  失败: ${errLine(r.err)}`);
          report.push({ id: t.id, how: '自动', ok: false, msg: errLine(r.err) });
        }
      }
    }

    // ── 安装结果汇总 ──
    const autoOk = report.filter((x) => x.ok === true);
    const autoFail = report.filter((x) => x.ok === false);
    const manual = report.filter((x) => x.how === '手动');
    const skipped = report.filter((x) => x.how === '跳过');
    console.log('\n--- 安装结果汇总 ---');
    console.log(`  自动成功: ${autoOk.length ? autoOk.map((x) => x.id).join(', ') : '（无）'}`);
    console.log(`  自动失败: ${autoFail.length ? autoFail.map((x) => `${x.id}（${x.msg}）`).join('; ') : '（无）'}`);
    console.log(`  需手动  : ${manual.length ? [...new Set(manual.map((x) => x.id))].join(', ') : '（无）'}`);
    console.log(`  已跳过  : ${skipped.length ? [...new Set(skipped.map((x) => x.id))].join(', ') : '（无）'}`);

    if (autoFail.length) {
      console.log('\n失败项的处理建议：');
      for (const f of autoFail) {
        console.log(`  - ${f.id}: 先查网络/代理；已安装但环境变量没生效时，**新开终端**再试；`);
        console.log(`    仍失败就按上面的「安装命令」手动执行，然后再跑一次本脚本。`);
      }
    }

    console.log('\n⚠️  注意：用包管理器装完 Node/Git 后，**当前终端不会自动刷新 PATH** —— 本进程内看到的仍是旧环境。');
    console.log('   请**新开一个终端**（或重启工具）后重跑本脚本，才算真正确认装好。');
  }
}

// 退出码反映【自检时】的状态：本进程内依赖确实还不可用（PATH 未刷新），不能因为「刚装过」就报绿。
process.exit(bad.length > 0 ? 1 : 0);
