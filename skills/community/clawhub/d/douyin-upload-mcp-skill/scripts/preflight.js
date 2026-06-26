#!/usr/bin/env node
import { existsSync, mkdirSync, accessSync, constants, readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { platform, homedir } from 'node:os';
import config from '../src/config.js';
import { resolveFeishuConfig, getTenantAccessToken } from './feishu-client.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');
const args = new Set(process.argv.slice(2));
const home = homedir();

function check(name, ok, detail = '', fix = '') {
  return { name, ok: Boolean(ok), detail, fix };
}

function canWrite(dir) {
  try {
    mkdirSync(dir, { recursive: true });
    accessSync(dir, constants.W_OK);
    return true;
  } catch {
    return false;
  }
}

function run(command, commandArgs = []) {
  return spawnSync(command, commandArgs, {
    cwd: root,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
}

function resolveHomePath(value) {
  const text = String(value || '').trim();
  if (!text) return '';
  if (text === '~') return home;
  if (text.startsWith('~/')) return join(home, text.slice(2));
  return text;
}

function parseEnvFile(path) {
  if (!existsSync(path)) return {};
  const env = {};
  for (const rawLine of readFileSync(path, 'utf8').split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#') || !line.includes('=')) continue;
    const index = line.indexOf('=');
    const key = line.slice(0, index).trim();
    let value = line.slice(index + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    if (key) env[key] = value;
  }
  return env;
}

function hasConfiguredValue(env, key, disallowed = []) {
  const value = String(env[key] || '').trim();
  if (!value) return false;
  const lower = value.toLowerCase();
  return !disallowed.some((item) => lower === item.toLowerCase() || lower.includes(item.toLowerCase()));
}

function detectBrowser() {
  if (config.browserPath && existsSync(config.browserPath)) return config.browserPath;
  const candidates = platform() === 'linux'
    ? [
        '/usr/bin/microsoft-edge',
        '/usr/bin/microsoft-edge-stable',
        '/opt/microsoft/msedge-beta/msedge',
        '/usr/bin/google-chrome',
        '/usr/bin/google-chrome-stable',
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
      ]
    : [];
  return candidates.find((item) => existsSync(item)) || null;
}

async function main() {
  const results = [];
  const nodeMajor = Number(process.versions.node.split('.')[0]);

  results.push(check(
    'node_version',
    nodeMajor >= 22,
    process.versions.node,
    'Install Node.js 22+.',
  ));

  results.push(check(
    'package_json',
    existsSync(join(root, 'package.json')),
    join(root, 'package.json'),
  ));

  results.push(check(
    'node_modules',
    existsSync(join(root, 'node_modules', 'puppeteer-core')),
    join(root, 'node_modules'),
    'Run npm install in the skill directory.',
  ));

  const syntaxFiles = [
    'src/mcp-server.js',
    'scripts/douyin-login-monitor.js',
    'scripts/feishu-reply-watcher.js',
    'scripts/publish-with-guard.js',
    'scripts/douyin-cli.js',
    'scripts/inspect-publish-fields.js',
    'scripts/validate-publish-task.js',
    'scripts/run-publish-task-stability.js',
    'scripts/douyin-schedule-manager.js',
  ];
  for (const file of syntaxFiles) {
    const res = run(process.execPath, ['--check', file]);
    results.push(check(
      `syntax:${file}`,
      res.status === 0,
      (res.stderr || res.stdout || '').trim(),
      `Fix syntax in ${file}.`,
    ));
  }

  const browser = detectBrowser();
  results.push(check(
    'browser_executable',
    browser,
    browser || `configured=${config.browserPath || '(auto)'}`,
    'Install Chrome/Edge or set BROWSER_PATH.',
  ));

  const xvfb = run('bash', ['-lc', 'command -v xvfb-run || true']);
  const displayReady = Boolean(process.env.DISPLAY || process.env.WAYLAND_DISPLAY || existsSync('/tmp/.X11-unix'));
  results.push(check(
    'display_or_xvfb',
    displayReady || Boolean((xvfb.stdout || '').trim()),
    `DISPLAY=${process.env.DISPLAY || ''}, WAYLAND_DISPLAY=${process.env.WAYLAND_DISPLAY || ''}, xvfb=${(xvfb.stdout || '').trim() || '(missing)'}`,
    'Install xvfb or ensure WSLg DISPLAY/WAYLAND_DISPLAY is available.',
  ));

  const cjkFontProbe = run(process.execPath, [join(root, 'scripts', 'ensure-cjk-fonts.js')]);
  let cjkPayload = null;
  try {
    const raw = `${cjkFontProbe.stdout || ''}${cjkFontProbe.stderr || ''}`.trim();
    cjkPayload = raw ? JSON.parse(raw.slice(raw.indexOf('{'))) : null;
  } catch {
    cjkPayload = null;
  }
  results.push(check(
    'wsl_cjk_fonts',
    cjkFontProbe.status === 0 && cjkPayload?.ok,
    cjkPayload ? JSON.stringify(cjkPayload).slice(0, 700) : `${cjkFontProbe.stdout || ''}${cjkFontProbe.stderr || ''}`.trim().slice(-700),
    'Check Windows font mount or install a CJK font package on WSL.',
  ));

  const qrPython = process.env.DOUYIN_QR_PYTHON
    || (existsSync('/opt/python-env/bin/python3') ? '/opt/python-env/bin/python3' : 'python3');
  const qrDependency = run(qrPython, ['-c', 'import PIL; print("pillow ok")']);
  results.push(check(
    'qr_detector_pillow',
    qrDependency.status === 0,
    (qrDependency.stdout || qrDependency.stderr || '').trim().slice(-500),
    'Install python3-pil or set DOUYIN_QR_PYTHON to a Python environment with Pillow.',
  ));

  const browserDataDir = config.browserUserDataDir || join(homedir(), '.wjz_browser_data');
  results.push(check(
    'browser_user_data_dir_writable',
    canWrite(browserDataDir),
    browserDataDir,
    'Set BROWSER_USER_DATA_DIR to a writable path.',
  ));

  results.push(check(
    'output_dir_writable',
    canWrite(config.outputDir),
    config.outputDir,
    'Set OUTPUT_DIR to a writable path.',
  ));

  const workspaceDir = join(homedir(), '.openclaw', 'workspace', 'douyin-ops');
  results.push(check(
    'workspace_dir_writable',
    canWrite(workspaceDir),
    workspaceDir,
    'Create a writable OpenClaw workspace directory.',
  ));

  const xiaoiceToolDir = resolveHomePath(process.env.XIAOICE_VIDEO_TOOL_DIR || join(home, '自动营销', 'xiaoice-video-tool'));
  const xiaoiceEnvPath = resolveHomePath(process.env.XIAOICE_VIDEO_ENV_PATH || join(xiaoiceToolDir, '.env'));
  const xiaoiceEnv = { ...parseEnvFile(xiaoiceEnvPath), ...process.env };
  results.push(check(
    'xiaoice_video_tool',
    existsSync(join(xiaoiceToolDir, 'src', 'service', 'cli.js')),
    xiaoiceToolDir,
    'Run node scripts/bootstrap-openclaw.js --apply to install vendor/xiaoice-video-tool.',
  ));
  results.push(check(
    'xiaoice_video_env',
    existsSync(xiaoiceEnvPath),
    xiaoiceEnvPath,
    'Create XiaoIce .env from references/xiaoice-service-config.md or vendor/xiaoice-video-tool/.env.example and fill provider keys.',
  ));
  const xiaoiceRequired = [
    ['VIDEO_SERVICE_INTERNAL_TOKEN', ['dev-internal-token-change-me', 'replace-me']],
    ['VIDEO_SERVICE_ADMIN_TOKEN', ['dev-admin-token-change-me', 'replace-me']],
    ['VIDEO_SERVICE_CALLBACK_TOKEN', ['dev-callback-token-change-me', 'replace-me']],
    ['VIDEO_PROVIDER_API_BASE_URL', ['127.0.0.1:3999', 'example']],
    ['VIDEO_PROVIDER_API_KEY', ['replace-me', 'your-', 'example']],
  ];
  const missingXiaoice = xiaoiceRequired
    .filter(([key, disallowed]) => !hasConfiguredValue(xiaoiceEnv, key, disallowed))
    .map(([key]) => key);
  results.push(check(
    'xiaoice_video_provider_config',
    missingXiaoice.length === 0,
    missingXiaoice.length ? `missing=${missingXiaoice.join(', ')}, env=${xiaoiceEnvPath}` : `env=${xiaoiceEnvPath}`,
    'Fill XiaoIce video provider keys and service tokens in the XiaoIce .env file.',
  ));

  const feishu = resolveFeishuConfig();
  results.push(check(
    'feishu_target_config',
    feishu.appId && feishu.appSecret && feishu.receiveId && feishu.receiveIdType,
    `receiveId=${feishu.receiveId || '(missing)'}, receiveIdType=${feishu.receiveIdType || '(missing)'}, dryRun=${feishu.dryRun}`,
    'Configure FEISHU_APP_ID/FEISHU_APP_SECRET or OpenClaw feishu account, plus DOUYIN_FEISHU_RECEIVE_ID.',
  ));

  if (args.has('--online')) {
    try {
      await getTenantAccessToken(feishu);
      results.push(check('feishu_token_online', true, 'tenant token ok'));
    } catch (err) {
      results.push(check('feishu_token_online', false, err.message, 'Check Feishu app credentials and network.'));
    }
  }

  const passed = results.every((item) => item.ok);
  const summary = {
    ok: passed,
    root,
    commandForFullFlow: 'node scripts/feishu-reply-watcher.js watch --since-seconds 1800 --interval-ms 1000 --page-size 50 --max-pages 10',
    commandBeforeColdStart: 'node scripts/feishu-reply-watcher.js poll --init',
    screenshotCommand: 'node scripts/douyin-cli.js screenshot',
    checks: results,
  };

  console.log(JSON.stringify(summary, null, 2));
  if (!passed) process.exitCode = 1;
}

main().catch((err) => {
  console.error(JSON.stringify({ ok: false, error: err.message, stack: err.stack }, null, 2));
  process.exitCode = 1;
});
