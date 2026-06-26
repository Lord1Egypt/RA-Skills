/**
 * search_progress.mjs — Track which searches have completed
 * Enables resume on restart — skips completed tracks and completed keywords within a track
 */
import { readFileSync, writeFileSync, existsSync, unlinkSync } from 'fs';

let progressPath = null;
let progress = null;

export function initProgress(dataDir, lookbackDays) {
  progressPath = `${dataDir}/search_progress.json`;

  if (existsSync(progressPath)) {
    const saved = JSON.parse(readFileSync(progressPath, 'utf8'));
    if (saved.lookback_days === lookbackDays) {
      progress = saved;
      const done = progress.completed?.length ?? 0;
      if (done > 0) {
        console.log(`🔁 Resuming — completed tracks: ${progress.completed.join(', ')}\n`);
      }
      return progress;
    }
    console.log(`🆕 New lookback window (${lookbackDays}d), starting fresh\n`);
  }

  progress = {
    lookback_days: lookbackDays,
    started_at: Date.now(),
    completed: [],
    keyword_progress: {},  // key: "platform:track" → last completed keyword index (0-based)
  };
  save();
  return progress;
}

/** Save generated keywords for a track — reused on resume, never regenerated mid-run */
export function saveKeywords(platform, track, keywords) {
  if (!progress) return;
  if (!progress.keywords) progress.keywords = {};
  progress.keywords[`${platform}:${track}`] = keywords;
  save();
}

/** Get saved keywords for a track, or null if not yet generated */
export function getSavedKeywords(platform, track) {
  return progress?.keywords?.[`${platform}:${track}`] ?? null;
}

export function isCompleted(platform, track) {
  if (!progress) return false;
  return progress.completed.includes(`${platform}:${track}`);
}

/** Returns the index of the first keyword to run (skips already-completed ones) */
export function getKeywordStart(platform, track) {
  if (!progress) return 0;
  const key = `${platform}:${track}`;
  const last = progress.keyword_progress?.[key] ?? -1;
  return last + 1; // resume from next keyword after last completed
}

/** Call after each keyword completes */
export function markKeywordComplete(platform, track, keywordIndex) {
  if (!progress) return;
  const key = `${platform}:${track}`;
  if (!progress.keyword_progress) progress.keyword_progress = {};
  progress.keyword_progress[key] = keywordIndex;
  save();
}

export function markComplete(platform, track, stats) {
  if (!progress) return;
  const key = `${platform}:${track}`;
  if (!progress.completed.includes(key)) progress.completed.push(key);
  // Clean up per-keyword progress for completed track
  if (progress.keyword_progress) delete progress.keyword_progress[key];
  progress[`stats:${key}`] = { ...stats, completed_at: Date.now() };
  save();
}

export function clearProgress() {
  try { if (progressPath) unlinkSync(progressPath); } catch {}
  progress = null;
}

function save() {
  if (progressPath && progress) {
    writeFileSync(progressPath, JSON.stringify(progress, null, 2));
  }
}
