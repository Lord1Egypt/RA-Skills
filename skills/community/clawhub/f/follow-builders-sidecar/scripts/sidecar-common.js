#!/usr/bin/env node

import { execFile } from 'child_process';
import { createHash } from 'crypto';
import { homedir } from 'os';
import { dirname, join } from 'path';
import { promisify } from 'util';
import { fileURLToPath } from 'url';
import {
  ensureDir,
  makeDir,
  pathExists,
  readJsonFile,
  readTextFile,
  removePath,
  statPath,
  writeJsonFile
} from './sidecar-fs.js';

const execFileAsync = promisify(execFile);

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const REPO_DIR = join(SCRIPT_DIR, '..');
const SIDECAR_HOME = join(homedir(), '.follow-builders-sidecar');
const SIDECAR_CONFIG_PATH = join(SIDECAR_HOME, 'config.json');
const SIDECAR_CREDENTIALS_PATH = join(SIDECAR_HOME, 'credentials.json');
const SIDECAR_STATE_PATH = join(SIDECAR_HOME, 'state.json');
const ORIGINAL_CONFIG_PATH = join(homedir(), '.follow-builders', 'config.json');

const DEFAULT_MODEL = 'openai-codex/gpt-5.4';
const DEFAULT_CRON_EXPR = '0 * * * *';
const DEFAULT_TIMEZONE = 'Asia/Shanghai';
const DEFAULT_LANGUAGE = 'zh';
const DEFAULT_FREQUENCY = 'daily';
const DEFAULT_WEEKLY_DAY = 'monday';
const DEFAULT_FEISHU_MODE = 'openclaw_account';
const SIDECAR_JOB_NAME = 'Follow Builders Sidecar';
const LEGACY_FEED_FILES = ['feed-x.json', 'feed-podcasts.json', 'feed-blogs.json'];
const FEED_FILE_PATTERN = /^feed-([a-z0-9-]+)\.json$/i;
const SUPPORTED_FEED_ADAPTERS = {
  x: {
    feedId: 'x',
    file: 'feed-x.json',
    outputKey: 'feedX'
  },
  podcasts: {
    feedId: 'podcasts',
    file: 'feed-podcasts.json',
    outputKey: 'feedPodcasts'
  },
  blogs: {
    feedId: 'blogs',
    file: 'feed-blogs.json',
    outputKey: 'feedBlogs'
  }
};
const PROMPT_FILES = [
  'summarize-podcast.md',
  'summarize-tweets.md',
  'summarize-blogs.md',
  'digest-intro.md',
  'translate.md'
];
const UPSTREAM_DEFAULTS = {
  owner: 'zarazhangrui',
  repo: 'follow-builders',
  branch: 'main'
};

function log(level, message, context = {}) {
  const payload = { level, message };
  if (Object.keys(context).length > 0) {
    payload.context = context;
  }
  console.error(JSON.stringify(payload));
}

function collapseWhitespace(value) {
  return String(value || '').replace(/\s+/g, ' ').trim();
}

function nowIso() {
  return new Date().toISOString();
}

function safeParseJson(raw) {
  try {
    return JSON.parse(raw);
  } catch {
    const match = raw.match(/(\{[\s\S]*\}|\[[\s\S]*\])\s*$/);
    if (!match) {
      throw new Error('Could not parse JSON output');
    }
    return JSON.parse(match[1]);
  }
}

async function runCommand(command, args, options = {}) {
  const { stdout } = await execFileAsync(command, args, {
    cwd: options.cwd || REPO_DIR,
    maxBuffer: 16 * 1024 * 1024
  });
  return stdout.trim();
}

async function runOpenClaw(args) {
  return runCommand('openclaw', args);
}

async function runOpenClawJson(args) {
  const stdout = await runOpenClaw(args);
  return safeParseJson(stdout);
}

