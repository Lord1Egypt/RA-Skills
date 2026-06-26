#!/usr/bin/env node

import { readFile, writeFile } from 'fs/promises';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { execFile } from 'child_process';
import { promisify } from 'util';

import { buildPreparedDigest } from './prepare-digest.js';
import { sendDigestPayloadThroughOpenClaw } from './send-openclaw-message.js';
import {
  DEFAULT_MODEL,
  REPO_DIR,
  SIDECAR_CONFIG_PATH,
  SIDECAR_STATE_PATH,
  buildCronFingerprint,
  buildFeedFingerprint,
  dateKeyInTimeZone,
  disableCronJob,
  discoverUpstreamFeedFiles,
  fetchCommitMetaBySha,
  fetchLatestRelevantCommit,
  findOriginalCronJob,
  findSidecarCronJob,
  listCronJobs,
  loadCurrentFeeds,
  loadFeedsForCommit,
  loadSidecarConfig,
  loadSidecarPrompts,
  loadSidecarState,
  log,
  nowIso,
  resolveScheduleWindow,
  saveSidecarState,
  summarizeFeedCompatibility,
  withStateLock
} from './sidecar-common.js';

const execFileAsync = promisify(execFile);
const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const CARD_PIPELINE_SCRIPT = join(SCRIPT_DIR, 'run-feishu-card-digest.js');
const FEISHU_SEND_SCRIPT = join(SCRIPT_DIR, 'send-feishu-card.js');
const DEFAULT_INPUT_JSON_PATH = '/tmp/follow-builders-sidecar-raw.json';
const DEFAULT_PAYLOAD_PATH = '/tmp/follow-builders-sidecar-payload.json';

function parseArgs(argv) {
  const args = argv.slice(2);
  const parsed = {
    commitSha: null,
    force: false,
    inputJsonPath: DEFAULT_INPUT_JSON_PATH,
    model: DEFAULT_MODEL,
    payloadPath: DEFAULT_PAYLOAD_PATH,
    skipDelivery: false
  };

  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    switch (arg) {
      case '--commit':
        parsed.commitSha = args[++index];
        break;
      case '--force':
        parsed.force = true;
        break;
      case '--input-json-out':
        parsed.inputJsonPath = args[++index];
        break;
      case '--model':
        parsed.model = args[++index];
        break;
      case '--payload-out':
        parsed.payloadPath = args[++index];
        break;
      case '--skip-delivery':
        parsed.skipDelivery = true;
        break;
      default:
        throw new Error(`Unknown argument: ${arg}`);
    }
  }

  return parsed;
}

function toPreparedConfig(config) {
  return {
    language: config.language,
    frequency: config.frequency,
    weeklyDay: config.weeklyDay,
    timezone: config.timezone,
    delivery: {
      method: 'stdout'
    }
  };
}

async function runCardPipeline({ inputJsonPath, payloadPath, model }) {
  const { stdout } = await execFileAsync('node', [
    CARD_PIPELINE_SCRIPT,
    '--input-json',
    inputJsonPath,
    '--payload-out',
    payloadPath,
    '--model',
    model,
    '--skip-send'
  ], {
    cwd: REPO_DIR,
    maxBuffer: 16 * 1024 * 1024,
    timeout: 180000
  });

  return stdout.trim() ? JSON.parse(stdout.trim()) : { status: 'ok' };
}

async function sendFeishuCard(payloadPath, config) {
  const feishu = config.delivery?.feishu || {};
  const args = ['node', FEISHU_SEND_SCRIPT, '--file', payloadPath];

  if (config.delivery?.avatarFallbackAccountId) {
    args.push('--avatar-fallback-account', config.delivery.avatarFallbackAccountId);
  }

  if (!feishu.accountId || !feishu.chatId) {
    if (feishu.mode !== 'direct_credentials' || !feishu.chatId) {
      throw new Error('Feishu card delivery requires chatId and a configured credential source');
    }
  }
  args.push('--mode', feishu.mode || 'openclaw_account');
  if (feishu.accountId) {
    args.push('--account', feishu.accountId);
  }
  args.push(
    '--to',
    feishu.chatId
  );

  const { stdout } = await execFileAsync(args[0], args.slice(1), {
    cwd: REPO_DIR,
    maxBuffer: 16 * 1024 * 1024,
    timeout: 180000
  });

  return stdout.trim() ? JSON.parse(stdout.trim()) : { status: 'ok' };
}

