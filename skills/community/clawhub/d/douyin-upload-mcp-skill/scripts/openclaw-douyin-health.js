#!/usr/bin/env node
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { homedir } from 'node:os';
import '../src/config.js';

const root = new URL('..', import.meta.url).pathname.replace(/\/$/, '');
const nodeBin = process.execPath;
const args = new Set(process.argv.slice(2));
const fix = args.has('--fix');
const restart = args.has('--restart-gateway');
const openclawConfigPath = process.env.OPENCLAW_CONFIG_PATH || join(homedir(), '.openclaw', 'openclaw.json');
const gatewayService = process.env.OPENCLAW_GATEWAY_SERVICE || 'openclaw-gateway.service';
const supervisorService = process.env.DOUYIN_SUPERVISOR_SERVICE || 'douyin-skill-supervisor.service';
const daemonPort = process.env.DAEMON_PORT || '40225';

function run(command, commandArgs = [], opts = {}) {
  return spawnSync(command, commandArgs, {
    cwd: opts.cwd || root,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: opts.timeout || 120000,
    env: {
      ...process.env,
      PATH: `${dirname(nodeBin)}:${process.env.PATH || ''}`,
      ...(opts.env || {}),
    },
  });
}

function check(name, ok, detail = '', fixHint = '') {
  return { name, ok: Boolean(ok), detail, fix: fixHint };
}

function readJson(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

function serviceActive(name) {
  const res = run('systemctl', ['--user', 'is-active', name]);
  const detail = (res.stdout || res.stderr).trim();
  return {
    ok: res.stdout.trim() === 'active',
    unavailable: /Failed to connect to bus|No such file or directory|System has not been booted/i.test(detail),
    detail,
  };
}

async function daemonHealth() {
  let last = null;
  for (let i = 0; i < 10; i += 1) {
    try {
      const res = await fetch(`http://127.0.0.1:${daemonPort}/health`, {
        signal: AbortSignal.timeout(2000),
      });
      const body = await res.json();
      if (body.ok) return body;
      last = body;
    } catch (err) {
      last = { ok: false, error: err.message };
    }
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
  return last || { ok: false, error: 'unknown daemon health failure' };
}

function mcpConfigured() {
  if (!existsSync(openclawConfigPath)) return { ok: false, detail: `${openclawConfigPath} missing` };
  const cfg = readJson(openclawConfigPath);
  const server = cfg.mcp?.servers?.douyin;
  const expectedArg = join(root, 'src', 'mcp-server.js');
  const ok = server?.command === nodeBin
    && server?.cwd === root
    && Array.isArray(server?.args)
    && server.args[0] === expectedArg;
  return {
    ok,
    detail: JSON.stringify({
      command: server?.command || '',
      expectedCommand: nodeBin,
      args: server?.args || [],
      expectedArg,
      cwd: server?.cwd || '',
      expectedCwd: root,
    }),
  };
}

function mcpProcessRunning() {
  const res = run('pgrep', ['-af', `${root}/src/mcp-server.js`]);
  const lines = (res.stdout || '').trim().split('\n').filter(Boolean);
  return { ok: lines.length > 0, detail: lines.join('\n') };
}

async function main() {
  if (fix) {
    run(nodeBin, ['scripts/bootstrap-openclaw.js', '--apply'], { timeout: 300000 });
    run('systemctl', ['--user', 'restart', supervisorService]);
    if (restart) run('systemctl', ['--user', 'restart', gatewayService]);
  }

  const gateway = serviceActive(gatewayService);
  const supervisor = serviceActive(supervisorService);
  const daemon = await daemonHealth();
  const mcpConfig = mcpConfigured();
  const mcpProcess = mcpProcessRunning();

  const checks = [
    check('openclaw_gateway_active', gateway.ok, gateway.detail, `systemctl --user restart ${gatewayService}`),
    check('douyin_supervisor_active', supervisor.ok, supervisor.detail, `systemctl --user restart ${supervisorService}`),
    check('douyin_daemon_health', daemon.ok, JSON.stringify(daemon), `systemctl --user restart ${supervisorService}`),
    check('openclaw_mcp_config_absolute_node', mcpConfig.ok, mcpConfig.detail, 'node scripts/bootstrap-openclaw.js --apply'),
    check('douyin_mcp_process_seen', mcpProcess.ok, mcpProcess.detail || 'not currently spawned; OpenClaw may lazy-load MCP until first tool call', `systemctl --user restart ${gatewayService}`),
  ];
  const systemdUnavailable = gateway.unavailable && supervisor.unavailable;
  const nonBlocking = new Set([
    'douyin_mcp_process_seen',
    ...(systemdUnavailable && mcpConfig.ok ? ['openclaw_gateway_active', 'douyin_supervisor_active'] : []),
    ...(systemdUnavailable && mcpConfig.ok && !daemon.ok ? ['douyin_daemon_health'] : []),
  ]);
  const blocking = checks.filter((item) => !nonBlocking.has(item.name));
  const ok = blocking.every((item) => item.ok);
  console.log(JSON.stringify({ ok, fixApplied: fix, gatewayRestarted: fix && restart, systemdUnavailable, checks }, null, 2));
  if (!ok) process.exitCode = 1;
}

main().catch((err) => {
  console.log(JSON.stringify({ ok: false, error: err.message, stack: err.stack }, null, 2));
  process.exitCode = 1;
});
