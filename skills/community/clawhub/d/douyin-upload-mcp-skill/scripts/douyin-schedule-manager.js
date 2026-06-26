#!/usr/bin/env node
import { appendFileSync, closeSync, existsSync, mkdirSync, openSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { sendFeishuText } from './feishu-client.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
function candidateNodeBins() {
  return [
    process.env.DOUYIN_NODE_BIN,
    process.env.OPENCLAW_NODE_BIN,
    process.execPath,
  ].filter(Boolean);
}

function nodeMajor(bin) {
  try {
    const result = spawnSync(bin, ['-p', 'process.versions.node.split(".")[0]'], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
      timeout: 5000,
    });
    return result.status === 0 ? Number(String(result.stdout || '').trim()) : 0;
  } catch {
    return 0;
  }
}

function resolveNodeBin() {
  return candidateNodeBins().find((bin) => nodeMajor(bin) >= 22) || process.execPath;
}

const NODE_BIN = resolveNodeBin();
const OPENCLAW_BIN = process.env.OPENCLAW_BIN || '';
const OPENCLAW_MJS = process.env.OPENCLAW_MJS
  || resolve(dirname(NODE_BIN), '..', 'lib', 'node_modules', 'openclaw', 'openclaw.mjs');
const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(process.env.HOME || '.', '.openclaw', 'workspace', 'douyin-ops');
const LOG_DIR = join(STATE_DIR, 'schedule-logs');
const LOCAL_CONFIG_PATH = join(STATE_DIR, 'schedule-config.json');
const LOCAL_STATE_PATH = join(STATE_DIR, 'schedule-state.json');
const LOCAL_LOCK_DIR = join(STATE_DIR, 'schedule-locks');
const TZ = process.env.DOUYIN_SCHEDULE_TZ || 'Asia/Shanghai';
const INSTALL_OPENCLAW_CRON = process.env.DOUYIN_INSTALL_OPENCLAW_CRON === 'true';

const JOBS = {
  autoReply: {
    name: 'douyin-auto-reply-30m',
    label: '自动回复',
    description: '每半小时检查新增未回复评论和未读私信，按内容自动回复；有回复或失败时通知飞书。',
    defaultSchedule: { kind: 'every', every: '30m' },
    defaultLocalSchedule: { kind: 'every', every: '30m' },
    timeoutSeconds: 3600,
    tick: 'tick-auto-reply',
  },
  dailyReport: {
    name: 'douyin-daily-data-report-0730',
    label: '每日数据报告',
    description: '每天 07:30 同步近 1 天抖音数据到飞书多维表，并发送数据分析报告和下一条视频方案。',
    defaultSchedule: { kind: 'cron', cron: '30 7 * * *', tz: TZ },
    defaultLocalSchedule: { kind: 'daily', time: '07:30', tz: TZ },
    timeoutSeconds: 7200,
    tick: 'tick-daily-report',
  },
  marketingDaily: {
    name: 'douyin-marketing-daily-0730',
    label: '自动化营销',
    description: '每天 07:30 执行数据更新、生成新视频并等待用户确认发布。',
    defaultSchedule: { kind: 'cron', cron: '30 7 * * *', tz: TZ },
    defaultLocalSchedule: { kind: 'daily', time: '07:30', tz: TZ },
    timeoutSeconds: 10800,
    tick: 'tick-marketing-daily',
  },
};

function usage() {
  console.error(`Usage:
  node scripts/douyin-schedule-manager.js install-default
  node scripts/douyin-schedule-manager.js status
  node scripts/douyin-schedule-manager.js enable
  node scripts/douyin-schedule-manager.js disable
  node scripts/douyin-schedule-manager.js set-auto-reply --every 30m
  node scripts/douyin-schedule-manager.js disable-auto-reply
  node scripts/douyin-schedule-manager.js set-marketing-daily --time 07:30
  node scripts/douyin-schedule-manager.js route-text --text "定时任务"
  node scripts/douyin-schedule-manager.js tick-auto-reply [--dry-run] [--notify-empty] [--limit 50]
  node scripts/douyin-schedule-manager.js tick-daily-report [--dry-run] [--days 1]
  node scripts/douyin-schedule-manager.js tick-marketing-daily [--dry-run] [--days 90] [--auto-confirm]
  node scripts/douyin-schedule-manager.js local-scheduler-once [--dry-run] [--force]
  node scripts/douyin-schedule-manager.js local-scheduler-loop
  node scripts/douyin-schedule-manager.js disable-openclaw-cron
`);
}

function parseArgs(argv) {
  const args = {};
  const positional = [];
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith('--')) {
      positional.push(item);
      continue;
    }
    const key = item.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) args[key] = true;
    else {
      args[key] = next;
      i += 1;
    }
  }
  args._ = positional;
  return args;
}

function run(command, args = [], opts = {}) {
  const result = spawnSync(command, args, {
    cwd: opts.cwd || ROOT,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: opts.timeout || 120000,
    env: {
      ...process.env,
      PATH: `${dirname(NODE_BIN)}:${process.env.PATH || ''}`,
      ...(opts.env || {}),
    },
  });
  const output = `${result.stderr || ''}${result.stdout || ''}`.trim();
  return {
    ok: result.status === 0,
    status: result.status,
    signal: result.signal,
    error: result.error?.message,
    output,
    stdout: result.stdout || '',
    stderr: result.stderr || '',
  };
}

function runOpenClaw(args = [], opts = {}) {
  if (OPENCLAW_BIN) {
    return run(OPENCLAW_BIN, args, opts);
  }
  return run(NODE_BIN, [OPENCLAW_MJS, ...args], opts);
}