function normalizeWeeklyDay(value) {
  const raw = collapseWhitespace(value).toLowerCase();
  const aliases = {
    mon: 'monday',
    tue: 'tuesday',
    tues: 'tuesday',
    wed: 'wednesday',
    thu: 'thursday',
    thur: 'thursday',
    thurs: 'thursday',
    fri: 'friday',
    sat: 'saturday',
    sun: 'sunday'
  };
  if (!raw) return DEFAULT_WEEKLY_DAY;
  if (aliases[raw]) return aliases[raw];
  return [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday'
  ].includes(raw) ? raw : DEFAULT_WEEKLY_DAY;
}

function normalizeFeishuDeliveryMode(value) {
  return value === 'direct_credentials' ? 'direct_credentials' : DEFAULT_FEISHU_MODE;
}

function buildDefaultConfig(overrides = {}) {
  const base = {
    version: 1,
    source: {
      ...UPSTREAM_DEFAULTS
    },
    language: DEFAULT_LANGUAGE,
    timezone: DEFAULT_TIMEZONE,
    frequency: DEFAULT_FREQUENCY,
    weeklyDay: DEFAULT_WEEKLY_DAY,
    model: DEFAULT_MODEL,
    delivery: {
      driver: 'openclaw_announce',
      openclaw: {
        channel: null,
        to: null,
        accountId: null
      },
      feishu: {
        mode: DEFAULT_FEISHU_MODE,
        accountId: null,
        chatId: null,
        domain: 'feishu'
      },
      avatarFallbackAccountId: null
    },
    importedFrom: {
      originalConfigPath: ORIGINAL_CONFIG_PATH,
      importedAt: null
    }
  };

  const merged = {
    ...base,
    ...overrides,
    source: {
      ...base.source,
      ...(overrides.source || {})
    },
    delivery: {
      ...base.delivery,
      ...(overrides.delivery || {}),
      openclaw: normalizeOpenClawDelivery(overrides.delivery?.openclaw || base.delivery.openclaw),
      feishu: {
        mode: normalizeFeishuDeliveryMode(overrides.delivery?.feishu?.mode || base.delivery.feishu.mode),
        accountId: overrides.delivery?.feishu?.accountId || base.delivery.feishu.accountId,
        chatId: overrides.delivery?.feishu?.chatId || base.delivery.feishu.chatId,
        domain: overrides.delivery?.feishu?.domain || base.delivery.feishu.domain
      }
    },
    importedFrom: {
      ...base.importedFrom,
      ...(overrides.importedFrom || {})
    }
  };

  merged.frequency = merged.frequency === 'weekly' ? 'weekly' : 'daily';
  merged.weeklyDay = normalizeWeeklyDay(merged.weeklyDay);
  merged.language = ['en', 'zh', 'bilingual'].includes(merged.language)
    ? merged.language
    : DEFAULT_LANGUAGE;
  merged.delivery.driver = merged.delivery.driver === 'feishu_card'
    ? 'feishu_card'
    : 'openclaw_announce';
  merged.delivery.openclaw = normalizeOpenClawDelivery(merged.delivery.openclaw);
  merged.delivery.feishu = {
    mode: normalizeFeishuDeliveryMode(merged.delivery.feishu?.mode),
    accountId: merged.delivery.feishu?.accountId || null,
    chatId: merged.delivery.feishu?.chatId || null,
    domain: merged.delivery.feishu?.domain || 'feishu'
  };
  return merged;
}

function buildDefaultState(overrides = {}) {
  return {
    version: 1,
    originalJobId: null,
    sidecarJobId: null,
    lastDeliveredKey: null,
    lastDeliveredCommitSha: null,
    lastSuccessAt: null,
    lastCheckedAt: null,
    lastOriginalCronFingerprint: null,
    lastObservedCommit: null,
    lastEvaluatedKey: null,
    lastEvaluatedCommitSha: null,
    lastEvaluatedOutcome: null,
    lastFeedCompatibility: null,
    lastCompatibilityWarnings: [],
    lastFeedFingerprint: null,
    ...overrides
  };
}

