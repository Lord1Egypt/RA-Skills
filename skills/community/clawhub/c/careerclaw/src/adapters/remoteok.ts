/**
 * adapters/remoteok.ts — RemoteOK RSS adapter.
 *
 * Fetches the RemoteOK RSS feed and normalises each <item> into a
 * NormalizedJob. Parsing is split from fetching so contract tests can
 * call parseRss() directly with fixture XML — no network mocking needed.
 *
 * RemoteOK RSS structure (abridged):
 *   <item>
 *     <title><![CDATA[Senior Engineer at Acme]]></title>
 *     <link>https://remoteok.com/remote-jobs/123</link>
 *     <pubDate>Mon, 03 Mar 2026 10:00:00 +0000</pubDate>
 *     <description><![CDATA[<p>HTML description...</p>]]></description>
 *     <location>Worldwide</location>          <!-- optional -->
 *     <salary>$120,000 - $180,000</salary>    <!-- optional -->
 *     <company><![CDATA[Acme Corp]]></company> <!-- optional -->
 *     <tag>typescript</tag>                    <!-- 0-n tags -->
 *   </item>
 */

import { createHash } from "node:crypto";
import { XMLParser } from "fast-xml-parser";
import { utcNow } from "../models.js";
import type { NormalizedJob, WorkMode } from "../models.js";
import {
  HTTP_TIMEOUT_MS,
  REMOTEOK_RSS_URL,
  USER_AGENT,
} from "../config.js";

// ---------------------------------------------------------------------------
// Types for the raw RSS parse tree
// ---------------------------------------------------------------------------

interface RssItem {
  title?: string;
  link?: string;
  pubDate?: string;
  description?: string;
  location?: string;
  salary?: string;
  company?: string;
  /** fast-xml-parser returns a single value or an array for repeated tags */
  tag?: string | string[];
}

interface RssFeed {
  rss?: { channel?: { item?: RssItem | RssItem[] } };
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/** Fetch the RemoteOK RSS feed and return normalised jobs. */
export async function fetchRemoteOkJobs(): Promise<NormalizedJob[]> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), HTTP_TIMEOUT_MS);

  try {
    const res = await fetch(REMOTEOK_RSS_URL, {
      signal: controller.signal,
      headers: { "User-Agent": USER_AGENT },
    });
    if (!res.ok) {
      throw new Error(`RemoteOK RSS returned HTTP ${res.status}`);
    }
    const xml = await res.text();
    return parseRss(xml);
  } finally {
    clearTimeout(timer);
  }
}

/**
 * Parse a RemoteOK RSS XML string into NormalizedJob[].
 * Exported for offline contract testing.
 */
export function parseRss(xml: string): NormalizedJob[] {
  const parser = new XMLParser({
    ignoreAttributes: false,
    cdataPropName: "__cdata",
    isArray: (_name, jpath) => jpath === "rss.channel.item",
  });

  const feed = parser.parse(xml) as RssFeed;
  const rawItems = feed?.rss?.channel?.item;
  if (!rawItems) return [];
  const items = Array.isArray(rawItems) ? rawItems : [rawItems];
  const fetched_at = utcNow();

  return items.flatMap((item) => {
    try {
      return [normaliseItem(item, fetched_at)];
    } catch {
      // Skip malformed items rather than aborting the whole feed
      return [];
    }
  });
}

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

function normaliseItem(item: RssItem, fetched_at: string): NormalizedJob {
  const rawTitle = coerceString(item.title);
  const url = coerceString(item.link);
  const rawDescription = stripHtml(coerceString(item.description));
  const rawLocation = coerceString(item.location);
  const rawSalary = coerceString(item.salary);
  const rawCompany = coerceString(item.company);

  const { title, company } = parseTitle(rawTitle, rawCompany);
  const { salary_min, salary_max } = parseSalary(rawSalary, rawDescription);
  const work_mode = inferWorkMode(rawLocation, rawDescription);
  const experience_years = inferExperienceYears(rawDescription);

  // Combine location tag with description inference
  const location = rawLocation || inferLocationLabel(rawDescription);

  return {
    job_id: stableId(url || `${company}:${title}`),
    title,
    company,
    location,
    description: rawDescription,
    url,
    source: "remoteok",
    salary_min,
    salary_max,
    work_mode,
    experience_years,
    posted_at: parsePubDate(coerceString(item.pubDate)),
    fetched_at,
  };
}