function parseJsonObjects(text) {
  const objects = [];
  let depth = 0;
  let start = -1;
  let inString = false;
  let escaped = false;
  const source = String(text || '');
  for (let i = 0; i < source.length; i += 1) {
    const ch = source[i];
    if (inString) {
      if (escaped) escaped = false;
      else if (ch === '\\') escaped = true;
      else if (ch === '"') inString = false;
      continue;
    }
    if (ch === '"') inString = true;
    else if (ch === '{') {
      if (depth === 0) start = i;
      depth += 1;
    } else if (ch === '}') {
      depth -= 1;
      if (depth === 0 && start >= 0) {
        try {
          objects.push(JSON.parse(source.slice(start, i + 1)));
        } catch {
          // Ignore non-JSON spans in OpenClaw banners or script logs.
        }
        start = -1;
      }
    }
  }
  return objects;
}

function parseLastJson(text) {
  const objects = parseJsonObjects(text);
  return objects[objects.length - 1] || null;
}

function logEvent(name, payload) {
  mkdirSync(LOG_DIR, { recursive: true });
  appendFileSync(join(LOG_DIR, `${name}.jsonl`), `${JSON.stringify({
    ts: new Date().toISOString(),
    ...payload,
  })}\n`);
}

function readJsonFile(path, fallback) {
  try {
    if (!existsSync(path)) return fallback;
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return fallback;
  }
}

function writeJsonFile(path, payload) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`);
}

function defaultLocalConfig() {
  return {
    version: 1,
    enabled: true,
    jobs: {
      autoReply: { enabled: true, schedule: JOBS.autoReply.defaultLocalSchedule },
      dailyReport: { enabled: false, schedule: JOBS.dailyReport.defaultLocalSchedule },
      marketingDaily: { enabled: false, schedule: JOBS.marketingDaily.defaultLocalSchedule },
    },
  };
}

function localConfig() {
  const current = readJsonFile(LOCAL_CONFIG_PATH, null);
  const base = defaultLocalConfig();
  if (!current || typeof current !== 'object') return base;
  return {
    ...base,
    ...current,
    jobs: {
      autoReply: { ...base.jobs.autoReply, ...(current.jobs?.autoReply || {}) },
      dailyReport: { ...base.jobs.dailyReport, ...(current.jobs?.dailyReport || {}) },
      marketingDaily: { ...base.jobs.marketingDaily, ...(current.jobs?.marketingDaily || {}) },
    },
  };
}

function saveLocalConfig(config) {
  writeJsonFile(LOCAL_CONFIG_PATH, config);
}

function localState() {
  const state = readJsonFile(LOCAL_STATE_PATH, null);
  if (!state || typeof state !== 'object') return { version: 1, jobs: {} };
  return {
    version: state.version || 1,
    ...state,
    jobs: state.jobs && typeof state.jobs === 'object' ? state.jobs : {},
  };
}

function saveLocalState(state) {
  writeJsonFile(LOCAL_STATE_PATH, state);
}

function parseEveryMs(every) {
  const text = String(every || '').trim().toLowerCase();
  const match = text.match(/^(\d+)\s*(ms|s|m|h)$/);
  if (!match) return 0;
  const n = Number(match[1]);
  const unit = match[2];
  if (unit === 'ms') return n;
  if (unit === 's') return n * 1000;
  if (unit === 'm') return n * 60_000;
  if (unit === 'h') return n * 3_600_000;
  return 0;
}

function localNowParts(date = new Date()) {
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: TZ,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).formatToParts(date).reduce((acc, part) => {
    if (part.type !== 'literal') acc[part.type] = part.value;
    return acc;
  }, {});
  return {
    ymd: `${parts.year}-${parts.month}-${parts.day}`,
    hm: `${parts.hour}:${parts.minute}`,
  };
}

function dailyNextRunAtMs(time = '07:30', nowMs = Date.now()) {
  const [hour = '7', minute = '30'] = String(time || '07:30').split(':');
  const now = new Date(nowMs);
  const target = new Date(nowMs);
  target.setHours(Number(hour), Number(minute), 0, 0);
  if (target.getTime() <= nowMs) target.setDate(now.getDate() + 1);
  return target.getTime();
}

function localJobDue(kind, jobConfig, state, nowMs = Date.now()) {
  if (!jobConfig?.enabled) return { due: false, reason: 'disabled' };
  const schedule = jobConfig.schedule || {};
  const jobState = state.jobs?.[kind] || {};
  if (schedule.kind === 'every') {
    const everyMs = parseEveryMs(schedule.every);
    if (!everyMs) return { due: false, reason: 'bad_every' };
    const last = Number(jobState.lastRunAtMs || 0);
    const next = Number(jobState.nextRunAtMs || 0);
    if (!last && !jobState.initializedAtMs) {
      return {
        due: false,
        reason: 'initialized',
        initialize: true,
        nextRunAtMs: nowMs + everyMs,
      };
    }
    return {
      due: next ? nowMs >= next : Boolean(last && nowMs - last >= everyMs),
      reason: next ? 'interval' : (!last ? 'waiting_first_interval' : 'interval'),
      nextRunAtMs: next || (last ? last + everyMs : nowMs + everyMs),
    };
  }
  if (schedule.kind === 'daily') {
    const now = localNowParts(new Date(nowMs));
    const time = schedule.time || '07:30';
    const ranToday = jobState.lastLocalDate === now.ymd;
    const next = Number(jobState.nextRunAtMs || 0);
    if (!jobState.initializedAtMs) {
      return {
        due: false,
        reason: 'initialized',
        initialize: true,
        nextRunAtMs: dailyNextRunAtMs(time, nowMs),
      };
    }
    return {
      due: !ranToday && (next ? nowMs >= next : now.hm >= time),
      reason: ranToday ? 'already_ran_today' : 'daily_time',
      nextRunAtMs: next || dailyNextRunAtMs(time, nowMs),
    };
  }
  return { due: false, reason: 'bad_schedule' };
}

function acquireLocalLock(kind) {
  mkdirSync(LOCAL_LOCK_DIR, { recursive: true });
  const path = join(LOCAL_LOCK_DIR, `${kind}.lock`);
  try {
    const fd = openSync(path, 'wx');
    return {
      ok: true,
      path,
      release() {
        try {
          closeSync(fd);
        } catch {
          // ignore
        }
        rmSync(path, { force: true });
      },
    };
  } catch {
    return { ok: false, path, release() {} };
  }
}

function cronList() {
  const result = runOpenClaw(['cron', 'list', '--all', '--json'], { timeout: 30000 });
  const payload = parseLastJson(result.output);
  return {
    ok: result.ok && Array.isArray(payload?.jobs),
    result,
    jobs: payload?.jobs || [],
  };
}

function scheduleArgs(schedule) {
  if (schedule.kind === 'cron') {
    return ['--cron', schedule.cron, '--tz', schedule.tz || TZ, '--exact'];
  }
  return ['--every', schedule.every];
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'\\''`)}'`;
}

