/**
 * filter.mjs — AI job relevance filter (Anthropic Batch API)
 * Scores queued jobs 0-10 against candidate profile using Claude (Sonnet by default)
 * Uses Batch API for 50% cost savings + prompt caching for shared context
 */

import { readFileSync, existsSync } from 'fs';
import {
  ANTHROPIC_BATCH_API_URL, FILTER_DESC_MAX_CHARS, FILTER_BATCH_MAX_TOKENS
} from './constants.mjs';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

export function loadProfile(profilePath) {
  if (!profilePath || !existsSync(profilePath)) return null;
  try { return JSON.parse(readFileSync(profilePath, 'utf8')); } catch { return null; }
}

function buildSystemPrompt(jobProfile, candidateProfile) {
  return `You are a job relevance scorer. Score each job listing 0-10 based on how well it matches the candidate profile below.

## Candidate Profile
${JSON.stringify(candidateProfile, null, 2)}

## Target Job Profile
${JSON.stringify(jobProfile, null, 2)}

## Instructions
- Use the candidate profile and target job profile above as your only criteria
- Score based on title fit, industry fit, experience match, salary range, location/remote requirements, and any exclude_keywords
- 10 = perfect match, 0 = completely irrelevant
- If salary is unknown, do not penalize
- If a posting is from a staffing agency but the role itself matches, score the role — not the agency

Return ONLY a JSON object: {"score": <0-10>, "reason": "<one concise line>"}`;
}

function sanitize(str) {
  // Remove lone surrogates and other invalid Unicode that breaks JSON encoding
  return (str || '').replace(/[\uD800-\uDFFF]/g, '').replace(/\0/g, '');
}

function buildJobMessage(job) {
  const desc = sanitize(job.description).substring(0, FILTER_DESC_MAX_CHARS).replace(/\s+/g, ' ').trim();
  return `Title: ${sanitize(job.title)}
Company: ${sanitize(job.company) || 'Unknown'}
Location: ${sanitize(job.location) || 'Unknown'}
Description: ${desc}

Return ONLY: {"score": <0-10>, "reason": "<one line>"}`;
}

// ---------------------------------------------------------------------------
// Batch API
// ---------------------------------------------------------------------------

function apiHeaders(apiKey) {
  return {
    'Content-Type': 'application/json',
    'x-api-key': apiKey,
    'anthropic-version': '2023-06-01',
    'anthropic-beta': 'prompt-caching-2024-07-31',
  };
}

/**
 * Submit one batch per track (one per job profile/search description).
 * Each batch uses the system prompt for that track only — maximizes prompt caching.
 * Returns array of { track, batchId, idMap, jobCount }
 */
export async function submitBatches(jobs, jobProfilesByTrack, candidateProfile, model, apiKey) {
  // Group jobs by track
  const byTrack = {};
  for (const job of jobs) {
    const track = job.track || 'ae';
    if (!jobProfilesByTrack[track]) continue; // no profile → skip
    if (!byTrack[track]) byTrack[track] = [];
    byTrack[track].push(job);
  }

  if (Object.keys(byTrack).length === 0) throw new Error('No jobs to submit — check job profiles are configured');

  const submitted = [];

  for (const [track, trackJobs] of Object.entries(byTrack)) {
    const jobProfile = jobProfilesByTrack[track];
    const systemPrompt = buildSystemPrompt(jobProfile, candidateProfile);
    const idMap = {};
    const requests = [];

    for (const job of trackJobs) {
      // Anthropic custom_id max 64 chars
      const customId = job.id.length <= 64 ? job.id : job.id.substring(0, 64);
      idMap[customId] = job.id;

      requests.push({
        custom_id: customId,
        params: {
          model,
          max_tokens: FILTER_BATCH_MAX_TOKENS,
          system: [{ type: 'text', text: systemPrompt, cache_control: { type: 'ephemeral' } }],
          messages: [{ role: 'user', content: buildJobMessage(job) }],
        }
      });
    }

    const res = await fetch(ANTHROPIC_BATCH_API_URL, {
      method: 'POST',
      headers: apiHeaders(apiKey),
      body: JSON.stringify({ requests }),
    });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(`Batch submit failed for track "${track}" ${res.status}: ${err}`);
    }

    const data = await res.json();
    submitted.push({ track, batchId: data.id, idMap, jobCount: trackJobs.length });
    console.log(`  [${track}] ${trackJobs.length} jobs → batch ${data.id}`);
  }

  return submitted;
}

/**
 * Check batch status. Returns { status: 'in_progress'|'ended', counts }
 */
export async function checkBatch(batchId, apiKey) {
  const res = await fetch(`${ANTHROPIC_BATCH_API_URL}/${batchId}`, {
    headers: apiHeaders(apiKey),
  });

  if (!res.ok) throw new Error(`Batch status check failed ${res.status}`);
  const data = await res.json();

  return {
    status: data.processing_status, // 'in_progress' | 'ended'
    counts: data.request_counts,    // { processing, succeeded, errored, canceled, expired }
    resultsUrl: data.results_url,
  };
}

/**
 * Download and parse batch results. Returns array of { jobId, score, reason, error }
 */
// Sonnet batch API pricing (per million tokens)
const PRICING = {
  input:          1.50,
  output:         7.50,
  cache_write:    1.875,
  cache_read:     0.15,
};

export async function downloadResults(batchId, apiKey, idMap = {}) {
  const res = await fetch(`${ANTHROPIC_BATCH_API_URL}/${batchId}/results`, {
    headers: apiHeaders(apiKey),
  });

  if (!res.ok) throw new Error(`Results download failed ${res.status}`);

  const text = await res.text();
  const lines = text.trim().split('\n').filter(Boolean);
  const results = [];
  const usage = { input_tokens: 0, output_tokens: 0, cache_creation_input_tokens: 0, cache_read_input_tokens: 0 };

  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      const jobId = idMap[entry.custom_id] || entry.custom_id;

      // Accumulate token usage
      const u = entry.result?.message?.usage;
      if (u) {
        usage.input_tokens += u.input_tokens || 0;
        usage.output_tokens += u.output_tokens || 0;
        usage.cache_creation_input_tokens += u.cache_creation_input_tokens || 0;
        usage.cache_read_input_tokens += u.cache_read_input_tokens || 0;
      }

      if (entry.result?.type === 'succeeded') {
        const content = entry.result.message?.content?.[0]?.text || '';
        try {
          const clean = content.replace(/```json\n?|\n?```/g, '').trim();
          const parsed = JSON.parse(clean);
          results.push({ jobId, score: parsed.score, reason: parsed.reason });
        } catch {
          results.push({ jobId, score: null, reason: 'parse_error', error: true });
        }
      } else {
        results.push({ jobId, score: null, reason: entry.result?.type || 'unknown_error', error: true });
      }
    } catch {
      // malformed line — skip
    }
  }

  // Calculate estimated cost
  const cost = (
    (usage.input_tokens * PRICING.input) +
    (usage.output_tokens * PRICING.output) +
    (usage.cache_creation_input_tokens * PRICING.cache_write) +
    (usage.cache_read_input_tokens * PRICING.cache_read)
  ) / 1_000_000;

  return { results, usage, cost: Math.round(cost * 100) / 100 };
}
