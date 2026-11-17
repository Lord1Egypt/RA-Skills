#!/usr/bin/env node
/**
 * DevSpace + Tailscale Funnel 一键引导脚本
 *
 * 用法：
 *   node devspace-bootstrap.mjs check
 *   node devspace-bootstrap.mjs apply --roots "D:\projects\my-app" [--public-base-url https://x.ts.net]
 *                                            [--port 7676] [--host 127.0.0.1]
 *                                            [--subagents codex,claude]
 *                                            [--dry-run] [--force]
 *   node devspace-bootstrap.mjs rollback [--config|--auth]
 *
 * 设计原则：
 *   - check 只读，绝不写盘。
 *   - apply 只改你显式传入的键，其余键一律保留；已存在的 ownerToken 绝不会被覆盖。
 *   - 不调用 `devspace init`（交互式且会重问所有问题），直接写配置文件。
 *
 * 容错约定（重要）：
 *   - **区分「文件不存在」与「文件解析失败」**。解析失败时默认**拒绝写盘**并退出，
 *     绝不像 `?? {}` 那样把损坏配置当空对象覆盖掉 —— 那会静默丢掉用户原有设置。
 *   - 写盘前**自动备份**到 `<文件>.bak`；写入用「临时文件 + rename」原子替换，
 *     避免进程中途被杀留下半个 JSON。
 *   - 出错时**不留下半成品**：任何校验失败都在写盘之前 process.exit(1)。
 *   - `--dry-run` 可先看会改什么，不落盘。
 *   - `rollback` 从 `.bak` 恢复，恢复前把当前文件另存为 `.pre-rollback`（回滚也可再回滚）。
 *
 * 人工介入提醒：
 *   - 登录 / 浏览器授权 / 后台开关这类步骤**脚本代替不了**，必须由用户本人做。
 *     检测到这类情况（Tailscale 未登录、Funnel 未启用…）会就地打 🙋 提示，
 *     并在输出末尾统一汇总，避免 agent 一路干等到卡住才发现。
 *
 * 跨平台（Windows / macOS / Linux）：
 *   - 配置目录三平台都是 `~/.devspace`（Windows 即 `C:\Users\<你>\.devspace`），由 DevSpace 自身决定，
 *     本脚本只用 os.homedir() 拼接，不做平台分支。
 *   - `--roots` 去重时按平台决定是否大小写不敏感：Windows/macOS 不敏感，**Linux 敏感**
 *     （弄错会静默丢掉一个白名单目录）。见 CASE_INSENSITIVE_FS。
 *   - tailscale 的候选路径与「未登录怎么办」的提示都按平台给出，见 findTailscale / tailscaleUpHint。
 * 细节见 references/cross-platform.md。
 *
 * 退出码：0 成功；1 出错（含前置条件不满足 / 配置损坏）。
 */

import { execFileSync } from 'node:child_process';
import { randomBytes } from 'node:crypto';
import { copyFileSync, existsSync, mkdirSync, readFileSync, renameSync, unlinkSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { delimiter, dirname, join, resolve as resolvePath } from 'node:path';

const CONFIG_DIR = join(homedir(), '.devspace');
const CONFIG_PATH = join(CONFIG_DIR, 'config.json');
const AUTH_PATH = join(CONFIG_DIR, 'auth.json');

const IS_WIN = process.platform === 'win32';
const IS_MAC = process.platform === 'darwin';

/**
 * 文件系统是否大小写不敏感。
 *
 * Windows 的 NTFS 和 macOS 默认的 APFS/HFS+ 都不敏感；Linux 的 ext4/xfs 敏感。
 * 这个常量决定 allowedRoots 去重时**能不能把路径转小写比较** ——
 * 弄错会静默丢掉一个白名单目录（Linux 上 ~/Projects 与 ~/projects 是两个不同的目录）。
 */
const CASE_INSENSITIVE_FS = IS_WIN || IS_MAC;

/**
 * Tailscale 未运行 / 未登录时的处置建议。
 *
 * 三个平台的服务模型不同，不能一句话打发：
 *   Windows —— 常驻托盘程序，登录靠它自己弹浏览器；
 *   macOS   —— GUI App（菜单栏图标），CLI 还可能藏在 app bundle 里不在 PATH；
 *   Linux   —— systemd 守护进程（tailscaled），CLI 默认要 root，官方建议用 --operator 交给当前用户。
 *
 * 与 env-check.mjs 里的同名逻辑保持一致（两个脚本各自独立可跑，所以是有意重复的）。
 */
function tailscaleUpHint() {
  if (IS_WIN) {
    return '启动 Tailscale（Windows 托盘图标）后执行 `tailscale up` —— 它会打印一个链接，用浏览器打开完成授权';
  }
  if (IS_MAC) {
    return '启动 Tailscale App（菜单栏图标）后执行 `tailscale up`；若提示命令不存在，CLI 在 /Applications/Tailscale.app/Contents/MacOS/Tailscale';
  }
  return '先确认守护进程在跑（`sudo systemctl enable --now tailscaled`），再执行 `sudo tailscale up --operator=$USER` —— 加了 --operator 之后就不用每次 sudo';
}

const log = (...a) => console.log(...a);
const ok = (m) => console.log(`  [ok]   ${m}`);
const warn = (m) => console.log(`  [warn] ${m}`);
const fail = (m) => console.log(`  [FAIL] ${m}`);

/**
 * 记录一条「必须人工介入」的提醒。
 * 这些步骤（登录、浏览器授权、后台开关）脚本代替不了，所以既要就地提示，
 * 也要在最后统一汇总一次 —— 埋在长日志中间容易被忽略。
 */
const manualActions = [];
const ask = (m) => {
  manualActions.push(m);
  console.log(`  🙋 需要用户操作: ${m}`);
};

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) out[key] = true;
      else { out[key] = next; i++; }
    } else out._.push(a);
  }
  return out;
}

