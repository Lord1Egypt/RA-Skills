/**
 * notify.mjs — Telegram notifications
 * Sends messages directly via Telegram Bot API
 */
import { TELEGRAM_API_BASE, NOTIFY_RATE_LIMIT_MS } from './constants.mjs';

let lastSentAt = 0;

/**
 * Send a Telegram message. Returns the message_id on success (useful for tracking replies).
 */
export async function sendTelegram(settings, message) {
  const { bot_token, telegram_user_id } = settings.notifications || {};
  if (!bot_token || !telegram_user_id) {
    console.log(`[notify] No Telegram config — would send: ${message.substring(0, 80)}`);
    return null;
  }

  // Rate limit to avoid Telegram API throttling
  const now = Date.now();
  const elapsed = now - lastSentAt;
  if (elapsed < NOTIFY_RATE_LIMIT_MS) {
    await new Promise(r => setTimeout(r, NOTIFY_RATE_LIMIT_MS - elapsed));
  }

  const url = `${TELEGRAM_API_BASE}${bot_token}/sendMessage`;
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: telegram_user_id,
        text: message,
        parse_mode: 'Markdown',
      }),
    });
    lastSentAt = Date.now();
    if (!res.ok) { console.error(`[notify] Telegram HTTP error: ${res.status}`); return null; }
    const data = await res.json();
    if (!data.ok) { console.error('[notify] Telegram error:', data.description); return null; }
    return data.result?.message_id || null;
  } catch (e) {
    console.error('[notify] Failed to send Telegram message:', e.message);
    return null;
  }
}

/**
 * Get updates from Telegram Bot API (long polling).
 * @param {string} botToken
 * @param {number} offset - Update ID offset (pass last_update_id + 1)
 * @param {number} timeout - Long poll timeout in seconds
 * @returns {Array} Array of update objects
 */
export async function getTelegramUpdates(botToken, offset = 0, timeout = 5) {
  const url = `${TELEGRAM_API_BASE}${botToken}/getUpdates`;
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ offset, timeout }),
    });
    if (!res.ok) return [];
    const data = await res.json();
    return data.ok ? (data.result || []) : [];
  } catch {
    return [];
  }
}

/**
 * Reply to a specific Telegram message.
 */
export async function replyTelegram(botToken, chatId, replyToMessageId, text) {
  const url = `${TELEGRAM_API_BASE}${botToken}/sendMessage`;
  try {
    await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        text,
        reply_to_message_id: replyToMessageId,
        parse_mode: 'Markdown',
      }),
    });
  } catch { /* best effort */ }
}

export function formatSearchSummary(added, skipped, platforms, trackCounts = {}) {
  if (added === 0) return `🔍 *Job Search Complete*\nNo new jobs found this run.`;
  const lines = [
    `🔍 *Job Search Complete*`,
    `${added} new job${added !== 1 ? 's' : ''} added (${skipped} already seen)`,
    `Platforms: ${platforms.join(', ')}`,
  ];
  if (Object.keys(trackCounts).length > 0) {
    lines.push('');
    for (const [track, counts] of Object.entries(trackCounts)) {
      lines.push(`• *${track}*: ${counts.added} new / ${counts.found} found`);
    }
  }
  return lines.join('\n');
}

export function formatApplySummary(results) {
  const { total, jobDetails = [] } = results;

  const applied = jobDetails.filter(j => j.status === 'submitted').length;
  const lines = [`*Apply Run Complete* — ${applied}/${total} applied`];

  // Group jobs by display category
  const categories = [
    { key: 'submitted', emoji: '📬', label: 'Applied' },
    { key: 'needs_answer', emoji: '💬', label: 'Needs Answer' },
    { key: 'closed', emoji: '🚫', label: 'Closed' },
    { key: 'incomplete', emoji: '⚠️', label: 'Incomplete' },
    { key: 'stuck', emoji: '⚠️', label: 'Stuck' },
    { key: 'skipped_honeypot', emoji: '⚠️', label: 'Honeypot' },
    { key: 'skipped_no_apply', emoji: '⏭️', label: 'No Apply Button' },
    { key: 'no_modal', emoji: '⏭️', label: 'No Modal' },
    { key: 'skipped_recruiter_only', emoji: '🚫', label: 'Recruiter Only' },
    { key: 'skipped_external_unsupported', emoji: '🌐', label: 'External ATS' },
  ];

  for (const { key, emoji, label } of categories) {
    const jobs = jobDetails.filter(j => j.status === key);
    if (jobs.length === 0) continue;
    lines.push('');
    lines.push(`${emoji} *${label}:*`);
    for (const j of jobs) {
      const shortUrl = (j.url || '').replace(/^https?:\/\/(?:www\.)?/, '').replace(/\/$/, '');
      lines.push(`• ${j.title} @ ${j.company}`);
      if (shortUrl) lines.push(`${shortUrl}`);
    }
  }

  if (jobDetails.some(j => j.status === 'needs_answer')) {
    lines.push('', '💬 Check Telegram — questions waiting for your answers');
  }

  return lines.join('\n');
}

export function formatFilterSummary({ passed, filtered, errors, cost, topJobs = [] }) {
  const lines = [
    `🧠 *AI Filter Complete*`,
    `✅ Passed: ${passed} | 🚫 Filtered: ${filtered}${errors ? ` | ⚠️ Errors: ${errors}` : ''}`,
  ];
  if (cost != null) lines.push(`💰 Cost: $${cost.toFixed(2)}`);
  if (topJobs.length > 0) {
    lines.push('', '*Top scores:*');
    for (const j of topJobs.slice(0, 5)) {
      lines.push(`• ${j.score} — ${j.title} @ ${j.company}`);
    }
  }
  return lines.join('\n');
}

export function formatUnknownQuestion(job, question) {
  return `❓ *Unknown question while applying*\n\n*Job:* ${job.title} @ ${job.company}\n*Question:* "${question}"\n\nWhat should I answer? (Reply and I'll save it for all future runs)`;
}
