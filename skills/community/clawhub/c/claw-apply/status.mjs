#!/usr/bin/env node
/**
 * status.mjs — claw-apply status report
 * Outputs structured JSON for agent formatting
 * Run: node status.mjs [--json]
 */
import { readFileSync, existsSync } from 'fs';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dir = dirname(fileURLToPath(import.meta.url));
const jsonMode = process.argv.includes('--json');

function readJson(path) {
  try { return JSON.parse(readFileSync(path, 'utf8')); } catch { return null; }
}

function isRunning(name) {
  const lockPath = resolve(__dir, `data/${name}.lock`);
  if (!existsSync(lockPath)) return false;
  const pid = parseInt(readFileSync(lockPath, 'utf8').trim(), 10);
  try { process.kill(pid, 0); return true; } catch { return false; }
}

function readLastRun(name) {
  const path = resolve(__dir, `data/${name}_last_run.json`);
  return readJson(path);
}

function buildSearchProgress() {
  const sp = readJson(resolve(__dir, 'data/search_progress.json'));
  if (!sp) return null;

  // Build unique track list from completed + keyword_progress, prefer platform-specific key
  const seen = new Set();
  const tracks = [];

  const allKeys = [
    ...(sp.completed || []),
    ...Object.keys(sp.keyword_progress || {}),
    ...Object.keys(sp.keywords || {}),
  ];

  for (const key of allKeys) {
    const [platform, ...trackParts] = key.split(':');
    const trackName = trackParts.join(':');
    if (seen.has(trackName)) continue;
    seen.add(trackName);

    const keywords = sp.keywords?.[key] || [];
    const lastDone = sp.keyword_progress?.[key] ?? -1;
    const complete = (sp.completed || []).includes(key);

    tracks.push({
      platform, track: trackName,
      total: keywords.length,
      done: complete ? keywords.length : Math.max(0, lastDone + 1),
      complete,
    });
  }
  return tracks;
}

function buildStatus() {
  const queue = readJson(resolve(__dir, 'data/jobs_queue.json')) || [];
  const log   = readJson(resolve(__dir, 'data/applications_log.json')) || [];

  // Queue breakdown
  const byStatus = {};
  const byPlatform = {};
  const atsCounts = {};

  const byApplyType = {};
  for (const job of queue) {
    byStatus[job.status] = (byStatus[job.status] || 0) + 1;
    byPlatform[job.platform] = (byPlatform[job.platform] || 0) + 1;
    if (job.status === 'new' && job.apply_type) {
      byApplyType[job.apply_type] = (byApplyType[job.apply_type] || 0) + 1;
    }
    if (job.status === 'skipped_external_unsupported' && job.ats_platform) {
      atsCounts[job.ats_platform] = (atsCounts[job.ats_platform] || 0) + 1;
    }
  }

  // Last applied
  const applied = [...queue, ...log].filter(j => j.status === 'applied')
    .sort((a, b) => (b.applied_at || 0) - (a.applied_at || 0));
  const lastApplied = applied[0] || null;

  const searcherLastRun = readLastRun('searcher');
  const applierLastRun  = readLastRun('applier');
  const searchProgress  = buildSearchProgress();

  // Filter state
  const filterState     = readJson(resolve(__dir, 'data/filter_state.json'));
  const filterRuns      = readJson(resolve(__dir, 'data/filter_runs.json')) || [];
  const lastFilterRun   = filterRuns.length > 0 ? filterRuns[filterRuns.length - 1] : null;
  const unscored        = queue.filter(j => j.status === 'new' && j.filter_score == null).length;

  return {
    searcher: {
      running: isRunning('searcher'),
      last_run: searcherLastRun,
      keyword_progress: searchProgress,
    },
    filter: {
      batch_pending: !!filterState,
      batch_id: filterState?.batch_id || null,
      submitted_at: filterState?.submitted_at || null,
      batch_job_count: filterState?.job_count || null,
      model: filterState?.model || lastFilterRun?.model || null,
      last_run: lastFilterRun,
      unscored,
    },
    applier: {
      running: isRunning('applier'),
      last_run: applierLastRun,
    },
    queue: {
      total: queue.length,
      duplicate: byStatus['duplicate'] || 0,
      new: byStatus['new'] || 0,
      filtered: byStatus['filtered'] || 0,
      applied: byStatus['applied'] || 0,
      closed: byStatus['closed'] || 0,
      failed: byStatus['failed'] || 0,
      needs_answer: byStatus['needs_answer'] || 0,
      skipped_external: byStatus['skipped_external_unsupported'] || 0,
      skipped_recruiter: byStatus['skipped_recruiter_only'] || 0,
      skipped_no_apply: (byStatus['skipped_easy_apply_unsupported'] || 0) + (byStatus['skipped_no_apply'] || 0),
      skipped_other: (byStatus['skipped_honeypot'] || 0) + (byStatus['stuck'] || 0) + (byStatus['incomplete'] || 0),
      already_applied: byStatus['already_applied'] || 0,
      by_platform: byPlatform,
    },
    ats_breakdown: atsCounts,
    apply_type_breakdown: byApplyType,
    last_applied: lastApplied ? {
      title: lastApplied.title,
      company: lastApplied.company,
      platform: lastApplied.platform,
      at: lastApplied.applied_at,
    } : null,
    log_total: log.length,
  };
}