async function loadSidecarConfig() {
  return buildDefaultConfig(await readJsonFile(SIDECAR_CONFIG_PATH, {}));
}

async function saveSidecarConfig(config) {
  await writeJsonFile(SIDECAR_CONFIG_PATH, buildDefaultConfig(config));
}

async function loadSidecarState() {
  return buildDefaultState(await readJsonFile(SIDECAR_STATE_PATH, {}));
}

async function saveSidecarState(state) {
  await writeJsonFile(SIDECAR_STATE_PATH, buildDefaultState(state));
}

async function ensureSidecarHome() {
  await ensureDir(SIDECAR_HOME);
}

async function loadOriginalConfig() {
  return readJsonFile(ORIGINAL_CONFIG_PATH, null);
}

function buildGitHubApiHeaders() {
  return {
    'User-Agent': 'follow-builders-sidecar/1.0',
    'Accept': 'application/vnd.github+json'
  };
}

async function getOpenClawConfigValue(path, { json = false, fallback = null } = {}) {
  try {
    if (json) {
      return await runOpenClawJson(['config', 'get', path, '--json']);
    }
    const stdout = await runOpenClaw(['config', 'get', path]);
    return collapseWhitespace(stdout) || fallback;
  } catch {
    return fallback;
  }
}

async function loadOpenClawFeishuConfig() {
  const accounts = await getOpenClawConfigValue('channels.feishu.accounts', {
    json: true,
    fallback: null
  });
  const defaultAccount = await getOpenClawConfigValue('channels.feishu.defaultAccount', {
    fallback: null
  });
  const domain = await getOpenClawConfigValue('channels.feishu.domain', {
    fallback: 'feishu'
  });

  return {
    accounts: accounts && typeof accounts === 'object' ? accounts : {},
    defaultAccount,
    domain: domain || 'feishu'
  };
}

function extractLocalDateParts(value, timeZone) {
  const formatter = new Intl.DateTimeFormat('en-CA', {
    timeZone,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    weekday: 'long'
  });
  const parts = formatter.formatToParts(value instanceof Date ? value : new Date(value));
  const lookup = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return {
    year: Number(lookup.year),
    month: Number(lookup.month),
    day: Number(lookup.day),
    weekday: String(lookup.weekday || '').toLowerCase()
  };
}

function dateKeyInTimeZone(value, timeZone) {
  const parts = extractLocalDateParts(value, timeZone);
  return `${String(parts.year).padStart(4, '0')}-${String(parts.month).padStart(2, '0')}-${String(parts.day).padStart(2, '0')}`;
}

function weekdayInTimeZone(value, timeZone) {
  return extractLocalDateParts(value, timeZone).weekday;
}

function weekKeyInTimeZone(value, timeZone) {
  const parts = extractLocalDateParts(value, timeZone);
  const date = new Date(Date.UTC(parts.year, parts.month - 1, parts.day));
  const day = date.getUTCDay() || 7;
  date.setUTCDate(date.getUTCDate() + 4 - day);
  const yearStart = new Date(Date.UTC(date.getUTCFullYear(), 0, 1));
  const weekNumber = Math.ceil((((date - yearStart) / 86400000) + 1) / 7);
  return `${date.getUTCFullYear()}-W${String(weekNumber).padStart(2, '0')}`;
}

function resolveScheduleWindow(config, at = new Date()) {
  const timeZone = config.timezone || DEFAULT_TIMEZONE;
  const today = dateKeyInTimeZone(at, timeZone);
  const weekday = weekdayInTimeZone(at, timeZone);

  if (config.frequency === 'weekly') {
    const weeklyDay = normalizeWeeklyDay(config.weeklyDay);
    return {
      allowed: weekday === weeklyDay,
      frequency: 'weekly',
      weeklyDay,
      today,
      weekday,
      key: `weekly:${weekKeyInTimeZone(at, timeZone)}`
    };
  }

  return {
    allowed: true,
    frequency: 'daily',
    today,
    weekday,
    key: `daily:${today}`
  };
}