async function gatherRuntimeContext(config, state, args) {
  const currentIso = nowIso();
  const compatibilityWarnings = [];
  const jobs = await listCronJobs();
  const originalJob = findOriginalCronJob(jobs, state.originalJobId);
  const sidecarJob = findSidecarCronJob(jobs, state.sidecarJobId);
  const takeoverActive = Boolean(
    state.sidecarJobId
    || state.originalJobId
    || config.importedFrom?.importedAt
  );

  if (takeoverActive && originalJob?.enabled) {
    log('info', 'Original follow-builders cron is enabled again, disabling it', {
      jobId: originalJob.id
    });
    await disableCronJob(originalJob.id);
  }

  const feedCompatibility = await discoverUpstreamFeedFiles(config.source);
  const feedCompatibilitySummary = summarizeFeedCompatibility(feedCompatibility);

  if (feedCompatibility.warnings?.length > 0) {
    compatibilityWarnings.push(...feedCompatibility.warnings);
  }
  if (feedCompatibility.unsupported.length > 0) {
    compatibilityWarnings.push(
      `Unsupported upstream feeds discovered: ${feedCompatibility.unsupported.map((entry) => entry.file).join(', ')}`
    );
  }

  const schedule = resolveScheduleWindow(config, new Date());

  let latestOverallCommit = null;
  let latestSupportedCommit = null;
  let latestUnsupportedCommit = null;
  let feeds = null;
  let feedFingerprint = null;
  let freshnessMode = null;
  let freshnessKey = null;
  let commitDate = null;

  try {
    latestOverallCommit = args.commitSha
      ? await fetchCommitMetaBySha(args.commitSha, config.source)
      : await fetchLatestRelevantCommit(config.source, feedCompatibility.all);
    latestSupportedCommit = args.commitSha
      ? latestOverallCommit
      : await fetchLatestRelevantCommit(config.source, feedCompatibility.supported);
    latestUnsupportedCommit = (!args.commitSha && feedCompatibility.unsupported.length > 0)
      ? await fetchLatestRelevantCommit(config.source, feedCompatibility.unsupported).catch(() => null)
      : null;
    commitDate = latestSupportedCommit?.committedAt
      ? dateKeyInTimeZone(latestSupportedCommit.committedAt, config.timezone)
      : null;
    freshnessMode = 'commit';
    freshnessKey = latestSupportedCommit?.sha || null;
    feeds = await loadFeedsForCommit(latestSupportedCommit.sha, config.source, feedCompatibility);
    feedFingerprint = buildFeedFingerprint(feeds);
  } catch (error) {
    compatibilityWarnings.push(`Commit discovery failed: ${error.message}`);
    feeds = await loadCurrentFeeds(config.source, feedCompatibility);
    feedFingerprint = buildFeedFingerprint(feeds);
    freshnessMode = 'fingerprint';
    freshnessKey = feedFingerprint;
  }

  return {
    currentIso,
    compatibilityWarnings,
    feedCompatibility,
    feedCompatibilitySummary,
    feedFingerprint,
    feeds,
    freshnessKey,
    freshnessMode,
    jobs,
    latestOverallCommit,
    latestSupportedCommit,
    latestUnsupportedCommit,
    commitDate,
    originalJob,
    schedule,
    sidecarJob
  };
}

async function commitStateUpdate(mutator) {
  return withStateLock(async () => {
    const state = await loadSidecarState();
    return mutator(state);
  });
}

