#!/usr/bin/env node

/**
 * ClawInsight Skill Client
 *
 * Lightweight API client for the ClawInsight research platform.
 * All network requests go ONLY to claw-insight.vercel.app.
 * All data submissions require explicit user approval.
 *
 * Source: https://github.com/ClawInsight/claw-insight-skill
 */

const BASE_URL = 'https://claw-insight.vercel.app/api/skill';

// Allowed fields for registration — nothing else is ever sent
const ALLOWED_PROFILE_FIELDS = ['age_range', 'city', 'gender', 'interests', 'occupation'];

// Allowed fields for survey responses — nothing else is ever sent
const ALLOWED_RESPONSE_FIELDS = ['assignment_id', 'question_key', 'raw_answer', 'confidence', 'source', 'response_time_ms'];

// Valid source values
const VALID_SOURCES = ['draft', 'conversation', 'direct'];

function sanitizeProfile(profile) {
  if (!profile) return {};
  const clean = {};
  for (const key of ALLOWED_PROFILE_FIELDS) {
    if (profile[key] !== undefined) {
      clean[key] = profile[key];
    }
  }
  return clean;
}

function sanitizeResponse(response) {
  if (!response) return {};
  const clean = {};
  for (const key of ALLOWED_RESPONSE_FIELDS) {
    if (response[key] !== undefined) {
      clean[key] = response[key];
    }
  }
  // Validate source
  if (clean.source && !VALID_SOURCES.includes(clean.source)) {
    clean.source = 'draft';
  }
  return clean;
}

async function request(path, options = {}) {
  const url = `${BASE_URL}${path}`;

  // Security: verify we're only connecting to the declared server
  if (!url.startsWith('https://claw-insight.vercel.app/')) {
    throw new Error('Security: ClawInsight only connects to claw-insight.vercel.app');
  }

  const res = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  return res.json();
}

function authHeaders(apiKey) {
  return { Authorization: `Bearer ${apiKey}` };
}

/**
 * Register a new user.
 * Returns { api_key, user_id, message }
 */
async function register({ openclaw_id, email, profile, timestamp }) {
  return request('/register', {
    method: 'POST',
    body: JSON.stringify({
      openclaw_id,
      email,
      timestamp: timestamp || new Date().toISOString(),
      profile: sanitizeProfile(profile),
    }),
  });
}

/**
 * List available tasks for the authenticated user.
 */
async function listTasks(apiKey) {
  return request('/tasks', {
    headers: authHeaders(apiKey),
  });
}

/**
 * Claim a task assignment.
 */
async function claimTask(apiKey, taskId, profile) {
  return request(`/tasks/${taskId}/claim`, {
    method: 'POST',
    headers: authHeaders(apiKey),
    body: JSON.stringify({
      user_profile: sanitizeProfile(profile),
    }),
  });
}

/**
 * Submit a user-approved survey response.
 * Only the allowed fields are sent — everything else is stripped.
 */
async function submitResponse(apiKey, responseData) {
  return request('/responses', {
    method: 'POST',
    headers: authHeaders(apiKey),
    body: JSON.stringify(sanitizeResponse(responseData)),
  });
}

/**
 * Get earnings and balance.
 */
async function getEarnings(apiKey) {
  return request('/earnings', {
    headers: authHeaders(apiKey),
  });
}

/**
 * Request a magic link login email.
 */
async function requestMagicLink(apiKey, openclaw_id) {
  return request('/magic-link', {
    method: 'POST',
    headers: authHeaders(apiKey),
    body: JSON.stringify({ openclaw_id }),
  });
}

/**
 * Delete account and all personal data.
 */
async function deleteAccount(apiKey) {
  return request('/account', {
    method: 'DELETE',
    headers: authHeaders(apiKey),
  });
}

module.exports = {
  BASE_URL,
  ALLOWED_PROFILE_FIELDS,
  ALLOWED_RESPONSE_FIELDS,
  VALID_SOURCES,
  register,
  listTasks,
  claimTask,
  submitResponse,
  getEarnings,
  requestMagicLink,
  deleteAccount,
};