async function listCronJobs() {
  const payload = await runOpenClawJson(['cron', 'list', '--json']);
  return Array.isArray(payload?.jobs) ? payload.jobs : [];
}

function extractCronMessage(job) {
  return collapseWhitespace(job?.payload?.message || job?.payload?.systemEvent || '');
}

function isOriginalFollowBuildersJob(job) {
  const message = extractCronMessage(job);
  const name = collapseWhitespace(job?.name).toLowerCase();
  return Boolean(
    message.includes('follow-builders/scripts/run-scheduled-feishu-card-digest.js')
    || message.includes('follow-builders/scripts/prepare-digest.js')
    || name === 'ai builders digest'
  );
}

function isSidecarJob(job) {
  const message = extractCronMessage(job);
  const name = collapseWhitespace(job?.name).toLowerCase();
  return Boolean(
    message.includes('follow-builders-sidecar/scripts/run-sidecar.js')
    || message.includes('/scripts/run-sidecar.js')
    || name === SIDECAR_JOB_NAME.toLowerCase()
  );
}

function findOriginalCronJob(jobs, preferredId = null) {
  if (preferredId) {
    const exact = jobs.find((job) => job.id === preferredId);
    if (exact) return exact;
  }
  return jobs.find((job) => isOriginalFollowBuildersJob(job)) || null;
}

function findSidecarCronJob(jobs, preferredId = null) {
  if (preferredId) {
    const exact = jobs.find((job) => job.id === preferredId);
    if (exact) return exact;
  }
  return jobs.find((job) => isSidecarJob(job)) || null;
}

function buildCronFingerprint(job) {
  if (!job) return null;
  return JSON.stringify({
    id: job.id || null,
    enabled: Boolean(job.enabled),
    name: job.name || null,
    schedule: job.schedule || null,
    delivery: job.delivery || null,
    updatedAtMs: job.updatedAtMs || null
  });
}

async function disableCronJob(jobId) {
  await runOpenClaw(['cron', 'disable', jobId]);
}

async function enableCronJob(jobId) {
  await runOpenClaw(['cron', 'enable', jobId]);
}

function buildSidecarCronMessage(scriptPath) {
  return [
    'Run exactly this command and do not generate the digest yourself:',
    `\`node ${scriptPath}\``,
    '',
    'If the command returns JSON with `status` equal to `ok` or `skipped`, reply with exactly `NO_REPLY`.',
    'If the command fails, inspect the error, fix the issue if possible, rerun once, and then reply with exactly `NO_REPLY`.'
  ].join('\n');
}

function extractJobId(payload) {
  return (
    payload?.job?.id
    || payload?.id
    || payload?.data?.id
    || payload?.result?.id
    || null
  );
}

async function createSidecarCronJob({ timeZone, scriptPath = join(SCRIPT_DIR, 'run-sidecar.js') }) {
  const payload = await runOpenClawJson([
    'cron',
    'add',
    '--name',
    SIDECAR_JOB_NAME,
    '--cron',
    DEFAULT_CRON_EXPR,
    '--tz',
    timeZone || DEFAULT_TIMEZONE,
    '--session',
    'isolated',
    '--message',
    buildSidecarCronMessage(scriptPath),
    '--no-deliver',
    '--exact',
    '--timeout-seconds',
    '900',
    '--json'
  ]);

  return {
    id: extractJobId(payload),
    raw: payload
  };
}

function withDefaultFetchTimeout(init = {}, timeoutMs = 30000) {
  if (init.signal) return init;
  return {
    ...init,
    signal: AbortSignal.timeout(timeoutMs)
  };
}

