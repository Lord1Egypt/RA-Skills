/**
 * telegram_answers.mjs — Process Telegram replies to question messages
 *
 * Shared by telegram_poller.mjs (cron) and job_applier.mjs (safety net).
 *
 * Flow:
 * 1. Poll Telegram getUpdates for new messages
 * 2. Match replies to needs_answer jobs via reply_to_message_id
 * 3. Save answer to answers.json (reused for ALL future jobs)
 * 4. Flip job back to "new" for retry
 * 5. Send confirmation reply
 */
import { existsSync, readFileSync, writeFileSync, renameSync } from 'fs';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

import { loadQueue, saveQueue } from './queue.mjs';
import { getTelegramUpdates, replyTelegram } from './notify.mjs';

const __dir = dirname(fileURLToPath(import.meta.url));
const OFFSET_PATH = resolve(__dir, '../data/telegram_offset.json');

function loadOffset() {
  if (!existsSync(OFFSET_PATH)) return 0;
  try {
    return JSON.parse(readFileSync(OFFSET_PATH, 'utf8')).offset || 0;
  } catch { return 0; }
}

function saveOffset(offset) {
  writeFileSync(OFFSET_PATH, JSON.stringify({ offset }));
}

function loadAnswers(path) {
  if (!existsSync(path)) return [];
  const raw = JSON.parse(readFileSync(path, 'utf8'));
  // Normalize: support both object {"q":"a"} and array [{pattern,answer}] formats
  if (Array.isArray(raw)) return raw;
  if (raw && typeof raw === 'object') {
    return Object.entries(raw).map(([pattern, answer]) => ({ pattern, answer: String(answer) }));
  }
  return [];
}

function saveAnswers(path, answers) {
  const tmp = path + '.tmp';
  writeFileSync(tmp, JSON.stringify(answers, null, 2));
  renameSync(tmp, path);
}

/**
 * Process pending Telegram replies. Returns number of answers processed.
 * @param {object} settings - settings.json contents
 * @param {string} answersPath - absolute path to answers.json
 * @returns {number} count of answers saved
 */
export async function processTelegramReplies(settings, answersPath) {
  const botToken = settings.notifications?.bot_token;
  const chatId = settings.notifications?.telegram_user_id;
  if (!botToken || !chatId) return 0;

  const offset = loadOffset();
  const updates = await getTelegramUpdates(botToken, offset, 1);
  if (updates.length === 0) return 0;

  // Build lookup: telegram_message_id → job
  const queue = loadQueue();
  const jobsByMsgId = new Map();
  for (const job of queue) {
    if (job.status === 'needs_answer' && job.telegram_message_id) {
      jobsByMsgId.set(job.telegram_message_id, job);
    }
  }

  let queueDirty = false;
  let answersDirty = false;
  const answers = loadAnswers(answersPath);
  let maxUpdateId = offset;
  let processed = 0;

  for (const update of updates) {
    maxUpdateId = Math.max(maxUpdateId, update.update_id);

    const msg = update.message;
    if (!msg || !msg.text) continue;
    if (String(msg.chat?.id) !== String(chatId)) continue;

    const replyTo = msg.reply_to_message?.message_id;
    const text = msg.text.trim();

    // Match reply to a pending question
    let matchedJob = null;
    if (replyTo && jobsByMsgId.has(replyTo)) {
      matchedJob = jobsByMsgId.get(replyTo);
    } else if (!replyTo) {
      // Not a reply — match to the single pending question if only one exists
      const pending = queue
        .filter(j => j.status === 'needs_answer' && j.telegram_message_id)
        .sort((a, b) => (b.status_updated_at || '').localeCompare(a.status_updated_at || ''));
      if (pending.length === 1) {
        matchedJob = pending[0];
      } else if (pending.length > 1) {
        await replyTelegram(botToken, chatId, msg.message_id,
          `I have ${pending.length} questions waiting. Please *reply* to the specific question message so I know which one you're answering.`
        );
        continue;
      }
    }

    if (!matchedJob) continue;

    const questionLabel = matchedJob.pending_question?.label || matchedJob.pending_question || '';
    const questionOptions = matchedJob.pending_question?.options || [];
    let answer;

    if (/^accept$/i.test(text)) {
      answer = matchedJob.ai_suggested_answer;
      if (!answer) {
        await replyTelegram(botToken, chatId, msg.message_id,
          `No AI answer available for this question. Please type your answer directly.`
        );
        continue;
      }
    } else {
      answer = text;
    }

    // For select fields, match reply to exact option text
    if (questionOptions.length > 0) {
      const matched = questionOptions.find(o => o.toLowerCase() === answer.toLowerCase());
      if (matched) answer = matched;
    }

    // Save to answers.json
    if (questionLabel) {
      const existing = answers.findIndex(a => a.pattern === questionLabel);
      if (existing >= 0) {
        answers[existing].answer = answer;
      } else {
        answers.push({ pattern: questionLabel, answer });
      }
      answersDirty = true;
    }

    // Flip job back to "new"
    const idx = queue.findIndex(j => j.id === matchedJob.id);
    if (idx >= 0) {
      queue[idx] = {
        ...queue[idx],
        status: 'new',
        status_updated_at: new Date().toISOString(),
        telegram_message_id: null,
      };
      queueDirty = true;
    }

    await replyTelegram(botToken, chatId, msg.message_id,
      `Saved "${answer}" for "${questionLabel.slice(0, 60)}"\n\n${matchedJob.title} @ ${matchedJob.company} will be retried next run.`
    );

    console.log(`[telegram] Saved answer for "${questionLabel}": "${answer.slice(0, 50)}"`);
    processed++;
  }

  if (answersDirty) saveAnswers(answersPath, answers);
  if (queueDirty) saveQueue(queue);
  saveOffset(maxUpdateId + 1);

  return processed;
}
