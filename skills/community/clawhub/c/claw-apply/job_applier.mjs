#!/usr/bin/env node
import { loadEnv } from './lib/env.mjs';
loadEnv(); // load .env before anything else
/**
 * job_applier.mjs — claw-apply Job Applier
 * Reads jobs queue and applies using the appropriate handler per apply_type
 * Run via cron or manually: node job_applier.mjs [--preview]
 */
import { existsSync, writeFileSync, createWriteStream } from 'fs';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dir = dirname(fileURLToPath(import.meta.url));

// Tee all output to a log file so it's always available regardless of how the process is launched
const logStream = createWriteStream(resolve(__dir, 'data/applier.log'), { flags: 'w' });
const origStdoutWrite = process.stdout.write.bind(process.stdout);
const origStderrWrite = process.stderr.write.bind(process.stderr);
process.stdout.write = (chunk, ...args) => { logStream.write(chunk); return origStdoutWrite(chunk, ...args); };
process.stderr.write = (chunk, ...args) => { logStream.write(chunk); return origStderrWrite(chunk, ...args); };

import { getJobsByStatus, updateJobStatus, appendLog, loadConfig, isAlreadyApplied } from './lib/queue.mjs';
import { acquireLock } from './lib/lock.mjs';
import { createBrowser } from './lib/browser.mjs';
import { ensureAuth } from './lib/session.mjs';
import { FormFiller } from './lib/form_filler.mjs';
import { applyToJob, supportedTypes } from './lib/apply/index.mjs';
import { sendTelegram, formatApplySummary } from './lib/notify.mjs';
import { processTelegramReplies } from './lib/telegram_answers.mjs';
import { generateAnswer } from './lib/ai_answer.mjs';
import {
  APPLY_BETWEEN_DELAY_BASE, APPLY_BETWEEN_DELAY_JITTER, DEFAULT_MAX_RETRIES,
  APPLY_RUN_TIMEOUT_MS, PER_JOB_TIMEOUT_MS
} from './lib/constants.mjs';

const DEFAULT_ENABLED_APPLY_TYPES = ['easy_apply', 'wellfound'];

const isPreview = process.argv.includes('--preview');