async function fetchJson(url, init = {}) {
  const response = await fetch(url, withDefaultFetchTimeout(init));
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Request failed for ${url}: HTTP ${response.status} ${body.slice(0, 200)}`);
  }
  return response.json();
}

async function fetchText(url, init = {}) {
  const response = await fetch(url, withDefaultFetchTimeout(init));
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Request failed for ${url}: HTTP ${response.status} ${body.slice(0, 200)}`);
  }
  return response.text();
}

function describeFeedFile(file) {
  const normalized = collapseWhitespace(file);
  const match = normalized.match(FEED_FILE_PATTERN);
  if (!match) {
    return null;
  }

  const feedId = match[1].toLowerCase();
  const adapter = SUPPORTED_FEED_ADAPTERS[feedId] || null;

  return {
    file: normalized,
    feedId,
    supported: Boolean(adapter),
    outputKey: adapter?.outputKey || null,
    reason: adapter ? null : 'no_adapter'
  };
}

function buildFeedCompatibilityReport(feedFiles, warnings = []) {
  const all = [...new Set(feedFiles)]
    .map((file) => describeFeedFile(file))
    .filter(Boolean)
    .sort((left, right) => left.file.localeCompare(right.file));
  const supported = all.filter((entry) => entry.supported);
  const unsupported = all.filter((entry) => !entry.supported);

  return {
    all,
    supported,
    unsupported,
    supportedFiles: supported.map((entry) => entry.file),
    unsupportedFiles: unsupported.map((entry) => entry.file),
    warnings
  };
}

function summarizeFeedCompatibility(report) {
  return {
    discovered: report.all.map((entry) => ({
      feedId: entry.feedId,
      file: entry.file,
      supported: entry.supported
    })),
    supported: report.supported.map((entry) => ({
      feedId: entry.feedId,
      file: entry.file
    })),
    unsupported: report.unsupported.map((entry) => ({
      feedId: entry.feedId,
      file: entry.file,
      reason: entry.reason || 'no_adapter'
    })),
    warnings: [...(report.warnings || [])]
  };
}

async function discoverUpstreamFeedFiles(source = UPSTREAM_DEFAULTS) {
  try {
    const url = `https://api.github.com/repos/${encodeURIComponent(source.owner)}/${encodeURIComponent(source.repo)}/contents?ref=${encodeURIComponent(source.branch)}`;
    const payload = await fetchJson(url, {
      headers: buildGitHubApiHeaders()
    });
    const feedFiles = (Array.isArray(payload) ? payload : [])
      .map((entry) => entry?.name)
      .filter((name) => FEED_FILE_PATTERN.test(name));

    if (feedFiles.length > 0) {
      return buildFeedCompatibilityReport(feedFiles);
    }
  } catch (error) {
    return buildFeedCompatibilityReport(LEGACY_FEED_FILES, [
      `Dynamic upstream feed discovery failed: ${error.message}`,
      'Falling back to legacy feed list.'
    ]);
  }

  return buildFeedCompatibilityReport(LEGACY_FEED_FILES, [
    'No upstream feed files were discovered dynamically.',
    'Falling back to legacy feed list.'
  ]);
}

async function fetchLatestRelevantCommit(source = UPSTREAM_DEFAULTS, feedFiles = LEGACY_FEED_FILES) {
  const targetFiles = [...new Set(
    (Array.isArray(feedFiles) ? feedFiles : LEGACY_FEED_FILES)
      .map((entry) => (typeof entry === 'string' ? entry : entry?.file))
      .filter(Boolean)
  )];

  if (targetFiles.length === 0) {
    throw new Error('No feed files were provided for commit discovery');
  }

  const candidates = [];
  const errors = [];

  for (const file of targetFiles) {
    try {
      const url = `https://api.github.com/repos/${encodeURIComponent(source.owner)}/${encodeURIComponent(source.repo)}/commits?sha=${encodeURIComponent(source.branch)}&path=${encodeURIComponent(file)}&per_page=1`;
      const commits = await fetchJson(url, {
        headers: buildGitHubApiHeaders()
      });
      const commit = Array.isArray(commits) ? commits[0] : null;
      if (!commit?.sha || !commit?.commit?.committer?.date) {
        continue;
      }
      candidates.push({
        sha: commit.sha,
        committedAt: commit.commit.committer.date,
        subject: String(commit.commit.message || '').split('\n')[0].trim(),
        file
      });
    } catch (error) {
      errors.push(`${file}: ${error.message}`);
    }
  }

  if (candidates.length === 0) {
    throw new Error(`Could not resolve latest upstream feed commit (${errors.join(' | ') || 'no commit metadata available'})`);
  }

  candidates.sort((a, b) => new Date(b.committedAt) - new Date(a.committedAt));
  return candidates[0];
}