/** 把底层异常压成一行，避免日志里刷堆栈。 */
function errLine(e) {
  if (!e) return '(无错误对象)';
  if (e.code === 'ETIMEDOUT' || e.killed) return '超时未返回';
  if (e.code === 'ENOENT') return '命令/文件不存在';
  const raw = e.stderr ? String(e.stderr) : String(e.message || e);
  return raw.split('\n').map((s) => s.trim()).filter(Boolean)[0]?.slice(0, 200) || '(无输出)';
}

/**
 * 严格读：区分 missing / ok / corrupt / unreadable 四种状态。
 * 【容错要点】绝不能把 corrupt 当成 missing —— 后续若用 `?? {}` 兜底，
 * 一个尾逗号就会让脚本把用户整套配置覆盖成最小对象，且毫无提示。
 */
function readJsonState(p) {
  if (!existsSync(p)) return { state: 'missing', path: p };
  let raw;
  try {
    raw = readFileSync(p, 'utf8');
  } catch (e) {
    return { state: 'unreadable', path: p, error: errLine(e) };
  }
  if (!raw.trim()) return { state: 'corrupt', path: p, raw, error: '文件为空' };
  try {
    return { state: 'ok', path: p, raw, value: JSON.parse(raw) };
  } catch (e) {
    return { state: 'corrupt', path: p, raw, error: String(e.message || e).split('\n')[0] };
  }
}

/** 宽松读，只给只读的 doctor 用。 */
function readJson(p) {
  const s = readJsonState(p);
  return s.state === 'ok' ? s.value : null;
}

/**
 * 处理「存在但损坏」的配置：把它另存为 `<文件>.corrupt-<时间戳>`（保留证据、可人工修复），
 * 然后视调用方决定是否继续。**绝不原地覆盖丢弃。**
 */
function quarantineCorrupt(state) {
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const dest = `${state.path}.corrupt-${stamp}`;
  try {
    copyFileSync(state.path, dest);
    ok(`已把损坏的配置另存为 ${dest}`);
  } catch (e) {
    warn(`另存损坏配置失败（${errLine(e)}），继续但请勿删原文件`);
    return null;
  }
  return dest;
}

/**
 * 统一的进程执行入口（容错要点）。
 *
 * Windows 上 Node **不能直接 spawn `.cmd` / `.bat`**（会抛 EINVAL），必须 `shell: true`；
 * 而 shell 模式只是把命令与参数用空格拼接、**不会给含空格的路径加引号**，
 * 所以带空格的路径会被截断。这里两个坑一起处理：先手动加引号，再走 shell。
 *
 * 同一个坑在 `env-check.mjs` 里也修过 —— 两处保持一致，
 * 因为 Windows 上 tailscale 有可能被装成 scoop/winget 的 `.cmd` shim 而非 `.exe`。
 */
function run(bin, args, extra = {}) {
  const needsShell = IS_WIN && /\.(cmd|bat)$/i.test(bin);
  const launch = needsShell ? `"${bin}"` : bin;
  return execFileSync(launch, args, {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    windowsHide: true,
    shell: needsShell,
    ...extra,
  });
}

/**
 * 定位 tailscale 可执行文件。
 *
 * 顺序遵守本 skill 的检查原则：**先用命令问系统，再考虑约定位置**。
 * 约定位置这层不能删 —— Tailscale 的 Windows 安装器不把 CLI 写进 PATH，
 * 光靠 `where` 会漏掉一个装得好好的客户端。但路径一律由环境变量 / 标准位置推导，不写死盘符。
 */
