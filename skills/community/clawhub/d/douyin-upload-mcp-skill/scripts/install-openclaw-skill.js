#!/usr/bin/env node
import { cpSync, existsSync, mkdirSync, realpathSync, rmSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { homedir } from 'node:os';
import { spawnSync } from 'node:child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const sourceRoot = resolve(__dirname, '..');
const args = new Set(process.argv.slice(2));
const apply = args.has('--apply');
const replace = args.has('--replace');
const standaloneWatcher = args.has('--standalone-watcher');
const enableService = args.has('--enable');
const resetBrowserProfile = args.has('--reset-browser-profile');
const skipSchedule = args.has('--skip-schedule');
const help = args.has('--help') || args.has('-h');
const targetArg = valueAfter('--target');
const targetRoot = resolve(targetArg || join(homedir(), '.openclaw', 'skills', 'douyin-upload-mcp-skill'));

function valueAfter(flag) {
  const argv = process.argv.slice(2);
  const index = argv.indexOf(flag);
  if (index < 0) return '';
  return argv[index + 1] || '';
}

function run(command, commandArgs = [], opts = {}) {
  return spawnSync(command, commandArgs, {
    cwd: opts.cwd || targetRoot,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: opts.timeout || 300000,
    env: {
      ...process.env,
      ...(opts.env || {}),
    },
  });
}

function check(name, ok, detail = '', fix = '') {
  return { name, ok: Boolean(ok), detail, fix };
}

function samePath(a, b) {
  try {
    return realpathSync(a) === realpathSync(b);
  } catch {
    return resolve(a) === resolve(b);
  }
}

function copySkill(checks) {
  const alreadyInPlace = existsSync(targetRoot) && samePath(sourceRoot, targetRoot);
  if (alreadyInPlace) {
    checks.push(check('copy_skill', true, `already in ${targetRoot}`));
    return;
  }
  if (!apply) {
    checks.push(check('copy_skill', false, `${sourceRoot} -> ${targetRoot}`, 'Run with --apply to copy skill into OpenClaw skills directory.'));
    return;
  }
  if (replace) rmSync(targetRoot, { recursive: true, force: true });
  mkdirSync(targetRoot, { recursive: true });
  cpSync(sourceRoot, targetRoot, {
    recursive: true,
    force: true,
    dereference: false,
    filter: (src) => {
      const rel = src.slice(sourceRoot.length).replace(/^\/+/, '');
      if (!rel) return true;
      return ![
        '.git',
        'node_modules',
        'douyin-output',
        'test',
        'temp',
      ].some((blocked) => rel === blocked || rel.startsWith(`${blocked}/`))
        && !rel.endsWith('.log')
        && !rel.includes('/__pycache__/')
        && !rel.endsWith('.pyc');
    },
  });
  checks.push(check('copy_skill', existsSync(join(targetRoot, 'SKILL.md')), `${sourceRoot} -> ${targetRoot}`));
}

function runBootstrap(checks) {
  if (!existsSync(join(targetRoot, 'scripts', 'bootstrap-openclaw.js'))) {
    checks.push(check('bootstrap_openclaw', false, 'missing scripts/bootstrap-openclaw.js', 'Check package extraction/copy.'));
    return;
  }
  if (!apply) {
    const result = run(process.execPath, ['scripts/bootstrap-openclaw.js'], { timeout: 360000 });
    checks.push(check('bootstrap_openclaw_check', result.status === 0, (result.stdout || result.stderr).slice(-1500), 'Run with --apply to configure OpenClaw.'));
    return;
  }
  const bootstrapArgs = ['scripts/bootstrap-openclaw.js', '--apply'];
  if (standaloneWatcher) bootstrapArgs.push('--standalone-watcher');
  if (enableService) bootstrapArgs.push('--enable');
  if (resetBrowserProfile) bootstrapArgs.push('--reset-browser-profile');
  const result = run(process.execPath, bootstrapArgs, { timeout: 600000 });
  checks.push(check('bootstrap_openclaw_apply', result.status === 0, (result.stdout || result.stderr).slice(-2000), 'Fix bootstrap blockers and rerun installer.'));
}

function installSchedule(checks) {
  if (skipSchedule) {
    checks.push(check('schedule_install', true, 'skipped by --skip-schedule'));
    return;
  }
  if (!apply) {
    checks.push(check('schedule_install', true, 'not applied; will run with --apply'));
    return;
  }
  const result = run(process.execPath, ['scripts/douyin-schedule-manager.js', 'install-default'], { timeout: 180000 });
  checks.push(check('schedule_install', result.status === 0, (result.stdout || result.stderr).slice(-1200), 'Check douyin-schedule-manager.js output.'));
}

function finalChecks(checks) {
  if (!apply) return;
  const preflight = run(process.execPath, ['scripts/preflight.js', '--online'], { timeout: 300000 });
  checks.push(check('preflight_online', preflight.status === 0, (preflight.stdout || preflight.stderr).slice(-1500), 'Configure missing Feishu/OpenClaw/browser items.'));
  const ready = run(process.execPath, ['scripts/agent-ready.js'], { timeout: 300000 });
  checks.push(check('agent_ready', ready.status === 0, (ready.stdout || ready.stderr).slice(-1500), 'Check agent-ready output.'));
}

if (help) {
  console.log(`Usage:
  node scripts/install-openclaw-skill.js --apply
  node scripts/install-openclaw-skill.js --apply --replace
  node scripts/install-openclaw-skill.js --apply --standalone-watcher

Options:
  --target <dir>             Default: ~/.openclaw/skills/douyin-upload-mcp-skill
  --replace                  Remove target skill directory before copying
  --standalone-watcher       Use skill watcher instead of OpenClaw gateway Feishu mode
  --enable                   Enable the user systemd supervisor service
  --reset-browser-profile    Clear target browser profile during bootstrap
  --skip-schedule            Do not install default scheduled jobs

Without --apply it only checks what would be configured.`);
  process.exit(0);
}

const checks = [];
checks.push(check('node_version', Number(process.versions.node.split('.')[0]) >= 22, process.versions.node, 'Install Node.js 22+.'));
copySkill(checks);
runBootstrap(checks);
installSchedule(checks);
finalChecks(checks);

const blockers = checks.filter((item) => !item.ok);
console.log(JSON.stringify({
  ok: blockers.length === 0,
  applied: apply,
  sourceRoot,
  targetRoot,
  mode: standaloneWatcher ? 'standalone-watcher' : 'openclaw-gateway',
  nextHumanSteps: [
    'If Feishu credentials or receive chat id are missing, fill .env.local or OpenClaw Feishu account config.',
    'If Bitable authorization is missing, authorize it from Feishu/OpenClaw when prompted.',
    'First Douyin use still requires QR scan and possible SMS/security verification.',
    'After install, test in Feishu with: 定时任务 / 自动化营销状态 / 发布抖音.',
  ],
  checks,
  blockers,
}, null, 2));

if (blockers.length) process.exitCode = 1;
