#!/usr/bin/env node
import { copyFileSync, cpSync, existsSync, mkdirSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { homedir, userInfo } from 'node:os';
import { spawnSync } from 'node:child_process';
import '../src/config.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');
const home = homedir();
const args = new Set(process.argv.slice(2));
const apply = args.has('--apply');
const enable = args.has('--enable');
const startWatcher = args.has('--standalone-watcher');
const restartGateway = !args.has('--no-restart-openclaw-gateway');
const strictPreflight = args.has('--strict-preflight') || args.has('--online');
const skipPreflight = args.has('--skip-preflight');
const resetBrowserProfile = args.has('--reset-browser-profile') || process.env.DOUYIN_RESET_BROWSER_PROFILE === 'true';
const nodeBin = process.execPath;
const stateDir = process.env.DOUYIN_MONITOR_STATE_DIR || join(home, '.openclaw', 'workspace', 'douyin-ops');
const browserDebugPort = process.env.BROWSER_DEBUG_PORT || '18800';
const daemonPort = process.env.DAEMON_PORT || '40225';
const browserUserDataDir = process.env.BROWSER_USER_DATA_DIR || join(home, '.wjz_browser_data');
const systemdUserDir = join(home, '.config', 'systemd', 'user');
const serviceName = process.env.DOUYIN_BOOTSTRAP_SERVICE_NAME || 'douyin-skill-supervisor';
const serviceUnit = serviceName.endsWith('.service') ? serviceName : `${serviceName}.service`;
const servicePath = join(systemdUserDir, serviceUnit);
const gatewayServiceName = process.env.OPENCLAW_GATEWAY_SERVICE_NAME || 'openclaw-gateway';
const gatewayServiceUnit = gatewayServiceName.endsWith('.service') ? gatewayServiceName : `${gatewayServiceName}.service`;
const openclawConfigPath = process.env.OPENCLAW_CONFIG_PATH || join(home, '.openclaw', 'openclaw.json');
const cjkFontScript = join(root, 'scripts', 'ensure-cjk-fonts.js');
const vendorXiaoiceToolDir = join(root, 'vendor', 'xiaoice-video-tool');
const xiaoiceServiceConfigTemplate = join(root, 'references', 'xiaoice-service-config.md');
const defaultXiaoiceToolDir = join(home, '自动营销', 'xiaoice-video-tool');
const xiaoiceToolDir = resolveHomePath(process.env.XIAOICE_VIDEO_TOOL_DIR || defaultXiaoiceToolDir);
const xiaoiceEnvPath = resolveHomePath(process.env.XIAOICE_VIDEO_ENV_PATH || join(xiaoiceToolDir, '.env'));

function run(command, commandArgs = [], opts = {}) {
  const nodeDir = dirname(nodeBin);
  return spawnSync(command, commandArgs, {
    cwd: opts.cwd || root,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: opts.timeout || 120000,
    env: {
      ...process.env,
      PATH: `${nodeDir}:${process.env.PATH || ''}`,
      ...(opts.env || {}),
    },
  });
}

function check(name, ok, detail = '', fix = '') {
  return { name, ok: Boolean(ok), detail, fix };
}

function firstExisting(paths) {
  return paths.find((item) => item && existsSync(item)) || '';
}

function resolveHomePath(value) {
  const text = String(value || '').trim();
  if (!text) return '';
  if (text === '~') return home;
  if (text.startsWith('~/')) return join(home, text.slice(2));
  return text;
}

function detectBrowser() {
  return firstExisting([
    process.env.BROWSER_PATH,
    '/usr/bin/microsoft-edge',
    '/usr/bin/microsoft-edge-stable',
    '/opt/microsoft/msedge-beta/msedge',
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
  ]);
}