function findTailscale() {
  // ① 命令：直接把它跑起来试试（Windows 上还有 scoop / winget 装的 .cmd shim，一并覆盖）
  const names = IS_WIN ? ['tailscale.exe', 'tailscale.cmd', 'tailscale.bat', 'tailscale'] : ['tailscale'];
  for (const n of names) {
    try { run(n, ['version'], { timeout: 8000 }); return n; } catch { /* 继续试下一个 */ }
  }
  // ② 约定位置。候选与 env-check.mjs 保持一致 —— 两个脚本若给出不同的结论，用户会以为其中一个是坏的。
  const conventional = IS_WIN
    ? [
        process.env.ProgramFiles && join(process.env.ProgramFiles, 'Tailscale', 'tailscale.exe'),
        process.env['ProgramFiles(x86)'] && join(process.env['ProgramFiles(x86)'], 'Tailscale', 'tailscale.exe'),
      ].filter(Boolean)
    : [
        // macOS：Homebrew / 官方 pkg；独立 App 与 App Store 版的 CLI 在 bundle 内、不在 PATH
        '/usr/local/bin/tailscale',
        '/opt/homebrew/bin/tailscale',
        '/Applications/Tailscale.app/Contents/MacOS/Tailscale',
        // Linux：官方脚本 → /usr/bin，发行版包 → /usr/sbin，snap → /snap/bin
        '/usr/bin/tailscale',
        '/usr/sbin/tailscale',
        '/snap/bin/tailscale',
      ];
  for (const c of conventional) if (existsSync(c)) return c;
  return null;
}

/**
 * 调 tailscale。带超时 —— 未登录 / 守护进程没起来时，
 * `tailscale status` 有可能长时间无响应，不设上限会把脚本挂死。
 */
function tsRun(bin, args) {
  return run(bin, args, { timeout: 15000, killSignal: 'SIGKILL' });
}

/** 从 `tailscale status --json` 推导 Funnel 公网 origin（不含 /mcp）。 */
function funnelOrigin(bin) {
  const raw = tsRun(bin, ['status', '--json']);
  const j = JSON.parse(raw);
  const dns = j?.Self?.DNSName;
  if (!dns) throw new Error('tailscale status 未返回 Self.DNSName（是否已登录？先跑 tailscale up）');
  return { origin: `https://${dns.replace(/\.$/, '')}`, dnsName: dns, tailnet: j?.MagicDNSSuffix ?? null };
}

function newNodeCheck() {
  const major = Number(process.versions.node.split('.')[0]);
  const minor = Number(process.versions.node.split('.')[1]);
  // README 要求 >=22.19 <27；代码内 assertSupportedNode 实际放宽到 >=20.12 <27。
  if (major >= 27) return { okNode: false, note: `Node ${process.versions.node} 过高（需 <27）` };
  if (major === 20 && minor < 12) return { okNode: false, note: `Node ${process.versions.node} 过低（需 >=20.12，建议 22 LTS）` };
  if (major < 20) return { okNode: false, note: `Node ${process.versions.node} 过低` };
  const recommended = !(major === 22 && minor >= 19) && major !== 24;
  return { okNode: true, note: recommended ? `Node ${process.versions.node} 可用，但 README 推荐 22.19+ / 24` : `Node ${process.versions.node}` };
}

/** 在 PATH 里找可执行文件（本脚本独立可跑，故不复用 env-check 的实现）。 */
function whichOnPath(name) {
  const pathEnv = process.env.PATH || '';
  const exts = IS_WIN ? (process.env.PATHEXT || '.EXE;.CMD;.BAT;.COM').split(';').filter(Boolean) : [''];
  for (const dir of pathEnv.split(delimiter).filter(Boolean)) {
    for (const ext of exts) {
      const p = join(dir, name + ext);
      try {
        if (existsSync(p)) return p;
      } catch {
        /* 忽略无权限目录 */
      }
    }
  }
  return null;
}

/**
 * DevSpace 实际会用的 shell 是否**真的能用**。
 *
 * 放在 doctor 里的理由：这是一条「启动 serve 之前必须为真」的前置条件，而且**失败时最难查** ——
 * serve 起得来、隧道通、ChatGPT 也能连上，但每条 shell 命令都失败，用户只会看到 `RuntimeException`
 * 或一段乱码，根本联想不到是 shell 选错了。
 *
 * 判定顺序完全复刻 DevSpace 源码 `pi-coding-agent/dist/utils/shell.js` 的 getShellConfig()：
 * Windows ① `%ProgramFiles%\Git\bin\bash.exe` ② `%ProgramFiles(x86)%\Git\bin\bash.exe`
 * ③ `where bash.exe` 的第一个命中 ④ 抛错。
 *
 * 关键是第 ③ 步：Git for Windows 装在非 C 盘时，①② 都落空，而 `C:\Windows\System32\bash.exe`
 * （**WSL 启动器，不是 shell**）几乎必定抢先 —— 它忽略 `-c`、不执行命令，所有命令全废。
 * 与 env-check.mjs 里的同名逻辑保持一致（两个脚本各自独立可跑，所以是有意重复的）。
 */
