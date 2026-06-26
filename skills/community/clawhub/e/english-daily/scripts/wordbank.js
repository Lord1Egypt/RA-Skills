#!/usr/bin/env node
/**
 * english-daily — Word Bank Loader + SRS Utilities
 * Utility module (not a CLI entry point). Exports helpers for all scripts.
 */

'use strict';

const fs = require('fs');
const path = require('path');

const WORDBANK_PATH = path.join(__dirname, '../data/wordbank.json');

/** Load and return the full word bank array */
function loadWordBank() {
  const raw = fs.readFileSync(WORDBANK_PATH, 'utf8');
  return JSON.parse(raw);
}

/** Filter words by CEFR level (A1/A2/B1/B2) */
function getWordsByLevel(level) {
  return loadWordBank().filter(w => w.lv === level);
}

/** Find a word entry by exact word string */
function getWordByText(word) {
  return loadWordBank().find(w => w.w === word) || null;
}

/**
 * Return words the user hasn't studied yet, matching their level.
 * Falls back to next level up if not enough words remain.
 * @param {Object} profile  user profile
 * @param {number} count    how many new words to return
 * @returns {Array}
 */
function getNewWordsForUser(profile, count) {
  const bank = loadWordBank();
  const studied = new Set(Object.keys(profile.wordProgress || {}));

  // Levels to draw from, starting at user's level and going up
  const levelOrder = ['A1', 'A2', 'B1', 'B2'];
  const startIdx = levelOrder.indexOf(profile.level || 'B1');
  const levelsToTry = levelOrder.slice(startIdx);

  const candidates = [];
  for (const lv of levelsToTry) {
    const words = bank.filter(w => w.lv === lv && !studied.has(w.w));
    candidates.push(...words);
    if (candidates.length >= count) break;
  }

  return candidates.slice(0, count);
}

/**
 * Return all words due for SRS review today (nextReview <= today).
 * @param {Object} profile
 * @returns {Array} array of word bank entries
 */
function getDueWords(profile) {
  const bank = loadWordBank();
  const today = todayStr();
  const progress = profile.wordProgress || {};

  return bank.filter(entry => {
    const p = progress[entry.w];
    if (!p) return false;
    return p.nextReview <= today;
  });
}

/**
 * SM-2 simplified SRS update.
 * quality: 1=forgot, 2=hard, 3=ok, 4=easy
 * @param {Object} profile  (mutated in place)
 * @param {string} word
 * @param {number} quality  1-4
 */
function updateWordProgress(profile, word, quality) {
  if (!profile.wordProgress) profile.wordProgress = {};

  const prev = profile.wordProgress[word] || { interval: 1, repetitions: 0, ease: 2.5 };
  let { interval, repetitions, ease } = prev;

  if (quality <= 2) {
    interval = 1;
    repetitions = 0;
  } else {
    const multiplier = quality === 3 ? 1.5 : 2;
    interval = Math.min(Math.round(interval * multiplier), 30);
    repetitions += 1;
  }

  // Ease factor adjustment (SM-2 inspired)
  ease = Math.max(1.3, ease + 0.1 - (4 - quality) * 0.08);

  const nextReview = addDays(todayStr(), interval);

  profile.wordProgress[word] = {
    interval,
    repetitions,
    ease: Math.round(ease * 100) / 100,
    nextReview,
    lastQuality: quality
  };
}

/**
 * Summary stats for a user's word progress.
 * @param {Object} profile
 * @returns {{ total: number, due: number, mastered: number, learning: number }}
 */
function getWordStats(profile) {
  const bank = loadWordBank();
  const total = bank.filter(w => w.lv === profile.level ||
    ['A1','A2','B1','B2'].indexOf(w.lv) <= ['A1','A2','B1','B2'].indexOf(profile.level)).length;
  const today = todayStr();
  const progress = profile.wordProgress || {};

  let due = 0, mastered = 0, learning = 0;
  for (const [word, p] of Object.entries(progress)) {
    if (p.nextReview <= today) due++;
    if (p.interval >= 7) mastered++;
    else learning++;
  }

  return { total, due, mastered, learning };
}

// ── Helpers ───────────────────────────────────────────────────────────────────

/** Returns today's date as YYYY-MM-DD string (Asia/Shanghai local time) */
function todayStr() {
  const now = new Date();
  const cst = new Date(now.toLocaleString('en-US', { timeZone: 'Asia/Shanghai' }));
  const y = cst.getFullYear();
  const m = String(cst.getMonth() + 1).padStart(2, '0');
  const d = String(cst.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

/** Add `days` to a YYYY-MM-DD string, return new YYYY-MM-DD string */
function addDays(dateStr, days) {
  const d = new Date(dateStr + 'T12:00:00Z');
  d.setUTCDate(d.getUTCDate() + days);
  return d.toISOString().slice(0, 10);
}

module.exports = {
  loadWordBank,
  getWordsByLevel,
  getWordByText,
  getNewWordsForUser,
  getDueWords,
  updateWordProgress,
  getWordStats,
  todayStr,
  addDays
};