function taskMessage(job) {
  const command = `cd ${shellQuote(ROOT)} && ${shellQuote(NODE_BIN)} scripts/douyin-schedule-manager.js ${job.tick}`;
  return [
    'RUN_LOCAL_EXEC_ONLY',
    command,
    'Use exec only. Do not browse. Do not send Feishu yourself. Return only the final JSON printed by the command.',
  ].join('\n');
}

function normalizeJob(job) {
  return {
    id: job.id,
    name: job.name,
    enabled: Boolean(job.enabled),
    schedule: job.schedule || {},
    nextRunAtMs: job.state?.nextRunAtMs || job.nextRunAtMs || null,
    lastRunAtMs: job.state?.lastRunAtMs || null,
    lastRunStatus: job.state?.lastRunStatus || job.state?.lastStatus || null,
    consecutiveErrors: job.state?.consecutiveErrors || 0,
  };
}

function findJobsByName(jobs, name) {
  return jobs.filter((job) => job.name === name);
}

function legacyJobNames(kind) {
  if (kind === 'marketingDaily') return ['douyin-marketing-daily-19'];
  return [];
}

function allManagedJobNames() {
  return new Set([
    ...Object.values(JOBS).map((job) => job.name),
    ...legacyJobNames('marketingDaily'),
  ]);
}

function findManagedJobsByKind(jobs, kind) {
  const names = [JOBS[kind]?.name, ...legacyJobNames(kind)].filter(Boolean);
  return jobs.filter((job) => names.includes(job.name));
}

function removeDuplicateJobs(jobs, keepId, name) {
  const names = Array.isArray(name) ? name : [name];
  const removed = [];
  for (const job of jobs) {
    if (!names.includes(job.name) || job.id === keepId) continue;
    const result = runOpenClaw(['cron', 'rm', job.id, '--json'], { timeout: 30000 });
    removed.push({ id: job.id, ok: result.ok, output: result.output.slice(-500) });
  }
  return removed;
}

function upsertJob(kind, schedule) {
  const job = JOBS[kind];
  if (!job) throw new Error(`unknown job kind: ${kind}`);
  const listed = cronList();
  if (!listed.ok) {
    throw new Error(`OpenClaw cron list failed: ${listed.result.output.slice(-1000)}`);
  }
  const existing = findManagedJobsByKind(listed.jobs, kind);
  const args = [
    '--name', job.name,
    '--description', job.description,
    '--message', taskMessage(job),
    '--session', 'isolated',
    '--no-deliver',
    '--light-context',
    '--tools', 'exec',
    '--thinking', 'low',
    '--timeout-seconds', String(job.timeoutSeconds),
    ...scheduleArgs(schedule),
  ];

  let result;
  let id = existing[0]?.id || null;
  if (id) {
    result = runOpenClaw(['cron', 'edit', id, '--enable', ...args], { timeout: 30000 });
  } else {
    result = runOpenClaw(['cron', 'add', '--json', ...args], { timeout: 30000 });
    const payload = parseLastJson(result.output);
    id = payload?.job?.id || payload?.id || null;
  }
  if (!result.ok) {
    throw new Error(`OpenClaw cron ${id ? 'edit' : 'add'} failed: ${result.output.slice(-1000)}`);
  }
  const after = cronList();
  const current = findJobsByName(after.jobs, job.name)[0] || findManagedJobsByKind(after.jobs, kind)[0] || null;
  const removedDuplicates = removeDuplicateJobs(after.jobs, current?.id || id, [job.name, ...legacyJobNames(kind)]);
  return {
    ok: true,
    kind,
    id: current?.id || id,
    job: current ? normalizeJob(current) : null,
    removedDuplicates,
  };
}

function installDefault() {
  const cronJobs = INSTALL_OPENCLAW_CRON ? {
    autoReply: upsertJob('autoReply', JOBS.autoReply.defaultSchedule),
    dailyReport: null,
    marketingDaily: null,
  } : { autoReply: null, dailyReport: null, marketingDaily: null };
  const config = defaultLocalConfig();
  saveLocalConfig(config);
  return {
    ok: true,
    action: 'install_default',
    jobs: cronJobs,
    localScheduler: { ok: true, configPath: LOCAL_CONFIG_PATH, config },
    customerMessage: '定时任务已准备：自动回复每 30 分钟执行；自动化营销默认每天 07:30 执行。',
  };
}

