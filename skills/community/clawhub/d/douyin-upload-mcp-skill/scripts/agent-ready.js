#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import '../src/config.js';

function run(command, args, opts = {}) {
  return spawnSync(command, args, {
    cwd: opts.cwd || process.cwd(),
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: opts.timeout || 120000,
  });
}

function parseJson(text) {
  const start = text.indexOf('{');
  const end = text.lastIndexOf('}');
  if (start < 0 || end <= start) return null;
  try {
    return JSON.parse(text.slice(start, end + 1));
  } catch {
    return null;
  }
}

function check(name, ok, detail = '', fix = '') {
  return { name, ok: Boolean(ok), detail, fix };
}

function isMissingBitableState(payload, text) {
  const error = String(payload?.error || text || '');
  return /bitable state is missing|Run sync-douyin-data-to-feishu-bitable/i.test(error);
}

async function main() {
  const checks = [];
  const daemonPort = process.env.DAEMON_PORT || '40225';
  const preflight = run(process.execPath, ['scripts/preflight.js', '--online'], { timeout: 180000 });
  checks.push(check(
    'skill_preflight_online',
    preflight.status === 0,
    (preflight.stdout || preflight.stderr).slice(-1200),
    'Fix failed checks from scripts/preflight.js --online.',
  ));

  const helpOk = run(process.execPath, ['scripts/help.js']);
  checks.push(check('quick_help', helpOk.status === 0 && /Douyin Creator Ops Skill/.test(helpOk.stdout), helpOk.stdout.slice(0, 300)));

  const bitable = run(process.execPath, ['scripts/douyin-data-report-from-bitable.js', '--days', '90'], { timeout: 120000 });
  const bitablePayload = parseJson(bitable.stdout || bitable.stderr || '');
  const bitableStateMissing = isMissingBitableState(bitablePayload, bitable.stdout || bitable.stderr || '');
  checks.push(check(
    'bitable_report_no_browser',
    bitable.status === 0 && bitablePayload?.ok,
    bitableStateMissing
      ? 'not initialized: run data sync before first report'
      : (bitablePayload ? `works=${bitablePayload.counts?.works}, source=${bitablePayload.source}` : (bitable.stdout || bitable.stderr).slice(-800)),
    'Run scripts/sync-douyin-data-to-feishu-bitable.js --days 90 --notify before first data report.',
  ));

  const daemonHealth = await fetch(`http://127.0.0.1:${daemonPort}/health`).then((res) => res.json()).catch((err) => ({ ok: false, error: err.message }));
  checks.push(check(
    'douyin_daemon_health',
    daemonHealth.ok,
    JSON.stringify(daemonHealth).slice(0, 500),
    `Run npm run daemon from this skill directory, or call a browser MCP tool once to auto-start it. Expected DAEMON_PORT=${daemonPort}.`,
  ));

  const displayReady = Boolean(process.env.DISPLAY || process.env.WAYLAND_DISPLAY || existsSync('/tmp/.X11-unix'));
  checks.push(check(
    'graphical_display_hint',
    displayReady,
    `DISPLAY=${process.env.DISPLAY || ''}, WAYLAND_DISPLAY=${process.env.WAYLAND_DISPLAY || ''}`,
    'Browser tasks need an existing GUI/daemon/CDP path. If OpenClaw local agent reports X Server missing, run browser tasks through the existing daemon or start an X server.',
  ));

  const nonBlocking = new Set([
    'graphical_display_hint',
    ...(bitableStateMissing ? ['bitable_report_no_browser'] : []),
  ]);
  const ok = checks.filter((item) => !nonBlocking.has(item.name)).every((item) => item.ok);
  console.log(JSON.stringify({
    ok,
    agentCanRunNoBrowserTools: checks.find((item) => item.name === 'bitable_report_no_browser')?.ok || false,
    dataReportNeedsInitialSync: bitableStateMissing,
    browserTasksNeedDisplayOrDaemon: true,
    checks,
  }, null, 2));
  if (!ok) process.exit(1);
}

main().catch((err) => {
  console.log(JSON.stringify({ ok: false, error: err.message, stack: err.stack }, null, 2));
  process.exit(1);
});