async function main() {
  const lock = acquireLock('applier', resolve(__dir, 'data'));

  const settings = loadConfig(resolve(__dir, 'config/settings.json'));
  const profile = loadConfig(resolve(__dir, 'config/profile.json'));
  const answersPath = resolve(__dir, 'config/answers.json');
  const answers = existsSync(answersPath) ? loadConfig(answersPath) : [];
  const maxApps = settings.max_applications_per_run || Infinity;
  const maxRetries = settings.max_retries ?? DEFAULT_MAX_RETRIES;
  const enabledTypes = settings.enabled_apply_types || DEFAULT_ENABLED_APPLY_TYPES;
  const apiKey = process.env.ANTHROPIC_API_KEY || settings.anthropic_api_key;
  const formFiller = new FormFiller(profile, answers, { apiKey, answersPath });

  const startedAt = Date.now();
  const results = {
    submitted: 0, failed: 0, needs_answer: 0, total: 0,
    skipped_recruiter: 0, skipped_external: 0, skipped_no_apply: 0, skipped_other: 0,
    already_applied: 0, closed: 0, atsCounts: {},
    jobDetails: [], // { title, company, url, status } per job for summary
  };

  lock.onShutdown(() => {
    writeFileSync(resolve(__dir, 'data/applier_last_run.json'), JSON.stringify({
      started_at: startedAt, finished_at: null, finished: false, ...results
    }, null, 2));
  });

  console.log('🚀 claw-apply: Job Applier starting\n');

  // Process any Telegram replies before fetching jobs — saves answers and flips jobs back to "new"
  const answered = await processTelegramReplies(settings, answersPath);
  if (answered > 0) console.log(`📬 Processed ${answered} Telegram answer(s)\n`);

  console.log(`Supported apply types: ${supportedTypes().join(', ')}\n`);

  // Preview mode
  if (isPreview) {
    const newJobs = getJobsByStatus('new');
    if (newJobs.length === 0) { console.log('No new jobs in queue.'); return; }
    console.log(`📋 ${newJobs.length} job(s) queued:\n`);
    for (const j of newJobs) {
      console.log(`  • [${j.apply_type || 'unclassified'}] ${j.title} @ ${j.company || '?'}`);
    }
    return;
  }

  // Get + sort jobs — only enabled apply types
  const allJobs = getJobsByStatus(['new', 'needs_answer'])
    .filter(j => enabledTypes.includes(j.apply_type))
    .sort((a, b) => {
      // Primary: filter_score descending
      const scoreDiff = (b.filter_score ?? 0) - (a.filter_score ?? 0);
      if (scoreDiff !== 0) return scoreDiff;
      // Secondary: recency descending (posted_date or found_at)
      const aDate = new Date(a.posted_date || a.found_at || 0).getTime();
      const bDate = new Date(b.posted_date || b.found_at || 0).getTime();
      return bDate - aDate;
    });
  const jobs = allJobs.slice(0, maxApps);
  console.log(`Enabled types: ${enabledTypes.join(', ')}\n`);
  results.total = jobs.length;

  if (jobs.length === 0) { console.log('Nothing to apply to. Run job_searcher.mjs first.'); return; }

  // Print breakdown
  const typeCounts = jobs.reduce((acc, j) => {
    acc[j.apply_type || 'unclassified'] = (acc[j.apply_type || 'unclassified'] || 0) + 1;
    return acc;
  }, {});
  console.log(`📋 ${jobs.length} jobs to process:`);
  for (const [type, count] of Object.entries(typeCounts)) {
    console.log(`  • ${type}: ${count}`);
  }
  console.log('');

  // Group by platform to share browser sessions
  const byPlatform = {};
  for (const job of jobs) {
    const platform = job.apply_type === 'easy_apply' ? 'linkedin'
      : job.platform === 'wellfound' || job.apply_type === 'wellfound' ? 'wellfound'
      : 'external'; // Greenhouse, Lever etc. — no auth needed
    if (!byPlatform[platform]) byPlatform[platform] = [];
    byPlatform[platform].push(job);
  }

  // Process each platform group — LinkedIn first, then Wellfound, then external
  const platformOrder = ['linkedin', 'wellfound', 'external'];
  const sortedPlatforms = Object.entries(byPlatform)
    .sort((a, b) => (platformOrder.indexOf(a[0]) ?? 99) - (platformOrder.indexOf(b[0]) ?? 99));
  let timedOut = false;
  for (const [platform, platformJobs] of sortedPlatforms) {
    if (timedOut) break;
    console.log(`\n--- ${platform.toUpperCase()} (${platformJobs.length} jobs) ---\n`);
    let browser;
    let platformProfileName = null;
    try {
      // LinkedIn and Wellfound need authenticated sessions; external ATS uses plain browser
      if (platform === 'external') {
        browser = await createBrowser(settings, null); // no profile needed
      } else {
        // Check auth status and get profile name dynamically
        const kernelApiKey = process.env.KERNEL_API_KEY || settings.kernel_api_key;
        const authResult = await ensureAuth(platform, kernelApiKey);
        if (!authResult.ok) {
          console.error(`  ❌ ${platform} auth failed: ${authResult.reason}`);
          await sendTelegram(settings, `⚠️ *${platform}* auth failed — ${authResult.reason}`).catch(() => {});
          for (const job of platformJobs) {
            updateJobStatus(job.id, 'new', { retry_reason: 'auth_failed' });
          }
          continue;
        }
        platformProfileName = authResult.profileName;
        browser = await createBrowser(settings, platformProfileName);
        console.log('  ✅ Logged in\n');
      }

      for (const job of platformJobs) {
        if (isAlreadyApplied(job.id)) {
          console.log(`  ⏭️  Already applied — ${job.title} @ ${job.company || '?'}`);
          updateJobStatus(job.id, 'already_applied', {});
          results.already_applied++;
          continue;
        }

        console.log(`  → [${job.apply_type}] ${job.title} @ ${job.company || '?'}`);

        // Check overall run timeout
        if (Date.now() - startedAt > APPLY_RUN_TIMEOUT_MS) {
          console.log(`  ⏱️  Run timeout (${Math.round(APPLY_RUN_TIMEOUT_MS / 60000)}min) — stopping`);
          timedOut = true;
          break;
        }

        // Set job context for AI answers
        formFiller.jobContext = { title: job.title, company: job.company };

        // Reload answers.json before each job — picks up Telegram replies between jobs
        try {
          const freshAnswers = existsSync(answersPath) ? loadConfig(answersPath) : [];
          formFiller.answers = freshAnswers;
        } catch { /* keep existing answers on read error */ }

        try {
          // If this job previously returned needs_answer and has an AI or user-provided answer,
          // inject it into formFiller so the question gets answered on retry
          if (job.status === 'needs_answer' && job.pending_question && job.ai_suggested_answer) {
            const questionLabel = job.pending_question.label || job.pending_question;
            const answer = job.ai_suggested_answer;
            // Only inject if not already in answers (avoid duplicates across retries)
            const alreadyHas = formFiller.answers.some(a => a.pattern === questionLabel);
            if (!alreadyHas) {
              formFiller.answers.push({ pattern: questionLabel, answer });
              console.log(`    ℹ️  Injecting AI answer for "${questionLabel}": "${String(answer).slice(0, 50)}"`);
            }
          }

          // Per-job timeout — prevents a single hung browser from blocking the run
          const applyStartedAt = Date.now();
          const result = await Promise.race([
            applyToJob(browser.page, job, formFiller),
            new Promise((_, reject) => setTimeout(() => reject(new Error('Job apply timed out')), PER_JOB_TIMEOUT_MS)),
          ]);
          result.applyStartedAt = applyStartedAt;
          await handleResult(job, result, results, settings, profile, apiKey);
        } catch (e) {
          console.error(`    ❌ Error: ${e.message}`);
          if (e.stack) console.error(`    Stack: ${e.stack.split('\n').slice(1, 3).join(' | ').trim()}`);

          // Browser crash recovery — check if page is still usable
          const pageAlive = await browser.page.evaluate(() => true).catch(() => false);
          if (!pageAlive) {
            console.log(`    ℹ️  Browser session dead — creating new browser`);
            await browser.browser?.close().catch(() => {});
            try {
              const newBrowser = platform === 'external'
                ? await createBrowser(settings, null)
                : await createBrowser(settings, platformProfileName);
              browser = newBrowser;
              console.log(`    ✅ New browser session created`);
            } catch (browserErr) {
              console.error(`    ❌ Could not recover browser: ${browserErr.message}`);
              break; // can't continue without a browser
            }
          }

          const retries = (job.retry_count || 0) + 1;
          if (retries <= maxRetries) {
            updateJobStatus(job.id, 'new', { retry_count: retries });
          } else {
            updateJobStatus(job.id, 'failed', { error: e.message });
            appendLog({ ...job, status: 'failed', error: e.message });
            results.failed++;
          }
        }

        // Delay between applications
        await new Promise(r => setTimeout(r, APPLY_BETWEEN_DELAY_BASE + Math.random() * APPLY_BETWEEN_DELAY_JITTER));
      }
    } catch (e) {
      console.error(`  ❌ Browser error for ${platform}: ${e.message}`);
      if (e.stack) console.error(`  Stack: ${e.stack.split('\n').slice(1, 3).join(' | ').trim()}`);
    } finally {
      await browser?.browser?.close().catch(() => {});
    }
  }

  // Final summary + Telegram
  const summary = formatApplySummary(results);
  console.log(`\n${summary.replace(/\*/g, '')}`);
  await sendTelegram(settings, summary);

  // Write last-run metadata
  writeFileSync(resolve(__dir, 'data/applier_last_run.json'), JSON.stringify({
    started_at: startedAt, finished_at: Date.now(), finished: true, ...results
  }, null, 2));

  console.log('\n✅ Apply run complete');
  return results;
}