function enableDisableAll(enable) {
  const listed = cronList();
  if (!listed.ok) throw new Error(`OpenClaw cron list failed: ${listed.result.output.slice(-1000)}`);
  const enabledNames = new Set([JOBS.autoReply.name, JOBS.marketingDaily.name]);
  const names = allManagedJobNames();
  const results = [];
  for (const job of listed.jobs.filter((item) => names.has(item.name))) {
    const shouldEnable = enable && enabledNames.has(job.name);
    const result = runOpenClaw(['cron', 'edit', job.id, shouldEnable ? '--enable' : '--disable'], { timeout: 30000 });
    results.push({ id: job.id, name: job.name, ok: result.ok, output: result.output.slice(-500) });
  }
  const config = localConfig();
  config.enabled = enable;
  config.jobs.autoReply.enabled = Boolean(enable);
  config.jobs.marketingDaily.enabled = Boolean(enable);
  config.jobs.dailyReport.enabled = false;
  saveLocalConfig(config);
  return {
    ok: results.every((item) => item.ok),
    action: enable ? 'enable' : 'disable',
    results,
    localScheduler: { ok: true, configPath: LOCAL_CONFIG_PATH, enabled: enable },
    customerMessage: enable ? '定时任务已开启。' : '定时任务已暂停。',
  };
}

function disableOpenClawCronJobs() {
  const listed = cronList();
  if (!listed.ok) throw new Error(`OpenClaw cron list failed: ${listed.result.output.slice(-1000)}`);
  const names = allManagedJobNames();
  const results = [];
  for (const job of listed.jobs.filter((item) => names.has(item.name))) {
    const result = runOpenClaw(['cron', 'edit', job.id, '--disable'], { timeout: 30000 });
    results.push({ id: job.id, name: job.name, ok: result.ok, output: result.output.slice(-500) });
  }
  return {
    ok: results.every((item) => item.ok),
    action: 'disable_openclaw_cron',
    results,
    customerMessage: 'OpenClaw cron 兼容任务已暂停，本地稳定调度继续运行。',
  };
}

