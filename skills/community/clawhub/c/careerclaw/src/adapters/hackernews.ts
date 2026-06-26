/**
 * adapters/hackernews.ts — Hacker News "Who is Hiring?" Firebase adapter.
 *
 * Flow:
 *   1. GET /v0/item/{threadId}.json  → thread item with `kids` array
 *   2. GET /v0/item/{commentId}.json → one comment per kid (parallel)
 *   3. Parse each comment: first line is "Company | Role | Location | ..."
 *      remainder is the job description.
 *
 * Parsing is split from fetching so contract tests can call
 * parseComment() directly with fixture JSON — no network mocking needed.
 *
 * HN comment text is HTML — tags are stripped before normalisation.
 * Deleted/dead items (no `text` field or `deleted: true`) are skipped.
 */

import { utcNow } from "../models.js";
import type { NormalizedJob, WorkMode } from "../models.js";
import {
  HN_API_BASE,
  HN_MAX_COMMENTS,
  HN_WHO_IS_HIRING_ID,
  HTTP_TIMEOUT_MS,
  USER_AGENT,
} from "../config.js";
import { stableId, stripHtml } from "./remoteok.js";

// ---------------------------------------------------------------------------
// Types for raw HN API responses
// ---------------------------------------------------------------------------

export interface HnItem {
  id: number;
  type?: string;
  by?: string;
  time?: number;           // Unix seconds UTC
  text?: string;           // HTML-encoded comment body
  kids?: number[];         // child comment IDs
  deleted?: boolean;
  dead?: boolean;
  parent?: number;
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/** Fetch all job comments from the current HN "Who is Hiring?" thread. */
export async function fetchHnJobs(
  threadId: number = HN_WHO_IS_HIRING_ID
): Promise<NormalizedJob[]> {
  const thread = await fetchItem(threadId);
  if (!thread || !thread.kids?.length) return [];

  const kidIds = thread.kids.slice(0, HN_MAX_COMMENTS);
  const fetched_at = utcNow();

  const results = await Promise.allSettled(
    kidIds.map((id) => fetchItem(id))
  );

  return results.flatMap((result) => {
    if (result.status === "rejected") return [];
    const item = result.value;
    if (!item) return [];
    try {
      return [parseComment(item, fetched_at)];
    } catch {
      // Skip non-job comments silently
      return [];
    }
  });
}

/**
 * Parse a single HN comment item into a NormalizedJob.
 * Exported for offline contract testing.
 * Throws if the item cannot be parsed as a job posting.
 */
export function parseComment(item: HnItem, fetched_at?: string): NormalizedJob {
  if (item.deleted || item.dead || !item.text) {
    throw new Error(`Item ${item.id} is deleted, dead, or has no text`);
  }
  if (item.type && item.type !== "comment") {
    throw new Error(`Item ${item.id} is type '${item.type}', not 'comment'`);
  }

  const plainText = stripHtml(item.text);

  // Split on the first blank line — header vs body
  const newlineIdx = plainText.indexOf("\n");
  const headerLine = newlineIdx >= 0 ? plainText.slice(0, newlineIdx).trim() : plainText.trim();
  const bodyText = newlineIdx >= 0 ? plainText.slice(newlineIdx + 1).trim() : "";

  const rawHeader = parseHeader(headerLine);
  const company = stripHtml(rawHeader.company);
  const title = stripHtml(rawHeader.title);
  const location = rawHeader.location;
  const description = bodyText || headerLine;

  const canonical_url = `https://news.ycombinator.com/item?id=${item.id}`;
  const posted_at = item.time
    ? new Date(item.time * 1000).toISOString()
    : null;

  return {
    job_id: stableId(canonical_url),
    title,
    company,
    location,
    description,
    url: canonical_url,
    source: "hackernews",
    salary_min: parseSalaryFromText(description),
    salary_max: null,
    work_mode: inferWorkMode(location, description),
    experience_years: inferExperienceYears(description),
    posted_at,
    fetched_at: fetched_at ?? utcNow(),
  };
}

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

/**
 * Parse the HN comment header line.
 *
 * Common formats:
 *   "Acme | Senior Engineer | Remote | Full-time"
 *   "Acme | Senior Engineer | Remote"
 *   "Acme (hiring) | Engineer"
 *   "Acme - Senior Engineer - Remote"  ← less common, dash separator
 */
function parseHeader(header: string): {
  company: string;
  title: string;
  location: string;
} {
  // Prefer pipe separator; fall back to dash
  const separator = header.includes("|") ? "|" : " - ";
  const parts = header
    .split(separator)
    .map((p) => p.trim())
    .filter(Boolean);

  const company = parts[0] ?? "";
  const title = parts[1] ?? "";
  // Location is usually the 3rd segment; if it looks like a work-mode
  // keyword or a city, use it. Otherwise leave empty.
  const location = parts[2] ?? "";

  return { company, title, location };
}

function inferWorkMode(location: string, description: string): WorkMode | null {
  const text = `${location} ${description}`.toLowerCase();
  if (/\bhybrid\b/.test(text)) return "hybrid";
  if (/\bremote\b/.test(text)) return "remote";
  if (/\bon-?site\b|\bin-?office\b/.test(text)) return "onsite";
  return null;
}

function inferExperienceYears(text: string): number | null {
  const m = text.match(/(\d+)\+?\s*(?:or more\s+)?years?\s+(?:of\s+)?experience/i);
  return m && m[1] ? parseInt(m[1], 10) : null;
}

/**
 * Best-effort salary extraction from free-form description text.
 * Returns the lower bound (salary_min) only; salary_max deferred to Phase 3+.
 */
function parseSalaryFromText(text: string): number | null {
  // "$120k", "$120,000", "120k", "$120K+"
  const m = text.match(/\$\s*([\d,]+)\s*k\b/i);
  if (m && m[1]) return parseInt(m[1].replace(/,/g, ""), 10) * 1_000;

  const m2 = text.match(/\$\s*([\d]{3,3}),([\d]{3})/);
  if (m2 && m2[1] && m2[2]) {
    return parseInt(`${m2[1]}${m2[2]}`, 10);
  }
  return null;
}

// ---------------------------------------------------------------------------
// HTTP fetch helper
// ---------------------------------------------------------------------------

async function fetchItem(id: number): Promise<HnItem | null> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), HTTP_TIMEOUT_MS);
  try {
    const res = await fetch(`${HN_API_BASE}/item/${id}.json`, {
      signal: controller.signal,
      headers: { "User-Agent": USER_AGENT },
    });
    if (!res.ok) return null;
    return (await res.json()) as HnItem;
  } catch {
    return null;
  } finally {
    clearTimeout(timer);
  }
}