async function fetchCommitMetaBySha(sha, source = UPSTREAM_DEFAULTS) {
  const url = `https://api.github.com/repos/${encodeURIComponent(source.owner)}/${encodeURIComponent(source.repo)}/commits/${encodeURIComponent(sha)}`;
  const payload = await fetchJson(url, {
    headers: buildGitHubApiHeaders()
  });
  return {
    sha: payload.sha,
    committedAt: payload?.commit?.committer?.date,
    subject: String(payload?.commit?.message || '').split('\n')[0].trim()
  };
}

function buildRawFeedUrl(source, ref, file) {
  return `https://raw.githubusercontent.com/${source.owner}/${source.repo}/${ref}/${file}`;
}

async function loadFeedsForCommit(sha, source = UPSTREAM_DEFAULTS, feedCompatibility = null) {
  const compatibility = feedCompatibility || await discoverUpstreamFeedFiles(source);
  const loadedFeeds = {};

  await Promise.all(
    compatibility.supported.map(async (entry) => {
      loadedFeeds[entry.outputKey] = await fetchJson(buildRawFeedUrl(source, sha, entry.file));
    })
  );

  return {
    feedX: loadedFeeds.feedX || null,
    feedPodcasts: loadedFeeds.feedPodcasts || null,
    feedBlogs: loadedFeeds.feedBlogs || null,
    loadedFeeds,
    feedCompatibility: compatibility
  };
}

async function loadCurrentFeeds(source = UPSTREAM_DEFAULTS, feedCompatibility = null) {
  const compatibility = feedCompatibility || await discoverUpstreamFeedFiles(source);
  const loadedFeeds = {};

  await Promise.all(
    compatibility.supported.map(async (entry) => {
      loadedFeeds[entry.outputKey] = await fetchJson(buildRawFeedUrl(source, source.branch, entry.file));
    })
  );

  return {
    feedX: loadedFeeds.feedX || null,
    feedPodcasts: loadedFeeds.feedPodcasts || null,
    feedBlogs: loadedFeeds.feedBlogs || null,
    loadedFeeds,
    feedCompatibility: compatibility
  };
}

function buildFeedFingerprint(feeds) {
  return createHash('sha256').update(JSON.stringify({
    feedX: feeds.feedX || null,
    feedPodcasts: feeds.feedPodcasts || null,
    feedBlogs: feeds.feedBlogs || null
  })).digest('hex');
}

async function loadSidecarPrompts() {
  const prompts = {};
  const userPromptsDir = join(SIDECAR_HOME, 'prompts');
  const localPromptsDir = join(REPO_DIR, 'prompts');

  for (const filename of PROMPT_FILES) {
    const key = filename.replace('.md', '').replace(/-/g, '_');
    const userPath = join(userPromptsDir, filename);
    const localPath = join(localPromptsDir, filename);
    if (pathExists(userPath)) {
      prompts[key] = await readTextFile(userPath);
      continue;
    }
    if (pathExists(localPath)) {
      prompts[key] = await readTextFile(localPath);
    }
  }

  return prompts;
}