function formatTime(ms) {
  if (!ms) return '-';
  return new Intl.DateTimeFormat('zh-CN', {
    timeZone: TZ,
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).format(new Date(Number(ms)));
}

function describeSchedule(schedule = {}) {
  if (schedule.kind === 'every') {
    if (schedule.every) return `每 ${schedule.every}`;
    const everyMs = Number(schedule.everyMs || 0);
    if (everyMs && everyMs % 3600000 === 0) return `每 ${everyMs / 3600000} 小时`;
    if (everyMs && everyMs % 60000 === 0) return `每 ${everyMs / 60000} 分钟`;
    return `每 ${everyMs || '-'} ms`;
  }
  if (schedule.kind === 'cron') return `${schedule.expr || schedule.cron || '-'}（${schedule.tz || TZ}）`;
  return '-';
}

function status() {
  const listed = cronList();
  const config = localConfig();
  if (!listed.ok) {
    return {
      ok: false,
      action: 'status',
      error: listed.result.output.slice(-1000),
      customerMessage: '定时任务状态读取失败，请稍后重试。',
    };
  }
  const jobs = {};
  const lines = ['定时任务：'];
  lines.push(`本地稳定调度：${config.enabled ? '已开启' : '已暂停'}`);
  const visibleKinds = ['autoReply', 'marketingDaily'];
  for (const kind of visibleKinds) {
    const meta = JOBS[kind];
    const job = findJobsByName(listed.jobs, meta.name)[0] || null;
    const local = config.jobs?.[kind] || null;
    jobs[kind] = {
      openclawCron: job ? normalizeJob(job) : null,
      local,
    };
    if (local?.schedule?.kind === 'every') {
      lines.push(`${meta.label}：${local.enabled ? '已开启' : '已暂停'}，每 ${local.schedule.every.replace('m', ' 分钟').replace('h', ' 小时')}。`);
    } else if (local?.schedule?.kind === 'daily') {
      lines.push(`${meta.label}：${local.enabled ? '已开启' : '已暂停'}，每天 ${local.schedule.time || meta.defaultLocalSchedule?.time || '07:30'}。`);
    } else if (!job) {
      lines.push(`${meta.label}：未安装`);
    } else {
      lines.push(`${meta.label}：${job.enabled ? '已开启' : '已暂停'}，${describeSchedule(job.schedule)}，下次 ${formatTime(job.state?.nextRunAtMs)}。`);
    }
  }
  lines.push('可发送：修改定时任务 自动回复 30分钟');
  lines.push('可发送：修改定时任务 自动化营销 07:30');
  return {
    ok: true,
    action: 'status',
    jobs,
    customerMessage: lines.join('\n'),
  };
}

function formatEvery(every) {
  return String(every || '').replace('m', ' 分钟').replace('h', ' 小时');
}

function parseDurationDetails(input) {
  const text = String(input || '').trim().toLowerCase();
  if (/半小时|半个小时/.test(text)) return { every: '30m', requested: '30m', clamped: false };
  const clampMinute = (value) => {
    const requested = Math.max(1, Number(value));
    const minute = Math.max(30, Math.min(1440, requested));
    return {
      every: `${minute}m`,
      requested: `${requested}m`,
      clamped: minute !== requested,
      minEvery: '30m',
    };
  };
  const minute = text.match(/(\d{1,3})\s*(分钟|分|m|min|mins|minute|minutes)/i);
  if (minute) return clampMinute(minute[1]);
  const hour = text.match(/(\d{1,2})\s*(小时|时|h|hour|hours)/i);
  if (hour) {
    const requested = Math.max(1, Number(hour[1]));
    const value = Math.max(1, Math.min(24, requested));
    return { every: `${value}h`, requested: `${requested}h`, clamped: value !== requested };
  }
  if (/^\d{1,3}$/.test(text)) return clampMinute(text);
  const compactMinute = text.match(/^(\d{1,3})m$/);
  if (compactMinute) return clampMinute(compactMinute[1]);
  const compactHour = text.match(/^(\d{1,2})h$/);
  if (compactHour) {
    const requested = Math.max(1, Number(compactHour[1]));
    const value = Math.max(1, Math.min(24, requested));
    return { every: `${value}h`, requested: `${requested}h`, clamped: value !== requested };
  }
  return null;
}

function parseDurationToEvery(input) {
  return parseDurationDetails(input)?.every || null;
}

function autoReplyScheduleMessage(details) {
  const base = `自动回复定时任务已改为每 ${formatEvery(details.every)}执行一次。`;
  if (details.clamped && details.minEvery === '30m') {
    return `${base}为避免任务重叠，最短间隔为 30 分钟。`;
  }
  return base;
}

function setAutoReply(everyText) {
  const details = parseDurationDetails(everyText);
  if (!details?.every) {
    return {
      ok: false,
      action: 'set_auto_reply',
      customerMessage: '请这样修改：修改定时任务 自动回复 30分钟',
    };
  }
  const every = details.every;
  const result = INSTALL_OPENCLAW_CRON ? upsertJob('autoReply', { kind: 'every', every }) : null;
  const config = localConfig();
  config.enabled = true;
  config.jobs.autoReply = { enabled: true, schedule: { kind: 'every', every } };
  saveLocalConfig(config);
  return {
    ok: true,
    action: 'set_auto_reply',
    result,
    every,
    requestedEvery: details.requested,
    clamped: details.clamped,
    localScheduler: { ok: true, configPath: LOCAL_CONFIG_PATH, schedule: config.jobs.autoReply.schedule },
    customerMessage: autoReplyScheduleMessage(details),
  };
}

function setAutoReplyEnabled(enable) {
  const listed = cronList();
  const results = [];
  if (listed.ok) {
    const names = new Set([JOBS.autoReply.name, ...legacyJobNames('autoReply')]);
    for (const job of listed.jobs.filter((item) => names.has(item.name))) {
      const result = runOpenClaw(['cron', 'edit', job.id, enable ? '--enable' : '--disable'], { timeout: 30000 });
      results.push({ id: job.id, name: job.name, ok: result.ok, output: result.output.slice(-500) });
    }
  }
  const config = localConfig();
  config.jobs.autoReply = {
    ...(config.jobs.autoReply || {}),
    enabled: Boolean(enable),
    schedule: config.jobs.autoReply?.schedule || JOBS.autoReply.defaultLocalSchedule,
  };
  config.enabled = Object.values(config.jobs || {}).some((job) => job?.enabled);
  saveLocalConfig(config);
  return {
    ok: results.every((item) => item.ok),
    action: enable ? 'enable_auto_reply' : 'disable_auto_reply',
    results,
    localScheduler: { ok: true, configPath: LOCAL_CONFIG_PATH, enabled: config.enabled, autoReplyEnabled: config.jobs.autoReply.enabled },
    customerMessage: enable ? '自动回复定时任务已开启。' : '自动回复定时任务已关闭。',
  };
}

function parseDailyTime(input) {
  const text = String(input || '').trim();
  const match = text.match(/([01]?\d|2[0-3])\s*(?:[:：点时])\s*([0-5]\d)?/);
  if (!match) return null;
  const hour = String(Number(match[1])).padStart(2, '0');
  const minute = String(Number(match[2] || 0)).padStart(2, '0');
  return `${hour}:${minute}`;
}

function setDailyReport(timeText) {
  return {
    ok: false,
    action: 'set_daily_report_removed',
    customerMessage: '数据报告不单独设置定时；会作为自动化营销的一部分执行。请发送：修改定时任务 自动化营销 07:30',
  };
}

function setMarketingDaily(timeText) {
  const time = parseDailyTime(timeText);
  if (!time) {
    return {
      ok: false,
      action: 'set_marketing_daily',
      customerMessage: '请这样修改：修改定时任务 自动化营销 07:30',
    };
  }
  const [hour, minute] = time.split(':').map(Number);
  const cron = `${minute} ${hour} * * *`;
  const result = INSTALL_OPENCLAW_CRON ? upsertJob('marketingDaily', { kind: 'cron', cron, tz: TZ }) : null;
  const config = localConfig();
  config.enabled = true;
  config.jobs.marketingDaily = { enabled: true, schedule: { kind: 'daily', time, tz: TZ } };
  saveLocalConfig(config);
  return {
    ok: true,
    action: 'set_marketing_daily',
    result,
    time,
    localScheduler: { ok: true, configPath: LOCAL_CONFIG_PATH, schedule: config.jobs.marketingDaily.schedule },
    customerMessage: `自动化营销定时任务已改为每天 ${time} 执行。`,
  };
}

async function notify(text, dryRun = false) {
  if (dryRun) return { ok: true, dryRun: true, text };
  return sendFeishuText(text);
}

async function notifyMany(messages, dryRun = false) {
  const list = (Array.isArray(messages) ? messages : [messages])
    .map((item) => String(item || '').trim())
    .filter(Boolean);
  const results = [];
  for (const text of list) {
    results.push(await notify(text, dryRun));
  }
  return {
    ok: results.every((item) => item?.ok),
    count: results.length,
    results,
    dryRun: Boolean(dryRun),
  };
}

function sentSummary(payload) {
  const summary = payload?.summary || {};
  return {
    commentSent: Number(summary.commentSent || 0),
    dmSent: Number(summary.dmSent || 0),
  };
}

function looksLoginExpired(text) {
  return /未登录|登录失效|二维码|扫码|need_login|qrcode|login/i.test(String(text || ''));
}

function loginRequiredMessage() {
  return '抖音需要重新登录。\n请在电脑端打开飞书，用手机抖音 App 准备扫码。\n准备好后回复：发送二维码';
}

function backgroundLoginRequiredMessage() {
  return '后台任务因抖音登录失效已暂停；下次主动发布或查询数据时会引导扫码。';
}

function looksTransientBrowserError(text) {
  return /Execution context was destroyed|Cannot find context with specified id|Target closed|Navigating frame was detached|Protocol error|net::ERR_ABORTED|timeout/i.test(String(text || ''));
}

function looksBitablePermissionBlocked(text) {
  return /Feishu HTTP 403|Forbidden|91403|bitable.*permission|多维表.*权限/i.test(String(text || ''));
}

function autoReplyTimeoutMs(opts = {}) {
  const explicit = Number(opts.timeout || process.env.DOUYIN_AUTO_REPLY_TICK_TIMEOUT_MS || 0);
  if (explicit > 0) return explicit;
  const limit = Math.max(1, Math.min(50, Number(opts.limit || process.env.DOUYIN_AUTO_REPLY_LIMIT || 50)));
  const perReplyMs = Math.max(60_000, Number(process.env.DOUYIN_COMMENT_AFTER_REPLY_WAIT_MS || 60_000) + 30_000);
  return Math.max(1_800_000, (limit * perReplyMs) + 600_000);
}

async function tickAutoReply(opts = {}) {
  const limit = Math.max(1, Math.min(50, Number(opts.limit || process.env.DOUYIN_AUTO_REPLY_LIMIT || 50)));
  const maxScan = Math.max(limit, Math.min(200, Number(opts.maxScan || process.env.DOUYIN_AUTO_REPLY_MAX_SCAN || 200)));
  const args = ['scripts/douyin-auto-reply.js', 'both', '--limit', String(limit), '--max-scan', String(maxScan)];
  if (!opts.dryRun) args.push('--execute');
  const timeout = autoReplyTimeoutMs({ ...opts, limit });
  let result = run(NODE_BIN, args, { timeout });
  let payload = parseLastJson(result.output);
  if ((!result.ok || payload?.ok === false) && looksTransientBrowserError(result.output)) {
    await new Promise((resolve) => setTimeout(resolve, 3000));
    result = run(NODE_BIN, args, { timeout });
    payload = parseLastJson(result.output);
  }
  const summary = sentSummary(payload);
  const sent = summary.commentSent + summary.dmSent;
  const ok = result.ok && payload?.ok !== false;
  let customerMessage = '';
  if (!ok) {
    customerMessage = looksLoginExpired(result.output)
      ? backgroundLoginRequiredMessage()
      : '自动回复失败，请稍后重试。';
  } else if (sent > 0 || opts.notifyEmpty) {
    customerMessage = `自动回复完成：评论 ${summary.commentSent} 条，私信 ${summary.dmSent} 条。`;
  }
  const notification = customerMessage ? await notify(customerMessage, opts.dryRun) : null;
  const output = {
    ok,
    action: 'tick_auto_reply',
    mode: opts.dryRun ? 'dry-run' : 'execute',
    summary,
    notified: Boolean(notification?.ok),
    notification,
    customerMessage,
    payload,
    rawStatus: result.status,
  };
  logEvent('auto-reply', output);
  return output;
}

function bitableUrl(syncPayload) {
  const appToken = syncPayload?.appToken;
  const tableId = syncPayload?.tables?.workTableId;
  if (!appToken || !tableId) return '';
  return `https://feishu.cn/base/${encodeURIComponent(appToken)}?table=${encodeURIComponent(tableId)}`;
}

async function tickDailyReport(opts = {}) {
  const days = Math.max(1, Math.min(30, Number(opts.days || 1)));
  const sync = run(NODE_BIN, ['scripts/sync-douyin-data-to-feishu-bitable.js', '--days', String(days)], { timeout: 600000 });
  const syncPayload = parseLastJson(sync.output);
  let report = null;
  let reportPayload = null;
  let plan = null;
  let planPayload = null;
  let customerMessage = '';
  let ok = sync.ok && syncPayload?.ok;
  if (ok) {
    report = run(NODE_BIN, ['scripts/douyin-data-report-from-bitable.js', '--days', String(days)], { timeout: 180000 });
    reportPayload = parseLastJson(report.output);
    ok = report.ok && reportPayload?.ok;
  }
  if (ok) {
    plan = run(NODE_BIN, ['scripts/douyin-next-video-plan-from-bitable.js', '--days', String(days)], { timeout: 180000 });
    planPayload = parseLastJson(plan.output);
    ok = plan.ok && planPayload?.ok;
  }
  if (ok) {
    const link = bitableUrl(syncPayload);
    customerMessage = [
      '老板，昨日数据报告如下，请您查收～',
      reportPayload.reportText || '数据报告已生成。',
      '',
      planPayload.planText || '下一条视频方案已生成。',
      link ? `多维表：${link}` : '',
    ].filter(Boolean).join('\n');
  } else if (syncPayload?.authUrl) {
    customerMessage = `数据报告生成失败：需要开通飞书多维表权限。\n请点击授权：${syncPayload.authUrl}`;
  } else if (looksBitablePermissionBlocked(sync.output) || looksBitablePermissionBlocked(report?.output) || looksBitablePermissionBlocked(plan?.output)) {
    customerMessage = '数据报告生成失败：飞书多维表暂无写入权限，请重新授权多维表权限后再试。';
  } else if (looksLoginExpired(sync.output) || looksLoginExpired(report?.output) || looksLoginExpired(plan?.output)) {
    customerMessage = opts.interactive ? loginRequiredMessage() : backgroundLoginRequiredMessage();
  } else {
    customerMessage = '数据报告生成失败，请稍后重试。';
  }
  const notification = await notify(customerMessage, opts.dryRun);
  const output = {
    ok,
    action: 'tick_daily_report',
    mode: opts.dryRun ? 'dry-run' : 'execute',
    days,
    notified: Boolean(notification?.ok),
    notification,
    customerMessage,
    sync: { status: sync.status, payload: syncPayload },
    report: report ? { status: report.status, payload: reportPayload } : null,
    plan: plan ? { status: plan.status, payload: planPayload } : null,
  };
  logEvent('daily-report', output);
  return output;
}

async function tickMarketingDaily(opts = {}) {
  const days = Math.max(1, Math.min(180, Number(opts.days || 90)));
  const args = ['scripts/marketing-controller.js', 'daily-run', '--days', String(days)];
  if (opts.dryRun) args.push('--dry-run');
  if (opts.force) args.push('--force');
  if (opts.autoConfirm) args.push('--auto-confirm');
  const result = run(NODE_BIN, args, { timeout: Number(opts.timeout || 10800000) });
  const payload = parseLastJson(result.output);
  const ok = result.ok && payload?.ok !== false;
  let customerMessage = '';
  if (!ok) {
    customerMessage = payload?.customerMessage || (looksLoginExpired(result.output) ? backgroundLoginRequiredMessage() : '今日自动化营销中断，请稍后重试。');
  } else {
    customerMessage = payload?.customerMessage || '今日自动化营销流程已启动。';
  }
  const customerMessages = Array.isArray(payload?.customerMessages)
    ? payload.customerMessages.map((item) => String(item || '').trim()).filter(Boolean)
    : (customerMessage ? [customerMessage] : []);
  const notification = customerMessages.length ? await notifyMany(customerMessages, opts.dryRun) : null;
  const output = {
    ok,
    action: 'tick_marketing_daily',
    mode: opts.dryRun ? 'dry-run' : 'execute',
    days,
    notified: Boolean(notification?.ok),
    notification,
    customerMessage,
    customerMessages,
    payload,
    rawStatus: result.status,
  };
  logEvent('marketing-daily', output);
  return output;
}

async function tickKind(kind, opts = {}) {
  if (kind === 'autoReply') return tickAutoReply(opts);
  if (kind === 'dailyReport') return tickDailyReport(opts);
  if (kind === 'marketingDaily') return tickMarketingDaily(opts);
  throw new Error(`unknown local tick kind: ${kind}`);
}

async function localSchedulerOnce(opts = {}) {
  const config = localConfig();
  const state = localState();
  const nowMs = Date.now();
  const results = [];
  if (!config.enabled) {
    return { ok: true, action: 'local_scheduler_once', enabled: false, results };
  }
  for (const kind of Object.keys(JOBS)) {
    const due = localJobDue(kind, config.jobs?.[kind], state, nowMs);
    if (!config.jobs?.[kind]?.enabled) {
      results.push({ kind, skipped: true, reason: 'disabled', nextRunAtMs: null });
      continue;
    }
    if (!due.due && !opts.force) {
      if (due.initialize) {
        const now = localNowParts(new Date(nowMs));
        state.jobs[kind] = {
          ...(state.jobs[kind] || {}),
          initializedAtMs: nowMs,
          lastLocalDate: state.jobs?.[kind]?.lastLocalDate,
          nextRunAtMs: due.nextRunAtMs || null,
          lastStatus: 'initialized',
        };
        saveLocalState(state);
      }
      results.push({ kind, skipped: true, reason: due.reason, nextRunAtMs: due.nextRunAtMs || null });
      continue;
    }
    const lock = acquireLocalLock(kind);
    if (!lock.ok) {
      results.push({ kind, skipped: true, reason: 'locked' });
      continue;
    }
    try {
      const result = await tickKind(kind, { dryRun: opts.dryRun, notifyEmpty: opts.notifyEmpty, interactive: false });
      const now = localNowParts(new Date(nowMs));
      const schedule = config.jobs?.[kind]?.schedule || {};
      const everyMs = schedule.kind === 'every' ? parseEveryMs(schedule.every) : 0;
      state.jobs[kind] = {
        ...(state.jobs[kind] || {}),
        lastRunAtMs: Date.now(),
        lastLocalDate: now.ymd,
        nextRunAtMs: schedule.kind === 'every'
          ? Date.now() + everyMs
          : dailyNextRunAtMs(schedule.time || '07:30', Date.now()),
        lastStatus: result.ok ? 'ok' : 'error',
      };
      saveLocalState(state);
      results.push({ kind, skipped: false, result });
    } catch (error) {
      const now = localNowParts(new Date(nowMs));
      const schedule = config.jobs?.[kind]?.schedule || {};
      const everyMs = schedule.kind === 'every' ? parseEveryMs(schedule.every) : 0;
      state.jobs[kind] = {
        ...(state.jobs[kind] || {}),
        lastRunAtMs: Date.now(),
        lastLocalDate: now.ymd,
        nextRunAtMs: schedule.kind === 'every'
          ? Date.now() + everyMs
          : dailyNextRunAtMs(schedule.time || '07:30', Date.now()),
        lastStatus: 'error',
        lastError: error.message,
      };
      saveLocalState(state);
      results.push({ kind, skipped: false, result: { ok: false, error: error.message } });
    } finally {
      lock.release();
    }
  }
  return {
    ok: results.every((item) => item.skipped || item.result?.ok !== false),
    action: 'local_scheduler_once',
    enabled: true,
    configPath: LOCAL_CONFIG_PATH,
    statePath: LOCAL_STATE_PATH,
    results,
  };
}

async function localSchedulerLoop(opts = {}) {
  const intervalMs = Math.max(10_000, Number(opts.intervalMs || process.env.DOUYIN_LOCAL_SCHEDULER_INTERVAL_MS || 60_000));
  console.log(JSON.stringify({
    ok: true,
    action: 'local_scheduler_started',
    intervalMs,
    configPath: LOCAL_CONFIG_PATH,
    statePath: LOCAL_STATE_PATH,
  }));
  let running = false;
  const runLoop = async () => {
    if (running) return;
    running = true;
    try {
      const result = await localSchedulerOnce(opts);
      logEvent('local-scheduler', result);
    } catch (error) {
      logEvent('local-scheduler', { ok: false, error: error.message });
    } finally {
      running = false;
    }
  };
  await runLoop();
  const timer = setInterval(runLoop, intervalMs);
  const shutdown = () => {
    clearInterval(timer);
    process.exit(0);
  };
  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);
}