function readJson(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

function backupPath(path) {
  const stamp = new Date().toISOString().replace(/[-:.TZ]/g, '').slice(0, 14);
  return `${path}.bak-douyin-bootstrap-${stamp}`;
}

function desiredMcpEnv(currentEnv = {}) {
  const browser = detectBrowser();
  const receiveId = process.env.DOUYIN_FEISHU_RECEIVE_ID
    || process.env.FEISHU_RECEIVE_ID
    || currentEnv.DOUYIN_FEISHU_RECEIVE_ID
    || currentEnv.FEISHU_RECEIVE_ID;
  const receiveIdType = process.env.DOUYIN_FEISHU_RECEIVE_ID_TYPE
    || process.env.FEISHU_RECEIVE_ID_TYPE
    || currentEnv.DOUYIN_FEISHU_RECEIVE_ID_TYPE
    || currentEnv.FEISHU_RECEIVE_ID_TYPE
    || (receiveId ? 'chat_id' : undefined);

  return {
    ...currentEnv,
    ...(browser ? { BROWSER_PATH: browser } : {}),
    BROWSER_DEBUG_PORT: browserDebugPort,
    DAEMON_PORT: daemonPort,
    BROWSER_USER_DATA_DIR: browserUserDataDir,
    BROWSER_HEADLESS: 'false',
    OUTPUT_DIR: join(stateDir, 'output'),
    DOUYIN_MONITOR_STATE_DIR: stateDir,
    XIAOICE_VIDEO_TOOL_DIR: xiaoiceToolDir,
    XIAOICE_VIDEO_ENV_PATH: xiaoiceEnvPath,
    ...(receiveId ? { DOUYIN_FEISHU_RECEIVE_ID: receiveId } : {}),
    ...(receiveIdType ? { DOUYIN_FEISHU_RECEIVE_ID_TYPE: receiveIdType } : {}),
  };
}

function desiredMcpServer(currentServer = {}) {
  return {
    ...currentServer,
    command: nodeBin,
    args: [join(root, 'src', 'mcp-server.js')],
    cwd: root,
    env: desiredMcpEnv(currentServer.env || {}),
  };
}

function mcpServerLooksConfigured(server) {
  if (!server || typeof server !== 'object') return false;
  const desired = desiredMcpServer(server);
  const envKeys = Object.keys(desired.env || {});
  return server.command === desired.command
    && JSON.stringify(server.args || []) === JSON.stringify(desired.args)
    && server.cwd === desired.cwd
    && envKeys.every((key) => server.env?.[key] === desired.env[key]);
}

function summarizeMcpServer(server) {
  return {
    command: server?.command || '',
    argsOk: JSON.stringify(server?.args || []) === JSON.stringify([join(root, 'src', 'mcp-server.js')]),
    cwdOk: server?.cwd === root,
    envKeys: Object.keys(server?.env || {}).sort(),
  };
}

function detectDisplayEnv() {
  return {
    DISPLAY: process.env.DISPLAY || (existsSync('/tmp/.X11-unix/X0') ? ':0' : ''),
    WAYLAND_DISPLAY: process.env.WAYLAND_DISPLAY || '',
    XDG_RUNTIME_DIR: process.env.XDG_RUNTIME_DIR || `/run/user/${userInfo().uid}`,
    DBUS_SESSION_BUS_ADDRESS: process.env.DBUS_SESSION_BUS_ADDRESS || `unix:path=/run/user/${userInfo().uid}/bus`,
  };
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'\\''`)}'`;
}

async function fetchJson(url, options = {}) {
  try {
    const res = await fetch(url, {
      ...options,
      signal: AbortSignal.timeout(options.timeoutMs || 10000),
    });
    const text = await res.text();
    let payload = {};
    if (text) {
      try {
        payload = JSON.parse(text);
      } catch {
        payload = { raw: text };
      }
    }
    return { ok: res.ok, status: res.status, payload };
  } catch (error) {
    return { ok: false, error: error.message };
  }
}

function killBrowserPortProcesses() {
  const pattern = `remote-debugging-port=${browserDebugPort}`;
  return run('bash', ['-lc', `pkill -f ${shellQuote(pattern)} >/dev/null 2>&1 || true`], { timeout: 30000 });
}

async function primeBrowserAfterReset(checks) {
  if (!resetBrowserProfile) return;

  const release = await fetchJson(`http://127.0.0.1:${daemonPort}/browser/release`, {
    method: 'POST',
    timeoutMs: 10000,
  });
  const kill = killBrowserPortProcesses();
  rmSync(browserUserDataDir, { recursive: true, force: true });
  mkdirSync(browserUserDataDir, { recursive: true });

  let acquire = { ok: false };
  for (let attempt = 1; attempt <= 10; attempt += 1) {
    acquire = await fetchJson(`http://127.0.0.1:${daemonPort}/browser/acquire`, {
      timeoutMs: 15000,
    });
    if (acquire.ok && acquire.payload?.ok) break;
    await sleep(1000);
  }

  let status = { ok: false, payload: {} };
  for (let attempt = 1; attempt <= 10; attempt += 1) {
    status = await fetchJson(`http://127.0.0.1:${daemonPort}/browser/status`, {
      timeoutMs: 5000,
    });
    if (status.ok && status.payload?.status === 'online') break;
    await sleep(1000);
  }

  checks.push(check(
    'browser_cold_start',
    Boolean(acquire.ok && acquire.payload?.ok && status.payload?.status === 'online'),
    JSON.stringify({
      release: release.payload || release.error || null,
      killStatus: kill.status,
      acquire: acquire.payload || acquire.error || null,
      status: status.payload || status.error || null,
    }).slice(0, 800),
    'Check browser release, profile deletion, and /browser/acquire.',
  ));
}