async function handleResult(job, result, results, settings, profile, apiKey) {
  const { status, meta, pending_question, externalUrl, ats_platform, applyStartedAt } = result;
  const title = meta?.title || job.title || '?';
  const company = meta?.company || job.company || '?';
  const applyDuration = applyStartedAt ? Math.round((Date.now() - applyStartedAt) / 1000) : null;

  // Track per-job detail for summary
  results.jobDetails.push({ title, company, url: job.url, status, duration: applyDuration });

  switch (status) {
    case 'submitted':
      console.log(`    ✅ Applied!${applyDuration ? ` (${applyDuration}s)` : ''}`);
      updateJobStatus(job.id, 'applied', { title, company, applied_at: Date.now(), apply_started_at: applyStartedAt });
      appendLog({ ...job, title, company, status: 'applied', applied_at: Date.now(), apply_started_at: applyStartedAt });
      results.submitted++;
      break;

    case 'needs_answer': {
      const questionText = pending_question?.label || pending_question || 'Unknown question';
      const questionOptions = pending_question?.options || [];
      console.log(`    💬 Paused — unknown question: "${questionText}"${questionOptions.length ? ` (options: ${questionOptions.join(', ')})` : ''}`);
      console.log(`    Generating AI answer and sending to Telegram...`);

      const aiAnswer = await generateAnswer(questionText, profile, apiKey, { title, company });

      const msg = [
        `❓ *New question* — ${company} / ${title}`,
        ``,
        `*Question:* ${questionText}`,
        questionOptions.length ? `*Options:* ${questionOptions.join(' | ')}` : '',
        ``,
        aiAnswer
          ? `*AI answer:*\n${aiAnswer}`
          : `_AI could not generate an answer._`,
        ``,
        `Reply with your answer to store it, or reply *ACCEPT* to use the AI answer.`,
      ].filter(Boolean).join('\n');

      const telegramMsgId = await sendTelegram(settings, msg);

      updateJobStatus(job.id, 'needs_answer', {
        title, company, pending_question,
        ai_suggested_answer: aiAnswer || null,
        telegram_message_id: telegramMsgId,
      });
      appendLog({ ...job, title, company, status: 'needs_answer', pending_question, ai_suggested_answer: aiAnswer });
      results.needs_answer++;
      console.log(`    ⏸️  Question sent to Telegram. Job will retry after you reply.`);
      break;
    }

    case 'skipped_recruiter_only':
      console.log(`    🚫 Recruiter-only`);
      updateJobStatus(job.id, 'skipped_recruiter_only', { title, company });
      appendLog({ ...job, title, company, status: 'skipped_recruiter_only' });
      results.skipped_recruiter++;
      break;

    case 'skipped_external_unsupported': {
      const platform = ats_platform || job.apply_type || 'unknown';
      console.log(`    ⏭️  External ATS: ${platform}`);
      updateJobStatus(job.id, 'skipped_external_unsupported', { title, company, ats_url: externalUrl, ats_platform: platform });
      appendLog({ ...job, title, company, status: 'skipped_external_unsupported', ats_url: externalUrl, ats_platform: platform });
      results.skipped_external++;
      results.atsCounts[platform] = (results.atsCounts[platform] || 0) + 1;
      break;
    }

    case 'closed':
      console.log(`    🚫 Closed — no longer accepting applications`);
      updateJobStatus(job.id, 'closed', { title, company });
      appendLog({ ...job, title, company, status: 'closed' });
      results.closed = (results.closed || 0) + 1;
      break;

    case 'no_modal':
    case 'skipped_no_apply':
    case 'skipped_easy_apply_unsupported':
      console.log(`    ⏭️  Skipped — ${status}`);
      updateJobStatus(job.id, status, { title, company });
      appendLog({ ...job, title, company, status });
      results.skipped_no_apply++;
      break;

    case 'skipped_honeypot':
      console.log(`    ⏭️  Skipped — honeypot`);
      updateJobStatus(job.id, status, { title, company });
      appendLog({ ...job, title, company, status });
      results.skipped_other++;
      break;

    case 'stuck':
    case 'incomplete': {
      const retries = (job.retry_count || 0) + 1;
      const maxRetry = settings.max_retries ?? DEFAULT_MAX_RETRIES;
      if (retries <= maxRetry) {
        console.log(`    ⏭️  ${status} — will retry (attempt ${retries}/${maxRetry})`);
        updateJobStatus(job.id, 'new', { title, company, retry_count: retries });
      } else {
        console.log(`    ⏭️  ${status} — max retries reached`);
        updateJobStatus(job.id, status, { title, company });
        appendLog({ ...job, title, company, status });
      }
      results.skipped_other++;
      break;
    }

    default:
      console.warn(`    ⚠️  Unhandled status: ${status}`);
      updateJobStatus(job.id, status, { title, company });
      appendLog({ ...job, title, company, status });
      results.skipped_other++;
  }
}

main().then(() => {
  process.exit(0);
}).catch(e => {
  console.error('Fatal:', e.message);
  process.exit(1);
});