function dryRunScheduleRoute(raw) {
  if (/^(开启定时任务|启动定时任务|安装定时任务|创建定时任务|恢复默认定时任务|重置定时任务|默认定时任务)$/.test(raw)) {
    return {
      ok: true,
      action: 'install_default_dry_run',
      dryRun: true,
      customerMessage: '定时任务已准备：自动回复每 30 分钟执行；自动化营销默认每天 07:30 执行。',
    };
  }
  if (/^(关闭定时任务|暂停定时任务|停用定时任务)$/.test(raw)) {
    return {
      ok: true,
      action: 'disable_dry_run',
      dryRun: true,
      customerMessage: '定时任务已暂停。',
    };
  }
  if (/修改定时任务/.test(raw) && /自动回复/.test(raw)) {
    const details = parseDurationDetails(raw);
    return details?.every ? {
      ok: true,
      action: 'set_auto_reply_dry_run',
      dryRun: true,
      every: details.every,
      requestedEvery: details.requested,
      clamped: details.clamped,
      customerMessage: autoReplyScheduleMessage(details),
    } : {
      ok: false,
      action: 'set_auto_reply_dry_run',
      dryRun: true,
      customerMessage: '请这样修改：修改定时任务 自动回复 30分钟',
    };
  }
  if (/^(关闭|暂停|停用).*(自动回复|评论回复|私信回复)$/.test(raw) || /^(自动回复|评论回复|私信回复).*(关闭|暂停|停用)$/.test(raw)) {
    return { ...setAutoReplyEnabled(false), dryRun: true };
  }
  if (/修改定时任务/.test(raw) && /数据报告|数据分析|报告/.test(raw)) return { ...setDailyReport(raw), dryRun: true };
  if (/修改定时任务/.test(raw) && /自动化营销|自动营销|每日营销/.test(raw)) {
    const time = parseDailyTime(raw);
    return time ? {
      ok: true,
      action: 'set_marketing_daily_dry_run',
      dryRun: true,
      time,
      customerMessage: `自动化营销定时任务已改为每天 ${time} 执行。`,
    } : {
      ok: false,
      action: 'set_marketing_daily_dry_run',
      dryRun: true,
      customerMessage: '请这样修改：修改定时任务 自动化营销 07:30',
    };
  }
  return null;
}