function supervisorServiceText(includeReset = false) {
  const display = detectDisplayEnv();
  const envLines = [
    `PATH=${dirname(nodeBin)}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin`,
    display.DISPLAY ? `DISPLAY=${display.DISPLAY}` : '',
    display.WAYLAND_DISPLAY ? `WAYLAND_DISPLAY=${display.WAYLAND_DISPLAY}` : '',
    `XDG_RUNTIME_DIR=${display.XDG_RUNTIME_DIR}`,
    `DBUS_SESSION_BUS_ADDRESS=${display.DBUS_SESSION_BUS_ADDRESS}`,
    `BROWSER_DEBUG_PORT=${browserDebugPort}`,
    `DAEMON_PORT=${daemonPort}`,
    `BROWSER_USER_DATA_DIR=${browserUserDataDir}`,
    'BROWSER_HEADLESS=false',
    `OUTPUT_DIR=${join(stateDir, 'output')}`,
    `DOUYIN_MONITOR_STATE_DIR=${stateDir}`,
    includeReset ? 'DOUYIN_RESET_BROWSER_PROFILE=true' : '',
    `DOUYIN_SUPERVISOR_START_WATCHER=${startWatcher ? 'true' : 'false'}`,
    'DOUYIN_SUPERVISOR_START_SCHEDULER=true',
  ].filter(Boolean).map((line) => `Environment=${line}`).join('\n');

  return `[Unit]
Description=Douyin skill supervisor
After=default.target

[Service]
Type=simple
WorkingDirectory=${root}
${envLines}
ExecStart=${nodeBin} scripts/douyin-skill-supervisor.js
Restart=always
RestartSec=3
StandardOutput=append:${join(stateDir, 'logs', 'douyin-skill-supervisor.log')}
StandardError=append:${join(stateDir, 'logs', 'douyin-skill-supervisor.log')}

[Install]
WantedBy=default.target
`;
}

function serviceLooksConfigured(current, includeReset = false) {
  if (!current) return false;
  const required = [
    `WorkingDirectory=${root}`,
    `ExecStart=${nodeBin} scripts/douyin-skill-supervisor.js`,
    `Environment=BROWSER_DEBUG_PORT=${browserDebugPort}`,
    `Environment=DAEMON_PORT=${daemonPort}`,
    `Environment=BROWSER_USER_DATA_DIR=${browserUserDataDir}`,
    `Environment=OUTPUT_DIR=${join(stateDir, 'output')}`,
    `Environment=DOUYIN_MONITOR_STATE_DIR=${stateDir}`,
    ...(includeReset ? ['Environment=DOUYIN_RESET_BROWSER_PROFILE=true'] : []),
    `Environment=DOUYIN_SUPERVISOR_START_WATCHER=${startWatcher ? 'true' : 'false'}`,
    'Environment=DOUYIN_SUPERVISOR_START_SCHEDULER=true',
  ];
  return required.every((line) => current.includes(line));
}

function ensureNpmInstall(checks) {
  const modulesOk = existsSync(join(root, 'node_modules', 'puppeteer-core'));
  if (modulesOk) {
    checks.push(check('node_dependencies', true, 'node_modules present'));
    return;
  }
  if (!apply) {
    checks.push(check('node_dependencies', false, 'node_modules missing', 'Run npm install, or rerun bootstrap with --apply.'));
    return;
  }
  const installArgs = existsSync(join(root, 'package-lock.json')) ? ['ci'] : ['install'];
  const npm = run('npm', installArgs, { timeout: 300000 });
  checks.push(check(
    'node_dependencies',
    npm.status === 0 && existsSync(join(root, 'node_modules', 'puppeteer-core')),
    (npm.stdout || npm.stderr).slice(-1000),
    `npm ${installArgs.join(' ')} failed; check network/npm registry.`,
  ));
}