function normalizeOpenClawDelivery(value = {}) {
  return {
    channel: value.channel || null,
    to: value.to || null,
    accountId: value.accountId || value.account || null
  };
}

function inferOpenClawDeliveryFromJob(job) {
  if (!job) {
    return normalizeOpenClawDelivery();
  }
  return normalizeOpenClawDelivery({
    channel: job?.delivery?.channel,
    to: job?.delivery?.to,
    accountId: job?.delivery?.accountId || job?.accountId
  });
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function isStaleLock(lockPath, staleMs) {
  try {
    const details = await statPath(lockPath);
    return Date.now() - details.mtimeMs > staleMs;
  } catch {
    return false;
  }
}

async function readLockOwner(lockPath) {
  try {
    return await readJsonFile(join(lockPath, 'owner.json'), null);
  } catch {
    return null;
  }
}

async function isProcessAlive(pid) {
  if (!pid || typeof pid !== 'number') return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

async function acquireLock(lockPath) {
  const staleMs = 15 * 60 * 1000;

  for (let attempt = 0; attempt < 20; attempt += 1) {
    try {
      await makeDir(lockPath);
      await writeJsonFile(join(lockPath, 'owner.json'), {
        pid: process.pid,
        createdAt: nowIso()
      });
      return async () => {
        await removePath(lockPath, { recursive: true, force: true });
      };
    } catch (error) {
      if (error?.code !== 'EEXIST') {
        throw error;
      }

      const owner = await readLockOwner(lockPath);
      const ownerAlive = await isProcessAlive(owner?.pid);
      if (!ownerAlive || await isStaleLock(lockPath, staleMs)) {
        await removePath(lockPath, { recursive: true, force: true });
        continue;
      }
      await sleep(250 * (attempt + 1));
    }
  }

  throw new Error(`Could not acquire sidecar lock: ${lockPath}`);
}

async function withStateLock(callback, statePath = SIDECAR_STATE_PATH) {
  await ensureDir(dirname(statePath));
  const release = await acquireLock(`${statePath}.lock`);
  try {
    return await callback();
  } finally {
    await release();
  }
}

export {
  DEFAULT_MODEL,
  DEFAULT_TIMEZONE,
  FEED_FILE_PATTERN,
  LEGACY_FEED_FILES,
  ORIGINAL_CONFIG_PATH,
  REPO_DIR,
  SCRIPT_DIR,
  SIDECAR_CONFIG_PATH,
  SIDECAR_CREDENTIALS_PATH,
  SIDECAR_HOME,
  SIDECAR_JOB_NAME,
  SIDECAR_STATE_PATH,
  UPSTREAM_DEFAULTS,
  buildCronFingerprint,
  buildDefaultConfig,
  buildDefaultState,
  buildSidecarCronMessage,
  collapseWhitespace,
  createSidecarCronJob,
  describeFeedFile,
  dateKeyInTimeZone,
  disableCronJob,
  discoverUpstreamFeedFiles,
  enableCronJob,
  ensureSidecarHome,
  fetchCommitMetaBySha,
  fetchJson,
  fetchLatestRelevantCommit,
  fetchText,
  findOriginalCronJob,
  findSidecarCronJob,
  inferOpenClawDeliveryFromJob,
  listCronJobs,
  buildFeedFingerprint,
  loadCurrentFeeds,
  loadFeedsForCommit,
  loadOpenClawFeishuConfig,
  loadOriginalConfig,
  loadSidecarConfig,
  loadSidecarPrompts,
  loadSidecarState,
  log,
  normalizeOpenClawDelivery,
  normalizeWeeklyDay,
  normalizeFeishuDeliveryMode,
  nowIso,
  resolveScheduleWindow,
  getOpenClawConfigValue,
  runCommand,
  runOpenClaw,
  runOpenClawJson,
  saveSidecarConfig,
  saveSidecarState,
  safeParseJson,
  summarizeFeedCompatibility,
  weekdayInTimeZone,
  withStateLock
};