async function execute(args) {
  const config = await loadSidecarConfig();
  const initialState = await loadSidecarState();

  const ctx = await gatherRuntimeContext(config, initialState, args);
  const latestUnsupportedCommitDate = ctx.latestUnsupportedCommit?.committedAt
    ? dateKeyInTimeZone(ctx.latestUnsupportedCommit.committedAt, config.timezone)
    : null;

  if (ctx.feedCompatibility.supported.length === 0) {
    await commitStateUpdate(async (state) => {
      state.lastCheckedAt = ctx.currentIso;
      state.lastFeedCompatibility = ctx.feedCompatibilitySummary;
      state.lastCompatibilityWarnings = [...ctx.compatibilityWarnings];
      state.lastEvaluatedOutcome = 'no_supported_feeds';
      await saveSidecarState(state);
    });
    return {
      status: 'skipped',
      reason: 'no_supported_feeds',
      upstreamFeeds: ctx.feedCompatibilitySummary
    };
  }

  if (!args.force && !ctx.schedule.allowed) {
    await commitStateUpdate(async (state) => {
      state.lastCheckedAt = ctx.currentIso;
      state.lastFeedCompatibility = ctx.feedCompatibilitySummary;
      state.lastCompatibilityWarnings = [...ctx.compatibilityWarnings];
      state.lastEvaluatedKey = ctx.schedule.key;
      state.lastEvaluatedOutcome = 'weekly_not_due';
      await saveSidecarState(state);
    });
    return {
      status: 'skipped',
      reason: 'weekly_not_due',
      weeklyDay: ctx.schedule.weeklyDay,
      weekday: ctx.schedule.weekday,
      date: ctx.schedule.today,
      upstreamFeeds: ctx.feedCompatibilitySummary
    };
  }

  const precheck = await commitStateUpdate(async (state) => {
    state.lastCheckedAt = ctx.currentIso;
    state.lastFeedCompatibility = ctx.feedCompatibilitySummary;
    state.lastCompatibilityWarnings = [...ctx.compatibilityWarnings];
    if (ctx.originalJob) {
      state.originalJobId = ctx.originalJob.id;
      state.lastOriginalCronFingerprint = buildCronFingerprint(ctx.originalJob);
    }
    if (ctx.sidecarJob) {
      state.sidecarJobId = ctx.sidecarJob.id;
    }

    if (!args.force && state.lastDeliveredKey === ctx.schedule.key) {
      await saveSidecarState(state);
      return {
        skipped: true,
        result: {
          status: 'skipped',
          reason: 'already_delivered',
          key: state.lastDeliveredKey,
          commitSha: state.lastDeliveredCommitSha,
          upstreamFeeds: ctx.feedCompatibilitySummary
        }
      };
    }

    if (
      !args.force
      && ctx.freshnessMode === 'commit'
      && ctx.latestUnsupportedCommit
      && latestUnsupportedCommitDate === ctx.schedule.today
      && ctx.commitDate !== ctx.schedule.today
    ) {
      state.lastEvaluatedKey = ctx.schedule.key;
      state.lastEvaluatedCommitSha = ctx.latestUnsupportedCommit.sha;
      state.lastEvaluatedOutcome = 'unsupported_feed_update_today';
      await saveSidecarState(state);
      return {
        skipped: true,
        result: {
          status: 'skipped',
          reason: 'unsupported_feed_update_today',
          today: ctx.schedule.today,
          latestUnsupportedCommit: ctx.latestUnsupportedCommit,
          upstreamFeeds: ctx.feedCompatibilitySummary,
          warnings: ctx.compatibilityWarnings
        }
      };
    }

    if (!args.force && ctx.freshnessMode === 'commit' && ctx.commitDate && ctx.commitDate !== ctx.schedule.today) {
      state.lastEvaluatedKey = ctx.schedule.key;
      state.lastEvaluatedCommitSha = ctx.latestSupportedCommit?.sha || null;
      state.lastEvaluatedOutcome = 'no_update_today';
      state.lastObservedCommit = ctx.latestSupportedCommit ? {
        sha: ctx.latestSupportedCommit.sha,
        committedAt: ctx.latestSupportedCommit.committedAt,
        subject: ctx.latestSupportedCommit.subject,
        date: ctx.commitDate
      } : null;
      await saveSidecarState(state);
      return {
        skipped: true,
        result: {
          status: 'skipped',
          reason: 'no_update_today',
          today: ctx.schedule.today,
          commitDate: ctx.commitDate,
          commit: ctx.latestSupportedCommit,
          latestOverallCommit: ctx.latestOverallCommit,
          upstreamFeeds: ctx.feedCompatibilitySummary,
          warnings: ctx.compatibilityWarnings
        }
      };
    }

    if (
      !args.force
      && ctx.freshnessMode === 'commit'
      && state.lastEvaluatedKey === ctx.schedule.key
      && state.lastEvaluatedCommitSha === ctx.latestSupportedCommit?.sha
      && state.lastEvaluatedOutcome === 'no_relevant_sources'
    ) {
      await saveSidecarState(state);
      return {
        skipped: true,
        result: {
          status: 'skipped',
          reason: 'same_commit_no_relevant_sources',
          commit: ctx.latestSupportedCommit,
          upstreamFeeds: ctx.feedCompatibilitySummary,
          warnings: ctx.compatibilityWarnings
        }
      };
    }

    if (!args.force && ctx.freshnessMode === 'fingerprint' && state.lastFeedFingerprint === ctx.feedFingerprint) {
      state.lastEvaluatedKey = ctx.schedule.key;
      state.lastEvaluatedOutcome = 'no_feed_change';
      await saveSidecarState(state);
      return {
        skipped: true,
        result: {
          status: 'skipped',
          reason: 'no_feed_change',
          upstreamFeeds: ctx.feedCompatibilitySummary,
          warnings: ctx.compatibilityWarnings
        }
      };
    }

    await saveSidecarState(state);
    return { skipped: false };
  });

  if (precheck.skipped) {
    return precheck.result;
  }

  if (
    ctx.latestUnsupportedCommit
    && ctx.latestOverallCommit?.sha === ctx.latestUnsupportedCommit.sha
    && ctx.latestOverallCommit.sha !== ctx.latestSupportedCommit?.sha
    && latestUnsupportedCommitDate === ctx.schedule.today
  ) {
    ctx.compatibilityWarnings.push(
      `Latest upstream update today was for unsupported feed ${ctx.latestUnsupportedCommit.file}; delivering the latest supported feeds only.`
    );
  }

  const { feedX, feedPodcasts, feedBlogs } = ctx.feeds;
  const prompts = await loadSidecarPrompts();
  const prepared = buildPreparedDigest({
    config: toPreparedConfig(config),
    feedX,
    feedPodcasts,
    feedBlogs,
    prompts,
    errors: []
  });
  prepared.sidecar = {
    upstreamFeeds: ctx.feedCompatibilitySummary,
    latestOverallCommit: ctx.latestOverallCommit,
    latestSupportedCommit: ctx.latestSupportedCommit,
    latestUnsupportedCommit: ctx.latestUnsupportedCommit,
    warnings: ctx.compatibilityWarnings,
    freshnessMode: ctx.freshnessMode,
    feedFingerprint: ctx.feedFingerprint
  };
  if (ctx.compatibilityWarnings.length > 0) {
    prepared.errors = [...new Set([...(prepared.errors || []), ...ctx.compatibilityWarnings])];
  }

  await writeFile(args.inputJsonPath, JSON.stringify(prepared, null, 2));
  log('info', 'Prepared upstream snapshot for sidecar run', {
    freshnessMode: ctx.freshnessMode,
    freshnessKey: ctx.freshnessKey,
    inputJsonPath: args.inputJsonPath
  });

  let pipelineResult;
  try {
    pipelineResult = await runCardPipeline({
      inputJsonPath: args.inputJsonPath,
      payloadPath: args.payloadPath,
      model: args.model || config.model || DEFAULT_MODEL
    });
  } catch (error) {
    await commitStateUpdate(async (state) => {
      state.lastCheckedAt = ctx.currentIso;
      state.lastFeedCompatibility = ctx.feedCompatibilitySummary;
      state.lastCompatibilityWarnings = [...new Set([...(ctx.compatibilityWarnings || []), `Pipeline failed: ${error.message}`])];
      state.lastEvaluatedKey = ctx.schedule.key;
      state.lastEvaluatedCommitSha = ctx.latestSupportedCommit?.sha || null;
      state.lastEvaluatedOutcome = 'pipeline_failed';
      state.lastFeedFingerprint = ctx.feedFingerprint;
      await saveSidecarState(state);
    });
    return {
      status: 'skipped',
      reason: 'pipeline_failed',
      commit: ctx.latestSupportedCommit,
      upstreamFeeds: ctx.feedCompatibilitySummary,
      warnings: [...new Set([...(ctx.compatibilityWarnings || []), `Pipeline failed: ${error.message}`])]
    };
  }

  if (pipelineResult?.status === 'skipped') {
    await commitStateUpdate(async (state) => {
      state.lastCheckedAt = ctx.currentIso;
      state.lastFeedCompatibility = ctx.feedCompatibilitySummary;
      state.lastCompatibilityWarnings = [...ctx.compatibilityWarnings];
      state.lastEvaluatedKey = ctx.schedule.key;
      state.lastEvaluatedCommitSha = ctx.latestSupportedCommit?.sha || null;
      state.lastEvaluatedOutcome = pipelineResult.reason || 'skipped';
      state.lastFeedFingerprint = ctx.feedFingerprint;
      await saveSidecarState(state);
    });
    return {
      status: 'skipped',
      reason: pipelineResult.reason || 'pipeline_skipped',
      commit: ctx.latestSupportedCommit,
      upstreamFeeds: ctx.feedCompatibilitySummary,
      warnings: ctx.compatibilityWarnings
    };
  }

  const payload = JSON.parse(await readFile(args.payloadPath, 'utf-8'));

  const finalCheck = await commitStateUpdate(async (state) => {
    state.lastCheckedAt = ctx.currentIso;
    state.lastFeedCompatibility = ctx.feedCompatibilitySummary;
    state.lastCompatibilityWarnings = [...ctx.compatibilityWarnings];

    if (!args.force && state.lastDeliveredKey === ctx.schedule.key) {
      await saveSidecarState(state);
      return {
        skipped: true,
        result: {
          status: 'skipped',
          reason: 'already_delivered',
          key: state.lastDeliveredKey,
          commitSha: state.lastDeliveredCommitSha,
          upstreamFeeds: ctx.feedCompatibilitySummary
        }
      };
    }

    await saveSidecarState(state);
    return { skipped: false };
  });

  if (finalCheck.skipped) {
    return finalCheck.result;
  }

  let deliveryResult = { status: 'dry_run' };
  if (!args.skipDelivery) {
    if (config.delivery.driver === 'feishu_card') {
      deliveryResult = await sendFeishuCard(args.payloadPath, config);
    } else {
      deliveryResult = await sendDigestPayloadThroughOpenClaw(payload, {
        ...(config.delivery?.openclaw || {})
      });
    }
  }

  await commitStateUpdate(async (state) => {
    state.lastCheckedAt = ctx.currentIso;
    state.lastFeedCompatibility = ctx.feedCompatibilitySummary;
    state.lastCompatibilityWarnings = [...ctx.compatibilityWarnings];
    state.lastEvaluatedKey = ctx.schedule.key;
    state.lastEvaluatedCommitSha = ctx.latestSupportedCommit?.sha || null;
    state.lastEvaluatedOutcome = args.skipDelivery ? 'dry_run' : 'success';
    state.lastFeedFingerprint = ctx.feedFingerprint;
    if (ctx.latestSupportedCommit?.committedAt) {
      state.lastObservedCommit = {
        sha: ctx.latestSupportedCommit.sha,
        committedAt: ctx.latestSupportedCommit.committedAt,
        subject: ctx.latestSupportedCommit.subject,
        date: dateKeyInTimeZone(ctx.latestSupportedCommit.committedAt, config.timezone)
      };
    }
    if (!args.skipDelivery) {
      state.lastDeliveredKey = ctx.schedule.key;
      state.lastDeliveredCommitSha = ctx.latestSupportedCommit?.sha || ctx.feedFingerprint;
      state.lastSuccessAt = ctx.currentIso;
    }
    await saveSidecarState(state);
  });

  return {
    status: 'ok',
    configPath: SIDECAR_CONFIG_PATH,
    statePath: SIDECAR_STATE_PATH,
    commit: ctx.latestSupportedCommit,
    latestOverallCommit: ctx.latestOverallCommit,
    latestUnsupportedCommit: ctx.latestUnsupportedCommit,
    delivered: !args.skipDelivery,
    delivery: deliveryResult,
    upstreamFeeds: ctx.feedCompatibilitySummary,
    warnings: ctx.compatibilityWarnings,
    freshnessMode: ctx.freshnessMode,
    feedFingerprint: ctx.feedFingerprint
  };
}

async function main() {
  const args = parseArgs(process.argv);
  const result = await execute(args);
  process.stdout.write(`${JSON.stringify(result)}\n`);
}

const IS_ENTRYPOINT = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];

if (IS_ENTRYPOINT) {
  main().catch(async (error) => {
    log('error', 'Sidecar runtime failed', {
      error: error.message,
      stack: error.stack
    });

    try {
      const state = await loadSidecarState();
      state.lastCheckedAt = nowIso();
      state.lastEvaluatedOutcome = 'error';
      await saveSidecarState(state);
    } catch {
      // best effort only
    }

    process.exit(1);
  });
}