function timeAgo(ms) {
  if (!ms) return 'never';
  const diff = Date.now() - ms;
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return 'just now';
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}

function formatReport(s) {
  const q = s.queue;

  // Searcher section
  const sr = s.searcher;
  const searcherLine = sr.running
    ? `🔄 Running now — ${q.total} jobs found so far`
    : sr.last_run?.finished === false
      ? `⚠️  Last run interrupted ${timeAgo(sr.last_run?.started_at)} (partial results saved)`
      : `⏸️  Last ran ${timeAgo(sr.last_run?.finished_at)}`;
  const lastRunDetail = sr.last_run && !sr.running
    ? `→ Found ${sr.last_run.added} new jobs (${sr.last_run.seen} seen, ${sr.last_run.skipped_dupes || 0} dupes)`
    : null;

  // Applier section
  const ar = s.applier;
  const applierLine = ar.running
    ? `🔄 Running now`
    : `⏸️  Last ran ${timeAgo(ar.last_run?.finished_at)}`;
  const lastApplierDetail = ar.last_run && !ar.running
    ? `→ Applied ${ar.last_run.submitted} jobs in that run`
    : null;

  const lines = [
    `📊 *claw-apply Status*`,
    ``,
    `🔍 *Searcher:* ${searcherLine}`,
  ];
  if (lastRunDetail) lines.push(lastRunDetail);

  // Keyword progress grouped by platform
  const kp = s.searcher.keyword_progress;
  if (kp && kp.length > 0) {
    const byPlatform = {};
    for (const t of kp) {
      if (!byPlatform[t.platform]) byPlatform[t.platform] = [];
      byPlatform[t.platform].push(t);
    }
    for (const [platform, tracks] of Object.entries(byPlatform)) {
      lines.push(`${platform.charAt(0).toUpperCase() + platform.slice(1)}:`);
      for (const t of tracks) {
        const pct = t.total > 0 ? Math.round((t.done / t.total) * 100) : 0;
        const bar = t.complete ? '✅ done' : `${t.done}/${t.total} keywords (${pct}%)`;
        lines.push(`• ${t.track}: ${bar}`);
      }
    }
  }

  // Filter section
  const fr = s.filter;
  let filterLine;
  if (fr.batch_pending) {
    filterLine = `⏳ Batch in flight — ${fr.batch_job_count} jobs, submitted ${timeAgo(new Date(fr.submitted_at).getTime())}`;
  } else if (fr.last_run) {
    const lr = fr.last_run;
    filterLine = `⏸️  Last ran ${timeAgo(new Date(lr.collected_at).getTime())} — ✅ ${lr.passed} passed, 🚫 ${lr.filtered} filtered`;
  } else {
    filterLine = fr.unscored > 0 ? `🟡 ${fr.unscored} jobs awaiting filter` : `⏸️  Never run`;
  }
  if (fr.model) filterLine += ` (${fr.model.replace('claude-', '').replace(/-\d{8}$/, '')})`;
  if (fr.unscored > 0 && !fr.batch_pending) filterLine += ` · ${fr.unscored} unscored`;

  lines.push(`🔬 *Filter:* ${filterLine}`);
  lines.push(`🚀 *Applier:* ${applierLine}`);
  if (lastApplierDetail) lines.push(lastApplierDetail);

  // Queue summary — only show non-zero counts
  const unique = q.total - (q.duplicate || 0);
  lines.push('', `📋 *Queue* — ${unique} unique jobs (${q.duplicate || 0} dupes)`);

  const queueLines = [
    [q.new, 'Ready to apply'],
    [q.applied, 'Applied'],
    [q.filtered || 0, 'AI filtered'],
    [q.closed || 0, 'Closed'],
    [q.needs_answer, 'Needs answer'],
    [q.skipped_other || 0, 'Incomplete/stuck'],
    [q.skipped_no_apply, 'No apply button'],
    [q.skipped_recruiter, 'Recruiter-only'],
    [q.skipped_external, 'External ATS'],
  ];
  for (const [count, label] of queueLines) {
    if (count > 0) lines.push(`• ${label}: ${count}`);
  }

  // Ready-to-apply breakdown by type
  if (s.apply_type_breakdown && Object.keys(s.apply_type_breakdown).length > 0) {
    const sorted = Object.entries(s.apply_type_breakdown).sort((a, b) => b[1] - a[1]);
    const parts = sorted.map(([type, count]) => `${type} ${count}`);
    lines.push(`• Breakdown: ${parts.join(', ')}`);
  }

  // Last applied
  if (s.last_applied) {
    const la = s.last_applied;
    lines.push('', `Last applied: ${la.title} @ ${la.company} — ${la.at ? timeAgo(la.at) : 'unknown'}`);
  }

  return lines.join('\n');
}

import { loadConfig } from './lib/queue.mjs';
import { sendTelegram } from './lib/notify.mjs';

const telegramMode = process.argv.includes('--telegram');
const status = buildStatus();

if (jsonMode) {
  console.log(JSON.stringify(status, null, 2));
} else if (telegramMode) {
  const report = formatReport(status);
  const settings = loadConfig(resolve(__dir, 'config/settings.json'));
  await sendTelegram(settings, report);
  console.log('Status sent to Telegram');
} else {
  // Console output keeps markdown * for agents that relay stdout to Telegram
  console.log(formatReport(status));
}