function routeText(text, opts = {}) {
  const raw = String(text || '').trim();
  if (!raw) return status();
  if (/^(定时任务|查看定时任务|任务计划|查看任务)$/.test(raw)) return status();
  if (opts.dryRun) {
    const dryRun = dryRunScheduleRoute(raw);
    if (dryRun) return dryRun;
  }
  if (/^(开启定时任务|启动定时任务|安装定时任务|创建定时任务)$/.test(raw)) return installDefault();
  if (/^(关闭定时任务|暂停定时任务|停用定时任务)$/.test(raw)) return enableDisableAll(false);
  if (/^(恢复默认定时任务|重置定时任务|默认定时任务)$/.test(raw)) return installDefault();
  if (/^(关闭|暂停|停用).*(自动回复|评论回复|私信回复)$/.test(raw) || /^(自动回复|评论回复|私信回复).*(关闭|暂停|停用)$/.test(raw)) return setAutoReplyEnabled(false);
  if (/^(开启|启动|启用).*(自动回复|评论回复|私信回复)$/.test(raw) || /^(自动回复|评论回复|私信回复).*(开启|启动|启用)$/.test(raw)) return setAutoReplyEnabled(true);

  if (/修改定时任务/.test(raw) && /自动回复/.test(raw)) {
    return setAutoReply(raw);
  }
  if (/修改定时任务/.test(raw) && /数据报告|数据分析|报告/.test(raw)) {
    return setDailyReport(raw);
  }
  if (/修改定时任务/.test(raw) && /自动化营销|自动营销|每日营销/.test(raw)) {
    return setMarketingDaily(raw);
  }
  return {
    ok: false,
    action: 'schedule_usage',
    customerMessage: [
      '定时任务支持：',
      '查看：定时任务',
      '修改自动回复：修改定时任务 自动回复 30分钟',
      '修改自动化营销：修改定时任务 自动化营销 07:30',
      '暂停：关闭定时任务',
    ].join('\n'),
  };
}