function installBrowser() {
  const script = `
set -e
find_browser() {
  for bin in microsoft-edge microsoft-edge-stable google-chrome google-chrome-stable chromium chromium-browser; do
    if command -v "$bin" >/dev/null 2>&1; then
      command -v "$bin"
      return 0
    fi
  done
  return 1
}
if find_browser; then exit 0; fi
if [ "$(id -u)" = "0" ]; then
  SUDO=""
elif command -v sudo >/dev/null 2>&1 && sudo -n true >/dev/null 2>&1; then
  SUDO="sudo"
else
  echo "sudo is required to install a browser automatically. Run sudo -v first, or install Chrome/Edge/Chromium manually." >&2
  exit 80
fi
$SUDO apt-get update
$SUDO apt-get install -y chromium-browser || $SUDO apt-get install -y chromium || {
  tmpdir="$(mktemp -d)"
  deb="$tmpdir/google-chrome-stable_current_amd64.deb"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL -o "$deb" https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  else
    wget -O "$deb" https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  fi
  $SUDO apt-get install -y "$deb"
}
find_browser
`;
  return run('bash', ['-lc', script], { timeout: 600000 });
}

function ensureBrowser(checks) {
  const before = detectBrowser();
  if (before) {
    checks.push(check('browser_executable', true, before));
    return;
  }

  if (!apply) {
    checks.push(check(
      'browser_executable',
      false,
      '(not found)',
      'Install Microsoft Edge/Chrome/Chromium, or rerun bootstrap with --apply to try automatic installation.',
    ));
    return;
  }

  const installed = installBrowser();
  const after = detectBrowser();
  checks.push(check(
    'browser_executable',
    Boolean(after),
    after || `${installed.stdout || ''}${installed.stderr || ''}`.trim().slice(-1200),
    'Install Chrome/Edge/Chromium manually, or set BROWSER_PATH in .env.local.',
  ));
}

function ensureXiaoiceTool(checks) {
  const vendorCli = join(vendorXiaoiceToolDir, 'src', 'service', 'cli.js');
  const vendorEnvExample = firstExisting([
    xiaoiceServiceConfigTemplate,
    join(vendorXiaoiceToolDir, '.env.example'),
  ]);
  if (!existsSync(vendorCli)) {
    checks.push(check(
      'xiaoice_video_tool_vendor',
      false,
      vendorXiaoiceToolDir,
      'The public package is incomplete; vendor/xiaoice-video-tool is missing.',
    ));
    return;
  }

  if (apply) {
    mkdirSync(dirname(xiaoiceToolDir), { recursive: true });
    cpSync(vendorXiaoiceToolDir, xiaoiceToolDir, {
      recursive: true,
      force: true,
      errorOnExist: false,
    });

    if (!existsSync(xiaoiceEnvPath)) {
      mkdirSync(dirname(xiaoiceEnvPath), { recursive: true });
      const installedEnvExample = firstExisting([
        xiaoiceServiceConfigTemplate,
        join(xiaoiceToolDir, '.env.example'),
        vendorEnvExample,
      ]);
      if (installedEnvExample) copyFileSync(installedEnvExample, xiaoiceEnvPath);
    }

    const installArgs = existsSync(join(xiaoiceToolDir, 'package-lock.json')) ? ['ci'] : ['install'];
    const npm = run('npm', installArgs, { cwd: xiaoiceToolDir, timeout: 300000 });
    checks.push(check(
      'xiaoice_video_tool_dependencies',
      npm.status === 0,
      (npm.stdout || npm.stderr).slice(-1000),
      `Run npm ${installArgs.join(' ')} in ${xiaoiceToolDir}.`,
    ));
  }

  checks.push(check(
    'xiaoice_video_tool_installed',
    existsSync(join(xiaoiceToolDir, 'src', 'service', 'cli.js')),
    xiaoiceToolDir,
    'Run node scripts/bootstrap-openclaw.js --apply to install vendored XiaoIce video tool.',
  ));
  checks.push(check(
    'xiaoice_video_env_file',
    existsSync(xiaoiceEnvPath),
    xiaoiceEnvPath,
    'Copy references/xiaoice-service-config.md or vendor/xiaoice-video-tool/.env.example to the XiaoIce .env path and fill provider keys.',
  ));
}

