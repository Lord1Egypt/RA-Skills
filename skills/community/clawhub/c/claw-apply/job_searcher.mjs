#!/usr/bin/env node
/**
 * job_searcher.mjs — claw-apply Job Searcher
 * Searches LinkedIn + Wellfound and populates the jobs queue
 * Run via cron or manually: node job_searcher.mjs
 */
import { loadEnv } from './lib/env.mjs';
loadEnv(); // load .env before anything else

import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';
import { createWriteStream } from 'fs';

const __dir = dirname(fileURLToPath(import.meta.url));

// Tee all output to a log file so it's always available regardless of how the process is launched
const logStream = createWriteStream(resolve(__dir, 'data/searcher.log'), { flags: 'w' });
const origStdoutWrite = process.stdout.write.bind(process.stdout);
const origStderrWrite = process.stderr.write.bind(process.stderr);
process.stdout.write = (chunk, ...args) => { logStream.write(chunk); return origStdoutWrite(chunk, ...args); };
process.stderr.write = (chunk, ...args) => { logStream.write(chunk); return origStderrWrite(chunk, ...args); };

import { addJobs, loadQueue, loadConfig } from './lib/queue.mjs';
import { writeFileSync, readFileSync, existsSync } from 'fs';
import { acquireLock } from './lib/lock.mjs';
import { createBrowser } from './lib/browser.mjs';
import { verifyLogin as liLogin, searchLinkedIn } from './lib/linkedin.mjs';
import { verifyLogin as wfLogin, searchWellfound } from './lib/wellfound.mjs';
import { sendTelegram, formatSearchSummary } from './lib/notify.mjs';
import { DEFAULT_FIRST_RUN_DAYS } from './lib/constants.mjs';
import { generateKeywords } from './lib/keywords.mjs';
import { initProgress, isCompleted, markComplete, getKeywordStart, markKeywordComplete, saveKeywords, getSavedKeywords, clearProgress } from './lib/search_progress.mjs';
import { ensureLoggedIn } from './lib/session.mjs';

