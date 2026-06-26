#!/usr/bin/env node
/**
 * Utility functions for ClawQuest skill scripts
 */

// ─── API ──────────────────────────────────────────────────────────────────────

const API_BASE = process.env.CLAWQUEST_API_URL || 'https://api.clawquest.ai';

/**
 * Make a public API request to ClawQuest (no auth required)
 * @param {string} endpoint - e.g. /quests
 */
export async function apiRequest(endpoint) {
  const url = `${API_BASE}${endpoint}`;
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
  });

  const text = await response.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = { text };
  }

  if (!response.ok) {
    const err = new Error(
      data?.error?.message || `API Error: ${response.status} ${response.statusText}`
    );
    err.status = response.status;
    err.data = data;
    throw err;
  }

  return data?.data !== undefined ? data.data : data;
}

// ─── Logging ──────────────────────────────────────────────────────────────────

export function success(message) { console.log(`✅ ${message}`); }
export function error(message) { console.log(`❌ ${message}`); }
export function warning(message) { console.log(`⚠️  ${message}`); }
export function info(message) { console.log(`ℹ️  ${message}`); }
export function prettyJson(obj) { return JSON.stringify(obj, null, 2); }
