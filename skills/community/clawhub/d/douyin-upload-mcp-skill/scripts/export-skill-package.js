#!/usr/bin/env node
import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { homedir, tmpdir } from 'node:os';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');
const rawArgs = process.argv.slice(2);
const includeEnv = rawArgs.includes('--include-env');
const help = rawArgs.includes('--help') || rawArgs.includes('-h');
const positional = rawArgs.filter((item) => !item.startsWith('--'));
const outDir = positional[0] ? resolve(positional[0]) : dirname(root);
const stamp = new Date().toISOString().replace(/[-:.TZ]/g, '').slice(0, 14);
const outPath = join(outDir, `douyin-upload-mcp-skill${includeEnv ? '-private-env' : ''}-${stamp}.tar.gz`);
const openclawConfigPath = process.env.OPENCLAW_CONFIG_PATH || join(homedir(), '.openclaw', 'openclaw.json');

if (help) {
  console.log(`Usage:
  node scripts/export-skill-package.js [out-dir]
  node scripts/export-skill-package.js [out-dir] --include-env

Default excludes .env/.env.local. Use --include-env only for trusted private transfer.
Browser login state and runtime workspace are never included.`);
  process.exit(0);
}

mkdirSync(outDir, { recursive: true });

function readJson(path) {
  try {
    if (!existsSync(path)) return null;
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return null;
  }
}

function parseEnv(text) {
  const result = {};
  for (const line of String(text || '').split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#') || !trimmed.includes('=')) continue;
    const index = trimmed.indexOf('=');
    const key = trimmed.slice(0, index).trim();
    let value = trimmed.slice(index + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    if (key) result[key] = value;
  }
  return result;
}

function serializeEnv(env) {
  return Object.entries(env)
    .filter(([key]) => key)
    .map(([key, value]) => `${key}=${String(value ?? '').replace(/\n/g, '\\n')}`)
    .join('\n') + '\n';
}

function configuredFeishuFromOpenClaw() {
  const cfg = readJson(openclawConfigPath);
  const feishu = cfg?.channels?.feishu;
  if (!feishu) return {};
  const accountId = process.env.FEISHU_ACCOUNT_ID || feishu.defaultAccount;
  const account = accountId ? feishu.accounts?.[accountId] : null;
  return {
    FEISHU_APP_ID: account?.appId || feishu.appId || '',
    FEISHU_APP_SECRET: account?.appSecret || feishu.appSecret || '',
  };
}

function preparePackageRoot() {
  if (!includeEnv) return { packageRoot: root, cleanup: () => null, injectedEnvKeys: [] };
  const tempParent = mkdtempSync(join(tmpdir(), 'douyin-skill-package-'));
  const tempRoot = join(tempParent, 'douyin-upload-mcp-skill');
  cpSync(root, tempRoot, {
    recursive: true,
    force: true,
    dereference: false,
    filter: (src) => {
      const rel = src.slice(root.length).replace(/^\/+/, '');
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
  const envLocalPath = join(tempRoot, '.env.local');
  const existing = existsSync(envLocalPath) ? parseEnv(readFileSync(envLocalPath, 'utf8')) : {};
  const feishu = configuredFeishuFromOpenClaw();
  const injected = {};
  for (const [key, value] of Object.entries(feishu)) {
    if (value && !existing[key]) injected[key] = value;
  }
  if (Object.keys(injected).length) {
    writeFileSync(envLocalPath, serializeEnv({ ...existing, ...injected }));
  }
  return {
    packageRoot: tempRoot,
    cleanup: () => rmSync(tempParent, { recursive: true, force: true }),
    injectedEnvKeys: Object.keys(injected),
  };
}

const baseExcludes = [
  './.git',
  './node_modules',
  './**/node_modules',
  './douyin-output',
  './test',
  './temp',
  './vendor/xiaoice-video-tool/data',
  './vendor/xiaoice-video-tool/tmp',
  './vendor/xiaoice-video-tool/logs',
  './vendor/xiaoice-video-tool/*.db',
  './vendor/xiaoice-video-tool/*.sqlite',
  './vendor/xiaoice-video-tool/*.sqlite3',
  './*.log',
  './**/*.log',
  './scripts/__pycache__',
  './**/__pycache__',
  './*.pyc',
  './.DS_Store',
];
const envExcludes = includeEnv ? [] : [
  './.env',
  './.env.local',
  './.env.development',
  './.env.production',
  './.env.test',
  './.env.secret',
  './.env.secrets',
  './vendor/xiaoice-video-tool/.env',
  './vendor/xiaoice-video-tool/.env.local',
  './vendor/xiaoice-video-tool/.env.development',
];
const excludes = [...baseExcludes, ...envExcludes];
const prepared = preparePackageRoot();

const args = [
  '-czf',
  outPath,
  ...excludes.flatMap((item) => ['--exclude', item]),
  '-C',
  prepared.packageRoot,
  '.',
];

const result = spawnSync('tar', args, {
  cwd: prepared.packageRoot,
  encoding: 'utf8',
  stdio: ['ignore', 'pipe', 'pipe'],
  timeout: 120000,
});
prepared.cleanup();

const ok = result.status === 0;
console.log(JSON.stringify({
  ok,
  packagePath: outPath,
  includeEnv,
  injectedEnvKeys: prepared.injectedEnvKeys,
  warning: includeEnv
    ? 'This private package includes local environment secrets. Transfer only to a trusted machine and do not upload it publicly.'
    : 'This safe package excludes local environment secrets. Fill .env.local on the target machine.',
  excluded: excludes,
  nextSteps: [
    'mkdir -p /tmp/douyin-skill-install && tar -xzf package.tar.gz -C /tmp/douyin-skill-install',
    includeEnv ? 'Review .env/.env.local on the target machine and rotate keys if needed' : 'cp references/skill-local-config.md .env.local 2>/dev/null || cp .env.example .env.local, then fill target machine credentials',
    'cd /tmp/douyin-skill-install && node scripts/install-openclaw-skill.js --apply',
  ],
  stdout: result.stdout?.trim() || '',
  stderr: result.stderr?.trim() || '',
}, null, 2));

if (!ok) process.exit(1);