async function main() {
  const lock = acquireLock('searcher', resolve(__dir, 'data'));

  // Cooldown guard — never run more than once per 6 hours unless --force is passed
  const MIN_HOURS_BETWEEN_RUNS = 6;
  if (!process.argv.includes('--force')) {
    const lastRunPath = resolve(__dir, 'data/searcher_last_run.json');
    if (existsSync(lastRunPath)) {
      const lastRun = JSON.parse(readFileSync(lastRunPath, 'utf8'));
      const lastRanAt = lastRun.finished_at || lastRun.started_at;
      if (lastRanAt) {
        const hoursSince = (Date.now() - new Date(lastRanAt).getTime()) / (1000 * 60 * 60);
        if (hoursSince < MIN_HOURS_BETWEEN_RUNS) {
          console.log(`⏳ Searcher ran ${hoursSince.toFixed(1)}h ago — cooldown (${MIN_HOURS_BETWEEN_RUNS}h min). Use --force to override.`);
          process.exit(0);
        }
      }
    }
  }

  console.log(`🔍 claw-apply: Job Searcher starting at ${new Date().toISOString()}\n`);

  let totalAdded = 0, totalSeen = 0;
  const platformsRun = [];
  const trackCounts = {}; // { trackName: { found, added } }
  const startedAt = Date.now();

  const settings = loadConfig(resolve(__dir, 'config/settings.json'));

  const writeLastRun = (finished = false) => {
    const entry = {
      started_at: startedAt,
      finished_at: finished ? Date.now() : null,
      finished,
      added: totalAdded,
      seen: totalSeen,
      skipped_dupes: totalSeen - totalAdded,
      platforms: platformsRun,
    };
    // Always update last-run snapshot
    writeFileSync(resolve(__dir, 'data/searcher_last_run.json'), JSON.stringify(entry, null, 2));
    // Append to run history log
    const runsPath = resolve(__dir, 'data/search_runs.json');
    const runs = existsSync(runsPath) ? JSON.parse(readFileSync(runsPath, 'utf8')) : [];
    // Update last entry if same run, otherwise append
    if (runs.length > 0 && runs[runs.length - 1].started_at === startedAt) {
      runs[runs.length - 1] = entry;
    } else {
      runs.push(entry);
    }
    writeFileSync(runsPath, JSON.stringify(runs, null, 2));
  };

  lock.onShutdown(async () => {
    console.log('  Writing partial results to last-run file...');
    writeLastRun(false);
    if (totalAdded > 0) {
      const summary = formatSearchSummary(totalAdded, totalSeen - totalAdded, platformsRun.length ? platformsRun : ['LinkedIn'], trackCounts);
      await sendTelegram(settings, summary + '\n_(partial run — interrupted)_').catch(() => {});
    }
  });

  // Load config
  const searchConfig = loadConfig(resolve(__dir, 'config/search_config.json'));

  // First run detection: if queue is empty, use first_run_days lookback
  const profile = loadConfig(resolve(__dir, 'config/profile.json'));
  const anthropicKey = process.env.ANTHROPIC_API_KEY || settings.anthropic_api_key;

  // Determine lookback: check for an in-progress run first, then fall back to first-run/normal logic
  const savedProgress = existsSync(resolve(__dir, 'data/search_progress.json'))
    ? JSON.parse(readFileSync(resolve(__dir, 'data/search_progress.json'), 'utf8'))
    : null;
  const isFirstRun = loadQueue().length === 0;

  // Dynamic lookback: time since last run × 1.25 buffer (min 4h, max first_run_days)
  function dynamicLookbackDays() {
    const lastRunPath = resolve(__dir, 'data/searcher_last_run.json');
    if (!existsSync(lastRunPath)) return searchConfig.posted_within_days || 2;
    const lastRun = JSON.parse(readFileSync(lastRunPath, 'utf8'));
    const lastRanAt = lastRun.started_at || lastRun.finished_at;
    if (!lastRanAt) return searchConfig.posted_within_days || 2;
    const hoursSince = (Date.now() - new Date(lastRanAt).getTime()) / (1000 * 60 * 60);
    const buffered = hoursSince * 1.25;
    const minHours = 4;
    const maxDays = searchConfig.first_run_days || DEFAULT_FIRST_RUN_DAYS;
    return Math.min(Math.max(buffered / 24, minHours / 24), maxDays);
  }

  const lookbackDays = savedProgress?.lookback_days
    || (isFirstRun ? (searchConfig.first_run_days || DEFAULT_FIRST_RUN_DAYS) : dynamicLookbackDays());

  if (savedProgress?.lookback_days) {
    console.log(`🔁 Resuming ${lookbackDays.toFixed(2)}-day search run\n`);
  } else if (isFirstRun) {
    console.log(`📅 First run — looking back ${lookbackDays} days\n`);
  } else {
    const hours = (lookbackDays * 24).toFixed(1);
    console.log(`⏱️  Dynamic lookback: ${hours}h (time since last run × 1.25)\n`);
  }

  // Init progress tracking — enables resume on restart
  initProgress(resolve(__dir, 'data'), lookbackDays);

  // Enhance keywords with AI — reuse saved keywords from progress if resuming, never regenerate mid-run
  for (const search of searchConfig.searches) {
    const saved = getSavedKeywords('linkedin', search.name) ?? getSavedKeywords('wellfound', search.name);
    if (saved) {
      console.log(`  [${search.name}] reusing ${saved.length} saved keywords`);
      search.keywords = saved;
    } else if (anthropicKey) {
      try {
        const aiKeywords = await generateKeywords(search, profile, anthropicKey);
        const merged = [...new Set([...search.keywords, ...aiKeywords])];
        console.log(`🤖 [${search.name}] ${search.keywords.length} → ${merged.length} keywords (AI-enhanced)`);
        search.keywords = merged;
      } catch (e) {
        console.warn(`  [${search.name}] AI keywords failed, using static: ${e.message}`);
      }
    }
    saveKeywords('linkedin', search.name, search.keywords);
    saveKeywords('wellfound', search.name, search.keywords);
  }
  console.log('');

  // Group searches by platform
  const liSearches = searchConfig.searches.filter(s => s.platforms?.includes('linkedin'));
  const wfSearches = searchConfig.searches.filter(s => s.platforms?.includes('wellfound'));

  // --- LinkedIn ---
  if (liSearches.length > 0) {
    console.log('🔗 LinkedIn search...');
    let liBrowser;
    try {
      console.log('  Creating browser...');
      liBrowser = await createBrowser(settings, 'linkedin');
      console.log('  Browser connected, verifying login...');
      const loggedIn = await ensureLoggedIn(liBrowser.page, liLogin, 'linkedin', settings.kernel_api_key || process.env.KERNEL_API_KEY, settings.kernel?.connection_ids || {});
      if (!loggedIn) throw new Error('LinkedIn not logged in');
      console.log('  ✅ Logged in');

      for (const search of liSearches) {
        if (isCompleted('linkedin', search.name)) {
          console.log(`  [${search.name}] ✓ already done, skipping`);
          continue;
        }
        const keywordStart = getKeywordStart('linkedin', search.name);
        if (keywordStart > 0) console.log(`  [${search.name}] resuming from keyword ${keywordStart + 1}/${search.keywords.length}`);
        const effectiveSearch = { ...search, keywords: search.keywords.slice(keywordStart), keywordOffset: keywordStart, filters: { ...search.filters, posted_within_days: lookbackDays } };
        let queryFound = 0, queryAdded = 0;
        await searchLinkedIn(liBrowser.page, effectiveSearch, {
          onPage: (pageJobs) => {
            const added = addJobs(pageJobs);
            totalAdded += added;
            totalSeen += pageJobs.length;
            queryFound += pageJobs.length;
            queryAdded += added;
            process.stdout.write(`\r  [${search.name}] ${queryFound} found, ${queryAdded} new...`);
          },
          onKeyword: (ki) => {
            markKeywordComplete('linkedin', search.name, keywordStart + ki);
          }
        });
        console.log(`\r  [${search.name}] ${queryFound} found, ${queryAdded} new`);
        markComplete('linkedin', search.name, { found: queryFound, added: queryAdded });
        const tc = trackCounts[search.name] || (trackCounts[search.name] = { found: 0, added: 0 });
        tc.found += queryFound; tc.added += queryAdded;
      }

      platformsRun.push('LinkedIn');
    } catch (e) {
      console.error(`  ❌ LinkedIn error: ${e.message}`);
      if (e.stack) console.error(`  Stack: ${e.stack.split('\n').slice(1, 3).join(' | ').trim()}`);
    } finally {
      await liBrowser?.browser?.close().catch(() => {});
    }
  }

  // --- Wellfound ---
  if (wfSearches.length > 0) {
    console.log('\n🌐 Wellfound search...');
    let wfBrowser;
    try {
      console.log('  Creating browser...');
      wfBrowser = await createBrowser(settings, 'wellfound');
      console.log('  Browser connected, verifying login...');
      const loggedIn = await ensureLoggedIn(wfBrowser.page, wfLogin, 'wellfound', settings.kernel_api_key || process.env.KERNEL_API_KEY, settings.kernel?.connection_ids || {});
      if (!loggedIn) console.warn('  ⚠️ Wellfound login unconfirmed, proceeding');
      else console.log('  ✅ Logged in');

      for (const search of wfSearches) {
        if (isCompleted('wellfound', search.name)) {
          console.log(`  [${search.name}] ✓ already done, skipping`);
          continue;
        }
        const effectiveSearch = { ...search, filters: { ...search.filters, posted_within_days: lookbackDays } };
        let queryFound = 0, queryAdded = 0;
        await searchWellfound(wfBrowser.page, effectiveSearch, {
          onPage: (pageJobs) => {
            const added = addJobs(pageJobs);
            totalAdded += added;
            totalSeen += pageJobs.length;
            queryFound += pageJobs.length;
            queryAdded += added;
            process.stdout.write(`\r  [${search.name}] ${queryFound} found, ${queryAdded} new...`);
          }
        });
        console.log(`\r  [${search.name}] ${queryFound} found, ${queryAdded} new`);
        markComplete('wellfound', search.name, { found: queryFound, added: queryAdded });
        const tc = trackCounts[search.name] || (trackCounts[search.name] = { found: 0, added: 0 });
        tc.found += queryFound; tc.added += queryAdded;
      }

      platformsRun.push('Wellfound');
    } catch (e) {
      console.error(`  ❌ Wellfound error: ${e.message}`);
      if (e.stack) console.error(`  Stack: ${e.stack.split('\n').slice(1, 3).join(' | ').trim()}`);
    } finally {
      await wfBrowser?.browser?.close().catch(() => {});
    }
  }

  // Summary
  const summary = formatSearchSummary(totalAdded, totalSeen - totalAdded, platformsRun, trackCounts);
  console.log(`\n${summary.replace(/\*/g, '')}`);
  if (totalAdded > 0) await sendTelegram(settings, summary).catch(() => {});

  writeLastRun(true);
  // Archive final progress snapshot before clearing (for audit — answers "what was searched?")
  const progressPath = resolve(__dir, 'data/search_progress.json');
  if (existsSync(progressPath)) {
    writeFileSync(resolve(__dir, 'data/search_progress_last.json'), readFileSync(progressPath, 'utf8'));
  }
  clearProgress(); // run finished cleanly — next run starts fresh with new keywords

  console.log(`\n✅ Search complete at ${new Date().toISOString()}`);
  return { added: totalAdded, seen: totalSeen };
}

main().then(() => {
  process.exit(0);
}).catch(e => {
  console.error('Fatal:', e.message);
  if (e.stack) console.error(e.stack);
  process.exit(1);
});