async function main() {
  const [command = '', ...rest] = process.argv.slice(2);
  const args = parseArgs(rest);
  let output;
  if (command === 'install-default' || command === 'install') output = installDefault();
  else if (command === 'status') output = status();
  else if (command === 'enable') output = enableDisableAll(true);
  else if (command === 'disable') output = enableDisableAll(false);
  else if (command === 'disable-openclaw-cron') output = disableOpenClawCronJobs();
  else if (command === 'set-auto-reply') output = setAutoReply(args.every || args._.join(' '));
  else if (command === 'disable-auto-reply') output = setAutoReplyEnabled(false);
  else if (command === 'enable-auto-reply') output = setAutoReplyEnabled(true);
  else if (command === 'set-daily-report') output = setDailyReport(args.time || args._.join(' '));
  else if (command === 'set-marketing-daily') output = setMarketingDaily(args.time || args._.join(' '));
  else if (command === 'route-text') output = routeText(args.text || args._.join(' '), args);
  else if (command === 'tick-auto-reply') output = await tickAutoReply(args);
  else if (command === 'tick-daily-report') output = await tickDailyReport({ ...args, interactive: true });
  else if (command === 'tick-marketing-daily') output = await tickMarketingDaily(args);
  else if (command === 'local-scheduler-once') output = await localSchedulerOnce(args);
  else if (command === 'local-scheduler-loop') {
    await localSchedulerLoop(args);
    return;
  }
  else {
    usage();
    process.exitCode = 2;
    return;
  }
  console.log(JSON.stringify(output, null, 2));
  if (output?.ok === false) process.exitCode = 1;
}

main().catch((err) => {
  const output = {
    ok: false,
    error: err.message,
    stack: err.stack,
  };
  console.log(JSON.stringify(output, null, 2));
  process.exit(1);
});