function parseJsonFromOutput(output) {
  const text = String(output || '').trim();
  if (!text) return null;
  const start = text.indexOf('{');
  if (start < 0) return null;
  try {
    return JSON.parse(text.slice(start));
  } catch {
    return null;
  }
}

function ensureCjkFonts(checks) {
  const result = run(nodeBin, [cjkFontScript], { timeout: 120000 });
  const payload = parseJsonFromOutput(`${result.stdout || ''}${result.stderr || ''}`);
  const ok = result.status === 0 && payload?.ok;
  checks.push(check(
    'wsl_cjk_fonts',
    ok,
    payload ? JSON.stringify(payload).slice(0, 700) : (result.stdout || result.stderr).slice(-700),
    'Check Windows font mount or install a CJK font package on WSL.',
  ));
}

function ensureService(checks) {
  const desired = supervisorServiceText(false);
  const current = existsSync(servicePath) ? readFileSync(servicePath, 'utf8') : '';
  if (!apply) {
    checks.push(check(
      'systemd_supervisor_service',
      serviceLooksConfigured(current),
      current ? servicePath : 'missing',
      `Rerun bootstrap with --apply to write ${serviceUnit}.`,
    ));
    return;
  }
  mkdirSync(systemdUserDir, { recursive: true });
  mkdirSync(join(stateDir, 'logs'), { recursive: true });
  if (current !== desired) writeFileSync(servicePath, desired);
  run('systemctl', ['--user', 'daemon-reload']);
  if (enable) run('systemctl', ['--user', 'enable', serviceUnit]);
  const start = run('systemctl', ['--user', 'restart', serviceUnit]);
  const active = run('systemctl', ['--user', 'is-active', serviceUnit]);
  const startedOk = start.status === 0 && active.stdout.trim() === 'active';

  checks.push(check(
    'systemd_supervisor_service',
    startedOk,
    `service=${servicePath}, active=${active.stdout.trim() || active.stderr.trim()}`,
    `Check systemctl --user status ${serviceUnit}.`,
  ));
}

function checkOpenClawConfig(checks) {
  if (!existsSync(openclawConfigPath)) {
    checks.push(check('openclaw_config', false, openclawConfigPath, 'Install/configure OpenClaw first.'));
    return false;
  }

  let cfg;
  try {
    cfg = readJson(openclawConfigPath);
  } catch (err) {
    checks.push(check('openclaw_config', false, err.message, 'Fix OpenClaw JSON config syntax.'));
    return false;
  }

  const current = cfg.mcp?.servers?.douyin;
  const configured = mcpServerLooksConfigured(current);
  if (!apply) {
    checks.push(check(
      'openclaw_mcp_registration',
      configured,
      JSON.stringify(summarizeMcpServer(current)).slice(0, 500),
      'Rerun bootstrap with --apply to register mcp.servers.douyin.',
    ));
    return false;
  }

  let changed = false;
  if (!configured) {
    const backup = backupPath(openclawConfigPath);
    writeFileSync(backup, `${JSON.stringify(cfg, null, 2)}\n`);
    cfg.mcp = cfg.mcp || {};
    cfg.mcp.servers = cfg.mcp.servers || {};
    cfg.mcp.servers.douyin = desiredMcpServer(current || {});
    writeFileSync(openclawConfigPath, `${JSON.stringify(cfg, null, 2)}\n`);
    changed = true;
  }

  const after = readJson(openclawConfigPath);
  const afterServer = after.mcp?.servers?.douyin;
  checks.push(check(
    'openclaw_mcp_registration',
    mcpServerLooksConfigured(afterServer),
    JSON.stringify(summarizeMcpServer(afterServer)).slice(0, 500),
    'Check mcp.servers.douyin in OpenClaw config.',
  ));
  return changed;
}