/**
 * Split "Senior Engineer at Acme Corp" → { title, company }.
 * Falls back to raw company field if present, then empty string.
 */
function parseTitle(
  raw: string,
  companyField: string
): { title: string; company: string } {
  const atIdx = raw.lastIndexOf(" at ");
  if (atIdx > 0) {
    return {
      title: raw.slice(0, atIdx).trim(),
      company: raw.slice(atIdx + 4).trim(),
    };
  }
  return { title: raw.trim(), company: companyField.trim() };
}

/** Parse "$120,000 - $180,000" or "$120k - $180k" into annualised USD. */
function parseSalary(
  salaryField: string,
  description: string
): { salary_min: number | null; salary_max: number | null } {
  const src = salaryField || description;
  // Match patterns: $120,000-$180,000 | $120k-$180k | 120000-180000
  const m = src.match(/\$?([\d,]+)\s*k?\s*[-–to]+\s*\$?([\d,]+)\s*k?/i);
  if (!m) return { salary_min: null, salary_max: null };

  const parse = (raw: string, isK: boolean): number => {
    const n = parseInt(raw.replace(/,/g, ""), 10);
    return isK || n < 1_000 ? n * 1_000 : n;
  };

  const rawMin = m[1] ?? "";
  const rawMax = m[2] ?? "";
  const isK = /k/i.test(salaryField || "");

  return {
    salary_min: parse(rawMin, isK),
    salary_max: parse(rawMax, isK),
  };
}

function inferWorkMode(location: string, description: string): WorkMode | null {
  const text = `${location} ${description}`.toLowerCase();
  if (/\bhybrid\b/.test(text)) return "hybrid";
  if (/\bremote\b/.test(text)) return "remote";
  if (/\bon-?site\b|\bin-?office\b/.test(text)) return "onsite";
  return null;
}

function inferLocationLabel(description: string): string {
  if (/\bworldwide\b|\banywhere\b/i.test(description)) return "Worldwide";
  if (/\bremote\b/i.test(description)) return "Remote";
  return "";
}

function inferExperienceYears(text: string): number | null {
  const m = text.match(/(\d+)\+?\s*(?:or more\s+)?years?\s+(?:of\s+)?experience/i);
  return m && m[1] ? parseInt(m[1], 10) : null;
}

function parsePubDate(raw: string): string | null {
  if (!raw) return null;
  try {
    return new Date(raw).toISOString();
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// Shared utilities
// ---------------------------------------------------------------------------

/**
 * Strip HTML tags and decode common entities.
 * Intentionally minimal — avoids a DOM/cheerio dependency.
 */
export function stripHtml(html: string): string {
  return html
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<p[^>]*>/gi, "\n")   // opening <p> → newline (creates split point)
    .replace(/<\/p>/gi, "")
    .replace(/<[^>]+>/g, "")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#x27;/g, "'")
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&#x2F;/gi, "/")
    .replace(/&#x([0-9a-f]{1,6});/gi, (_, hex) =>
      String.fromCodePoint(parseInt(hex, 16))
    )
    .replace(/&nbsp;/g, " ")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

/** SHA-256(text) → first 16 hex chars (matches Python job_id convention). */
export function stableId(text: string): string {
  return createHash("sha256").update(text).digest("hex").slice(0, 16);
}

/** Safely coerce a parsed value to string (fast-xml-parser can return numbers). */
function coerceString(val: unknown): string {
  if (val === null || val === undefined) return "";
  if (typeof val === "string") return val;
  if (typeof val === "number") return String(val);
  // CDATA objects from fast-xml-parser
  if (typeof val === "object" && val !== null && "__cdata" in val) {
    return String((val as Record<string, unknown>)["__cdata"] ?? "");
  }
  return "";
}