function checkDevspaceShell() {
  const isLegacyWsl = (p) => /^[a-z]:\\windows\\(?:system32|sysnative)\\bash\.exe$/i.test(String(p).replace(/\//g, '\\'));
  const isStoreWsl = (p) => /\\appdata\\local\\microsoft\\windowsapps\\/i.test(String(p).replace(/\//g, '\\'));

  if (!IS_WIN) {
    if (existsSync('/bin/bash')) return { ok: true, path: '/bin/bash', note: '/bin/bash（存在即用）' };
    const p = whichOnPath('bash');
    if (p) return { ok: true, path: p, note: p };
    if (existsSync('/bin/sh')) {
      return { ok: false, soft: true, path: '/bin/sh', note: '没有 bash，DevSpace 会退化成 /bin/sh（bash 专有语法会失败）' };
    }
    return { ok: false, path: null, note: '找不到 bash，也没有 /bin/sh 兜底' };
  }

  // ①② DevSpace 源码里写死的那两个位置 —— 必须照抄才能得到和它一致的结论。
  // 这是本脚本唯一一处「看目录」：要复刻的是**它的行为**，不是我们的判断；
  // 路径由 %ProgramFiles% 环境变量推导，所以不含任何盘符字面量。
  const known = [];
  if (process.env.ProgramFiles) known.push(join(process.env.ProgramFiles, 'Git', 'bin', 'bash.exe'));
  if (process.env['ProgramFiles(x86)']) known.push(join(process.env['ProgramFiles(x86)'], 'Git', 'bin', 'bash.exe'));
  let resolved = known.find((p) => existsSync(p)) ?? null;
  // ③ 问系统：PATH 上第一个 bash（= `where bash.exe` 的第一个命中）
  if (!resolved) resolved = whichOnPath('bash') || whichOnPath('bash.exe') || null;

  if (!resolved) {
    return { ok: false, path: null, note: '找不到任何 bash → DevSpace 会抛 "No bash shell found"（Windows 无兜底）' };
  }
  if (isLegacyWsl(resolved) || isStoreWsl(resolved)) {
    // 反查真 Git Bash 的位置：从 PATH 上的 `git.exe` 反推同一份安装里的 `bin\bash.exe`。
    // 不假设 git.exe 一定在 `<root>\cmd` 下（也可能是 `<root>\mingw64\bin`），所以逐级向上找 ——
    // 这样修法里的命令能直接粘贴，又不会把某一台机器的盘符写死进脚本。
    const gitExe = whichOnPath('git') || whichOnPath('git.exe');
    let gitRoot = null;
    for (let d = gitExe ? dirname(gitExe) : null, i = 0; d && i < 4; i++) {
      if (existsSync(join(d, 'bin', 'bash.exe'))) { gitRoot = d; break; }
      const up = dirname(d);
      if (up === d) break;
      d = up;
    }
    if (!gitRoot && gitExe) gitRoot = dirname(dirname(gitExe));
    const binDir = gitRoot ? join(gitRoot, 'bin') : '<你的Git安装目录>\\bin';
    const rootShown = gitRoot ?? '<你的Git安装目录>';
    return {
      ok: false,
      wsl: true,
      path: resolved,
      note:
        `${resolved} 是 **WSL 启动器，不是 shell** —— 它忽略 -c、不执行命令，` +
        'ChatGPT 里**所有**命令都会失败（连 `echo` 也不例外）。\n' +
        '        原因：Windows 上 DevSpace 只在 %ProgramFiles%\\Git\\bin 找 bash，装到别的盘就落到 PATH 第一个命中。\n' +
        '        修法（三选一）：\n' +
        `          ① 启动 serve 时前置 PATH：set "PATH=${binDir};%PATH%" && devspace serve\n` +
        `          ② 建 junction（需管理员）：mklink /J "C:\\Program Files\\Git" "${rootShown}"\n` +
        '          ③ 把 Git 的 bin 前置到【系统】PATH（用户变量没用，系统 PATH 优先）\n' +
        '        详见 references/troubleshooting.md「Windows：bash 被 WSL 启动器顶掉」',
    };
  }
  // 真跑一条命令 —— 路径存在不等于它能干活
  try {
    const out = run(resolved, ['-c', 'echo devspace-shell-ok'], { timeout: 15000, killSignal: 'SIGKILL' });
    if (!String(out).includes('devspace-shell-ok')) {
      return { ok: false, path: resolved, note: `${resolved} 起不来（echo 没有回显）` };
    }
  } catch (e) {
    return { ok: false, path: resolved, note: `${resolved} 执行失败：${errLine(e)}` };
  }
  return { ok: true, path: resolved, note: `${resolved}（冒烟测试通过）` };
}

function doctor() {
  log('=== DevSpace + Tailscale 环境检查 ===\n');

  const n = newNodeCheck();
  log(`Node ${process.versions.node}`);
  n.okNode ? ok(n.note) : fail(n.note);

  // shell 放在 Node 之后、Tailscale 之前 —— 它同样是「serve 之前必须为真」的前置条件，
  // 而且失败时最难查（serve 能起、隧道能通，只有命令全失败）。见 checkDevspaceShell()。
  const sh = checkDevspaceShell();
  if (sh.ok) ok(`shell: ${sh.note}`);
  else if (sh.soft) warn(`shell: ${sh.note}`);
  else {
    fail(`shell: ${sh.note}`);
    if (sh.wsl) ask('把真 Git Bash 放到 DevSpace 能找到的位置（上面三条修法任选其一），改完重启 serve');
  }

  const ts = findTailscale();
  if (!ts) {
    fail('未找到 tailscale CLI');
    log('        Windows: winget install -e --id Tailscale.Tailscale');
    log('        macOS  : brew install --cask tailscale');
    log('        Linux  : curl -fsSL https://tailscale.com/install.sh | sh');
  } else {
    ok(`tailscale CLI: ${ts}`);
    try {
      const v = tsRun(ts, ['version']).split('\n')[0].trim();
      ok(`tailscale 版本: ${v}`);
      if (/^1\.(3[0-9]|4[0-9]|5[0-1])\./.test(v)) warn('版本 <1.52，serve/funnel CLI 语法是旧的，建议升级');
    } catch { warn('无法读取 tailscale 版本'); }

    try {
      const { origin, dnsName, tailnet } = funnelOrigin(ts);
      ok(`MagicDNS 域名: ${dnsName}`);
      tailnet && ok(`tailnet suffix: ${tailnet}`);
      ok(`推导出的 publicBaseUrl: ${origin}`);
      log(`         ChatGPT 里要填的 MCP 端点: ${origin}/mcp`);
    } catch (e) {
      fail(`无法推导 Funnel 域名: ${errLine(e)}`);
      ask(`Tailscale 未就绪 —— ${tailscaleUpHint()}`);
    }

    try {
      const st = tsRun(ts, ['funnel', 'status']);
      const lines = st.split('\n').map((s) => s.trim()).filter(Boolean);
      if (lines.some((l) => l.includes('proxy') || l.includes('(Funnel on)'))) {
        ok('Funnel 已开启');
        lines.forEach((l) => log(`         ${l}`));
      } else {
        warn('Funnel 未配置');
        // 命令本身三平台一致；差别在 Linux 上 CLI 默认要 root（除非 up 时带过 --operator）
        const funnelCmd = IS_WIN || IS_MAC ? 'tailscale funnel --bg 7676' : 'tailscale funnel --bg 7676（未设 --operator 时要 sudo）';
        log(`        命令: ${funnelCmd}`);
        ask(`起隧道需要执行 \`tailscale funnel --bg 7676\`；**若是首次启用 Funnel**，终端会另给一个批准链接，也要你去浏览器点同意`);
      }
    } catch {
      warn('funnel status 读取失败（可能未启用 Funnel）');
      ask('去 Tailscale 后台确认 Funnel 已启用，并确认 MagicDNS 已打开（后台 DNS 页）');
    }
  }

  log('\n--- 现有 DevSpace 配置 ---');
  const cfg = readJson(CONFIG_PATH);
  const auth = readJson(AUTH_PATH);
  if (cfg) {
    ok(`config.json 存在 (port=${cfg.port ?? '未设'} host=${cfg.host ?? '未设'})`);
    log(`         publicBaseUrl : ${cfg.publicBaseUrl ?? '(未设，会兜底成 localhost)'}`);
    log(`         allowedRoots  : ${cfg.allowedRoots ? cfg.allowedRoots.join(', ') : '(未设 → 兜底 process.cwd())'}`);
    log(`         subagents     : ${cfg.subagents?.providers?.map((p) => p.id).join(', ') || '(未设)'}`);
  } else {
    warn('config.json 不存在 → serve 会尝试交互式 init');
  }
  if (auth?.ownerToken) ok(`auth.json 存在，ownerToken 长度 ${auth.ownerToken.length}`);
  else warn('auth.json 不存在/无 ownerToken → 非交互环境下 serve 会直接报错');

  log('\n提示：allowedRoots 未配置时会兜底成 `devspace serve` 启动时的当前目录。');

  log('');
  if (manualActions.length) {
    log('🙋 需要你亲自完成的步骤（脚本代替不了，请先做掉）:');
    manualActions.forEach((m, i) => log(`   ${i + 1}) ${m}`));
  } else {
    log('✅ 本机侧没有待办的人工登录/授权步骤。');
  }
  log('   （ChatGPT 侧建连接器 + OAuth 授权可由 agent 用 browser-harness 自动完成；');
  log('     没装 browser-harness 时才需要人工在浏览器里填表 —— 见 references/chatgpt-connector.md）');
}

/** 备份已有文件到 `<文件>.bak`（覆盖旧备份 —— 只保留最近一次可用的好状态）。 */
function backupFile(p) {
  if (!existsSync(p)) return null;
  const bak = `${p}.bak`;
  try {
    copyFileSync(p, bak);
    return bak;
  } catch (e) {
    warn(`备份 ${p} 失败：${errLine(e)}（继续写入，但请留意）`);
    return null;
  }
}

/**
 * 原子写 + 自动备份：
 *   1) 先把现有文件备份成 .bak
 *   2) 写同目录临时文件，再 rename 覆盖 —— 同分区 rename 是原子的。
 *      这样即使进程恰在写入瞬间被杀，目标文件也只可能是「旧的完整版」或「新的完整版」，
 *      不会留下被截断的半个 JSON（那正是配置文件损坏最常见的来源）。
 */
function writeJson(p, obj) {
  mkdirSync(dirname(p), { recursive: true });
  const payload = JSON.stringify(obj, null, 2) + '\n';

  const bak = backupFile(p);
  if (bak) ok(`已备份原文件 → ${bak}`);

  const tmp = `${p}.tmp-${process.pid}`;
  writeFileSync(tmp, payload, 'utf8');
  try {
    renameSync(tmp, p);
  } catch (e) {
    // 兜底：Windows 上文件被占用 / 跨设备时 rename 可能失败，退化成 copy
    try {
      copyFileSync(tmp, p);
    } catch (e2) {
      try { unlinkSync(tmp); } catch { /* 清理失败不掩盖主错误 */ }
      throw e2;
    }
    try { unlinkSync(tmp); } catch { /* noop */ }
  }
}

function apply(args) {
  const dryRun = !!args['dry-run'];
  const force = !!args.force;
  log(`=== 应用 DevSpace 配置${dryRun ? '（dry-run，不落盘）' : ''} ===\n`);

  const n = newNodeCheck();
  if (!n.okNode) { fail(n.note); process.exit(1); }
  ok(n.note);

  // ── 容错①：配置坏了就拒绝写盘 ──
  // 绝不能 `readJson(...) ?? {}` —— 那会把「一个尾逗号」演变成「整套配置被静默清空」。
  const cfgState = readJsonState(CONFIG_PATH);
  let cfg;
  if (cfgState.state === 'ok') cfg = cfgState.value;
  else if (cfgState.state === 'missing') cfg = {};
  else {
    fail(`config.json 无法解析：${cfgState.error}`);
    log(`        路径: ${CONFIG_PATH}`);
    quarantineCorrupt(cfgState);
    if (!force) {
      log('\n  已中止，**未改动任何内容**。');
      log('  请人工修好（多是一个尾逗号/被截断），或加 --force 以最小配置重建。');
      process.exit(1);
    }
    warn('--force 已指定 → 以最小配置重建（原文件已另存，证据保留）');
    cfg = {};
  }
  if (cfg === null || typeof cfg !== 'object' || Array.isArray(cfg)) {
    fail('config.json 顶层不是对象 —— 结构不对，拒绝继续以免写坏');
    process.exit(1);
  }
  const before = JSON.stringify(cfg);

  // publicBaseUrl：显式传入优先，否则尝试从 Tailscale 推导
  let publicBaseUrl = typeof args['public-base-url'] === 'string' ? args['public-base-url'] : null;
  if (!publicBaseUrl) {
    const ts = findTailscale();
    if (ts) {
      try {
        const { origin } = funnelOrigin(ts);
        publicBaseUrl = origin;
        ok(`从 Tailscale 推导 publicBaseUrl: ${origin}`);
      } catch (e) {
        warn(`无法推导（${String(e.message || e).split('\n')[0]}）`);
      }
    }
  }
  if (publicBaseUrl) {
    cfg.publicBaseUrl = publicBaseUrl.replace(/\/+$/, ''); // 规整：去尾斜杠
    // 容错②：形态校验一律在【写盘之前】做，失败就退出，不留下半成品配置
    if (cfg.publicBaseUrl.endsWith('/mcp')) {
      fail('publicBaseUrl 不能带 /mcp —— 这是 setup 用的 origin，客户端才填 /mcp');
      process.exit(1);
    }
    let parsed = null;
    try { parsed = new URL(cfg.publicBaseUrl); } catch { /* 下面统一处理 */ }
    if (!parsed) {
      fail(`publicBaseUrl 不是合法 URL：${cfg.publicBaseUrl}`);
      process.exit(1);
    }
    const isLocal = /^(127\.0\.0\.1|localhost|\[::1\])$/i.test(parsed.hostname);
    if (parsed.protocol !== 'https:' && !isLocal) {
      warn(`${parsed.protocol}// 不是 HTTPS —— ChatGPT 侧很可能连不上（仅临时隧道场景才可接受）`);
    }
    ok(`publicBaseUrl = ${cfg.publicBaseUrl}`);
  } else {
    warn('未设置 publicBaseUrl（隧道没起来就会这样）');
  }

  if (typeof args.roots === 'string') {
    const roots = args.roots.split(',').map((s) => s.trim()).filter(Boolean);

    // macOS / Linux 的路径用正斜杠。传了反斜杠基本是从 Windows 文档里直接抄过来的，
    // 在 POSIX 上会被当成「名字里带反斜杠的文件名」，目录当然不存在 —— 明确提示比让人猜好。
    if (!IS_WIN) {
      for (const r of roots) {
        if (r.includes('\\')) warn(`路径含反斜杠：${r} —— macOS / Linux 用正斜杠（如 /home/you/projects），这个路径多半不对`);
      }
    }

    // 展开 ~ 后统一 resolve() 归一化。
    // 原因：Git Bash / MSYS 会把 D:\x 这种参数自动改写成 D:/x（路径转换），
    // 直接用会让写进配置的路径形式不稳定，进而破坏下面的幂等比较。
    // resolve() 在 Windows 上统一成 D:\x，在 POSIX 上统一成正斜杠绝对路径。
    const homeExpanded = roots
      .map((r) =>
        r === '~' ? homedir() : r.startsWith('~/') || r.startsWith('~\\') ? join(homedir(), r.slice(2)) : r
      )
      .map((r) => resolvePath(r));

    // 去重。大小写敏感与否**按平台判断**：
    // 无条件 toLowerCase() 在 Linux 上会把 ~/Projects 与 ~/projects 当成同一个目录，
    // 静默丢掉一个白名单项 —— 而它们在 ext4 上是两个完全不同的目录。
    const seen = new Set();
    const unique = homeExpanded.filter((r) => {
      const k = CASE_INSENSITIVE_FS ? r.toLowerCase() : r;
      if (seen.has(k)) return false;
      seen.add(k);
      return true;
    });

    const home = resolvePath(homedir());
    for (const r of unique) {
      if (!existsSync(r)) warn(`根目录不存在（先建好再启动，否则 serve 会报 path 不在白名单）：${r}`);
      if (/^[a-z]:\\?$/i.test(r) || r === '/') {
        warn(`--roots 指向盘符/系统根：${r} —— 等于把整盘交出去，强烈建议改成具体项目目录`);
      } else if (r === home) {
        // 主目录同样危险，而且更隐蔽：里面有 .ssh / .aws / .devspace/auth.json 等凭据文件
        warn(`--roots 指向用户主目录：${r} —— 主目录下有 .ssh / .aws 等凭据，等于一起交出去，请改成具体项目目录`);
      }
    }

    cfg.allowedRoots = unique;
    ok(`allowedRoots = ${unique.join(', ')}`);
  } else if (!cfg.allowedRoots) {
    warn('未传 --roots 且配置里也没有 allowedRoots → 会兜底成 serve 启动时的当前目录');
  }

  if (typeof args.port === 'string') { cfg.port = Number(args.port); ok(`port = ${cfg.port}`); }
  else if (cfg.port === undefined) { cfg.port = 7676; ok('port = 7676 (默认)'); }

  if (typeof args.host === 'string') { cfg.host = args.host; ok(`host = ${cfg.host}`); }
  else if (cfg.host === undefined) { cfg.host = '127.0.0.1'; ok('host = 127.0.0.1 (默认)'); }

  if (typeof args.subagents === 'string') {
    const ids = args.subagents.split(',').map((s) => s.trim()).filter(Boolean);
    cfg.subagents = { enabled: true, providers: ids.map((id) => ({ id, enabled: true })) };
    ok(`subagents = ${ids.join(', ')}`);
  }

  // ── 容错③：auth.json 同样先验完整性 ──
  // 如果损坏就当成「没有 ownerToken」去生成新的，会**静默让用户原有的 Owner password 失效**，
  // 且下一次授权会莫名其妙被拒。所以这里宁可停。
  const authState = readJsonState(AUTH_PATH);
  let auth;
  let authNeedsWrite = false;
  if (authState.state === 'ok') {
    auth = authState.value;
    if (auth === null || typeof auth !== 'object' || Array.isArray(auth)) {
      fail('auth.json 顶层不是对象 —— 拒绝继续，以免覆盖掉里面的 ownerToken');
      process.exit(1);
    }
    if (auth.ownerToken) ok(`保留已有 ownerToken（长度 ${String(auth.ownerToken).length}）`);
    else { warn('auth.json 存在但没有 ownerToken → 将生成一个'); authNeedsWrite = true; }
  } else if (authState.state === 'missing') {
    auth = {};
    authNeedsWrite = true;
    warn('auth.json 不存在 → 将生成');
  } else {
    fail(`auth.json 无法解析：${authState.error}`);
    quarantineCorrupt(authState);
    if (!force) {
      log('\n  已中止，**未改动任何内容**。');
      log('  auth.json 里的 ownerToken 是授权页唯一凭据，别随手删。');
      log('  请人工修好，或加 --force 重建（会生成新的 Owner password，需重新授权）。');
      process.exit(1);
    }
    warn('--force 已指定 → 重建 auth.json（原文件已另存，证据保留）');
    auth = {};
    authNeedsWrite = true;
  }

  // ── 落盘 ──
  if (dryRun) {
    log('\n--- dry-run：以下变更【未写入】 ---');
    log(`  ${CONFIG_PATH}`);
    log(JSON.stringify(cfg, null, 2).split('\n').map((l) => '    ' + l).join('\n'));
    if (authNeedsWrite) log(`  ${AUTH_PATH} → 会生成新的 ownerToken`);
    else log(`  ${AUTH_PATH} → 不变（保留现有 ownerToken）`);
    log('\n确认无误后去掉 --dry-run 即真正写入。');
    return;
  }

  // 幂等：内容真变了才写，避免无意义地动用户文件
  if (JSON.stringify(cfg) === before) ok('config.json 无需变更（幂等：跳过写入）');
  else { writeJson(CONFIG_PATH, cfg); ok(`已写入 ${CONFIG_PATH}`); }

  if (authNeedsWrite) {
    if (!auth.ownerToken) auth.ownerToken = randomBytes(32).toString('base64url'); // 与 devspace 的 generateOwnerToken 一致
    writeJson(AUTH_PATH, auth);
    ok(`已写入 ${AUTH_PATH}`);
    log(`\n  ★ Owner password（授权页要填这个）:\n    ${auth.ownerToken}\n`);
  }

  log('--- 下一步 ---');
  log('  [脚本可做] 1) 在目标目录下启动（进程必须常驻，停了 ChatGPT 就断）：');
  log('               devspace serve');
  log('  [脚本可做] 2) 检查启动日志里的 "allowed roots:" 一行是否符合预期');
  log('  [脚本可做] 3) 开隧道：');
  log(`               tailscale funnel --bg ${cfg.port}`);
  log('');
  log('  🤖 以下步骤【默认由 agent 用 browser-harness 自动完成，用户不用自己填表】：');
  log('     4) 打开【开发者模式】：设置 → 账户安全与登录 → 开发者模式（只需一次）');
  log('     5) 建连接器（用深链接直达新插件弹窗，别去列表页找按钮）：');
  log('          https://chatgpt.com/plugins#settings/Connectors?create-connector=true&redirectAfter=%2Fplugins');
  log(`          服务器 URL : ${cfg.publicBaseUrl ?? '<publicBaseUrl>'}/mcp`);
  log('          身份验证   : OAUTH（保持默认）');
  log('          勾选「我了解并希望继续」→ 点「创建」（提交是异步的，至少等 6 秒再判断成败）');
  log('          提交前先看「高级 OAuth 设置」按钮是否从 disabled 变 enabled ——');
  log('          没变就说明 OAuth 发现失败（URL 少了 /mcp / 隧道不通 / 服务没起），别提交');
  log('        ⚠️ 连接器必须在「插件」页建；在「设置」里建同样字段的表单会报 Something went wrong');
  log(
    `     6) 跳 /authorize 后，agent 从 auth.json 就地读取 Owner password 填入${
      authNeedsWrite ? '（就是上面新生成的那个）' : '（你原有的那个）'
    } → 点 Authorize DevSpace`
  );
  log('        ⚠️ 绝不 print / 回显 / 当命令行参数传；也绝不要用户把它贴进聊天或日志里');
  log('');
  log('  🙋 以下步骤【必须由你亲自完成】：');
  log('     7) 新开一个对话，从工具菜单手动挂上 DevSpace（没有公开 API）');
  log('     8) 【首次】允许 Chrome 远程调试：勾选 "Allow remote debugging for this browser instance"');
  log('        并点 Allow（只需一次；不要在循环里重试，Chrome 每个新连接都会弹新对话框）');
  log('');
  log('  若本机没有 browser-harness：第 4–6 步退化为人工作业 —— 把上面那些值自己填进浏览器即可，结果一致。');
  log('  详见 references/chatgpt-connector.md（含完整自动化步骤与人工兜底路径）。');
  log('');
  log('  若是【首次】启用 Funnel，Tailscale 会另给一个批准链接 —— 也需要你去浏览器点同意。');
  if (!publicBaseUrl) log('  ⚠️ 目前还没拿到公网域名（隧道未起）→ 第 5 步的 URL 先留着，起完隧道再回来填。');
}

/**
 * 从 .bak 恢复。
 * 恢复前先把当前文件另存为 `.pre-rollback` —— 于是「回滚」本身也可再回滚，
 * 避免一次误操作后连现状都找不回来。
 */
function rollback(args) {
  log('=== 回滚 DevSpace 配置（从 .bak 恢复）===\n');
  const targets = [];
  if (!args.auth) targets.push(CONFIG_PATH);
  if (!args.config) targets.push(AUTH_PATH);
  const list = args.config || args.auth ? targets : [CONFIG_PATH, AUTH_PATH];

  let done = 0;
  for (const p of list) {
    const bak = `${p}.bak`;
    if (!existsSync(bak)) { warn(`没有备份，跳过：${bak}`); continue; }
    if (existsSync(p)) {
      const pre = `${p}.pre-rollback`;
      try {
        copyFileSync(p, pre);
        ok(`当前文件已另存 → ${pre}`);
      } catch (e) {
        fail(`另存当前文件失败：${errLine(e)} —— 为安全起见跳过该项`);
        continue;
      }
    }
    try {
      copyFileSync(bak, p);
      ok(`已从 ${bak} 恢复 → ${p}`);
      done++;
    } catch (e) {
      fail(`恢复失败：${errLine(e)}`);
    }
  }

  if (!done) { log('\n没有恢复任何文件。'); process.exit(1); }
  log('\n提示：改完配置必须**重启 `devspace serve`** 才生效（配置只在启动时读一次）。');
  log('      若 ownerToken 变了，下次授权要用新的密码。');
}

const args = parseArgs(process.argv.slice(2));
const cmd = args._[0] || 'check';

if (cmd === 'check') doctor();
else if (cmd === 'apply') apply(args);
else if (cmd === 'rollback') rollback(args);
else {
  log('用法:');
  log('  node devspace-bootstrap.mjs check');
  log('  node devspace-bootstrap.mjs apply --roots "D:\\projects\\my-app" [--dry-run] [--force]');
  log('  node devspace-bootstrap.mjs rollback [--config|--auth]');
  process.exit(1);
}