function checkOpenClawGateway(checks, mcpChanged) {
  if (startWatcher) {
    checks.push(check('openclaw_gateway_service', true, 'standalone watcher mode; gateway not required'));
    return;
  }

  const before = run('systemctl', ['--user', 'is-active', gatewayServiceUnit]);
  const beforeState = before.stdout.trim() || before.stderr.trim();
  if (beforeState !== 'active') {
    checks.push(check(
      'openclaw_gateway_service',
      false,
      `${gatewayServiceUnit}: ${beforeState || 'unknown'}`,
      `Start OpenClaw gateway, or use --standalone-watcher if this skill should receive Feishu directly.`,
    ));
    return;
  }

  if (apply && mcpChanged && restartGateway) {
    const restart = run('systemctl', ['--user', 'restart', gatewayServiceUnit]);
    const after = run('systemctl', ['--user', 'is-active', gatewayServiceUnit]);
    checks.push(check(
      'openclaw_gateway_service',
      restart.status === 0 && after.stdout.trim() === 'active',
      `${gatewayServiceUnit}: restarted=${restart.status === 0}, active=${after.stdout.trim() || after.stderr.trim()}`,
      `Check systemctl --user status ${gatewayServiceUnit}.`,
    ));
    return;
  }

  checks.push(check(
    'openclaw_gateway_service',
    true,
    `${gatewayServiceUnit}: active${mcpChanged ? ', restart skipped by --no-restart-openclaw-gateway' : ''}`,
  ));
}

async function main() {
  const checks = [];
  const nodeMajor = Number(process.versions.node.split('.')[0]);
  checks.push(check('node_version', nodeMajor >= 22, process.versions.node, 'Use Node.js 22+.'));

  ensureNpmInstall(checks);
  ensureCjkFonts(checks);
  ensureBrowser(checks);
  ensureXiaoiceTool(checks);

  mkdirSync(join(stateDir, 'output'), { recursive: true });
  mkdirSync(join(stateDir, 'logs'), { recursive: true });
  checks.push(check('state_dir', existsSync(stateDir), stateDir));

  ensureService(checks);
  if (apply) {
    await primeBrowserAfterReset(checks);
  }
  const mcpChanged = checkOpenClawConfig(checks);
  checkOpenClawGateway(checks, mcpChanged);

  if (!skipPreflight) {
    const preflightArgs = ['scripts/preflight.js', ...(strictPreflight ? ['--online'] : [])];
    const preflight = run(nodeBin, preflightArgs, { timeout: 240000 });
    let preflightPayload = null;
    try {
      const raw = preflight.stdout || preflight.stderr || '';
      preflightPayload = JSON.parse(raw.slice(raw.indexOf('{'), raw.lastIndexOf('}') + 1));
    } catch {
      // Keep raw output in detail.
    }
    const preflightOk = preflight.status === 0 && preflightPayload?.ok;
    checks.push(check(
      strictPreflight ? 'skill_preflight_online' : 'skill_preflight_hint',
      strictPreflight ? preflightOk : true,
      preflightPayload
        ? `actualOk=${Boolean(preflightPayload.ok)}, mode=${strictPreflight ? 'online' : 'offline'}`
        : (preflight.stdout || preflight.stderr).slice(-1200),
      strictPreflight
        ? 'Configure missing .env/OpenClaw/Feishu/Bitable/browser items reported by preflight.'
        : 'After filling .env.local and XiaoIce .env, run node scripts/preflight.js --online.',
    ));
  }

  const health = await fetch(`http://127.0.0.1:${daemonPort}/health`)
    .then((res) => res.json())
    .catch((err) => ({ ok: false, error: err.message }));
  checks.push(check(
    'douyin_daemon_health',
    health.ok,
    JSON.stringify(health).slice(0, 500),
    'Supervisor should start daemon; check logs/douyin-daemon.log.',
  ));

  const blockers = checks.filter((item) => !item.ok).map((item) => ({
    name: item.name,
    fix: item.fix,
    detail: item.detail,
  }));

  console.log(JSON.stringify({
    ok: blockers.length === 0,
    applied: apply,
    enabled: enable,
    mode: startWatcher ? 'standalone-watcher' : 'openclaw-gateway',
    root,
    stateDir,
    daemonPort,
    browserDebugPort,
    browserUserDataDir,
    serviceUnit,
    servicePath,
    gatewayServiceUnit,
    copyToNewOpenClawFirstCommand: 'node scripts/bootstrap-openclaw.js --apply',
    strictPreflight,
    skipPreflight,
    resetBrowserProfile,
    humanRequired: [
      'Feishu app credentials / receive chat id',
      'Feishu Bitable tenant authorization',
      'XiaoIce video provider keys in the XiaoIce .env file',
      'First Douyin QR scan and SMS verification',
      'Douyin security challenges such as slider/captcha',
    ],
    checks,
    blockers,
  }, null, 2));

  if (blockers.length) process.exitCode = 1;
}

main().catch((err) => {
  console.log(JSON.stringify({ ok: false, error: err.message, stack: err.stack }, null, 2));
  process.exitCode = 1;
});
