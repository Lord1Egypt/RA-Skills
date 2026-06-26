#!/usr/bin/env node
/**
 * calendar-extractor — pure logic library (no network, no stdin, no fs).
 *
 * Everything here is deterministic and unit-testable: event normalization,
 * dedup keys, and TTL pruning.
 * The CLI (`calendar-extractor.js`) requires these and stays thin.
 */
'use strict';

const SEEN_TTL_DAYS = 30;

// The "Javis calls you" proactive voice-call engine rings the user at
// `start − lead_time`. Per the design spec (2026-06-24-javis-calls-you-voice-
// calendar-alert-design.md §2/§4B) lead_time is per-event minutes-before-start,
// defaulting to 10 when the extractor doesn't supply one. Kept here so the value
// is normalized in exactly one place (normalizeEvent for fresh events,
// buildUpdateItem for in-thread edits).
const DEFAULT_LEAD_TIME_MINUTES = 10;

// ---- event normalization -------------------------------------------------
function isoOrNull(v) {
  if (!v) return null;
  const d = new Date(v);
  return isNaN(d.getTime()) ? null : d.toISOString();
}

// Coerce a raw lead_time into a non-negative integer count of minutes, falling
// back to DEFAULT_LEAD_TIME_MINUTES (10). Backward-compatible: an absent, null,
// empty, non-numeric, negative, or non-finite value all resolve to the default,
// so events extracted before this field existed keep ringing 10 min ahead.
// Accepts a number or a numeric string (the agent may emit either). Fractions
// are floored (a lead time is whole minutes).
function normalizeLeadTime(raw) {
  if (raw == null) return DEFAULT_LEAD_TIME_MINUTES;
  let n;
  if (typeof raw === 'number') {
    n = raw;
  } else {
    const s = String(raw).trim();
    // Number('') === 0, which would wrongly treat an empty/whitespace string as
    // "ring at start" — guard it so blank input collapses to the default.
    if (s === '') return DEFAULT_LEAD_TIME_MINUTES;
    n = Number(s);
  }
  if (!Number.isFinite(n) || n < 0) return DEFAULT_LEAD_TIME_MINUTES;
  return Math.floor(n);
}

function normalizeEvent(raw) {
  if (!raw || typeof raw !== 'object') return null;
  const title = (raw.title || raw.name || raw.event_name || '').toString().trim();
  if (!title) return null;
  const startAt = isoOrNull(raw.start_at || raw.start_time || raw.start || raw.date);
  const endAt = isoOrNull(raw.end_at || raw.end_time || raw.end);
  const location = (raw.location || raw.address || '').toString().trim() || null;
  const attendees = Array.isArray(raw.attendees)
    ? raw.attendees.map((a) => a.toString().trim()).filter(Boolean)
    : (typeof raw.attendees === 'string' && raw.attendees.trim() ? [raw.attendees.trim()] : []);
  const notes = (raw.notes || raw.description || '').toString().trim() || null;
  const sourceRef = (raw.source_ref || raw.session_id || '').toString().trim() || null;
  const sourceKind = (raw.source_kind || raw.source || '').toString().trim().toLowerCase() || null;
  // Per-event lead time (minutes before start) for the proactive voice call;
  // defaults to 10 so pre-existing events without the field are unchanged.
  const leadTime = normalizeLeadTime(raw.lead_time);
  return { title, startAt, endAt, location, attendees, notes, sourceRef, sourceKind, leadTime };
}

function dedupKey(ev) {
  const day = ev.startAt ? ev.startAt.slice(0, 10) : 'nodate';
  const title = ev.title.toLowerCase().replace(/\s+/g, ' ').trim();
  return `${day}|${title}|${ev.startAt || ''}`.slice(0, 512);
}

// ---- naive-local wall-clock for skill_data -------------------------------
// iOS (Sources/JavisApp/utils/ServerDate.swift) reads calendar start_at/end_at
// as NAIVE LOCAL wall-clock in the device timezone — a zoneless string is
// interpreted in TimeZone.current. So we must store the wall-clock of the
// instant in `tz` WITHOUT a zone designator (no Z); a UTC `Z` instant would be
// re-read as device-local and shift by the tz offset. Example:
//   2026-06-06T04:00:00.000Z @ America/Los_Angeles -> "2026-06-05T21:00:00".
function toNaiveLocal(iso, tz) {
  if (!iso) return null;
  const d = new Date(iso);
  if (isNaN(d.getTime())) return null;
  const p = new Intl.DateTimeFormat('en-CA', {
    timeZone: tz, hour12: false,
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
  }).formatToParts(d).reduce((o, x) => ((o[x.type] = x.value), o), {});
  let { year, month, day, hour } = p;
  // Node/V8 emits "00" at local midnight, but some ICU builds emit "24:00",
  // meaning the END of this calendar day (= start of the next). Normalize to
  // "00" AND roll the date forward a day, else the result is off by a full day.
  if (hour === '24') {
    hour = '00';
    const next = new Date(Date.UTC(+year, +month - 1, +day) + 86400000);
    year = String(next.getUTCFullYear()).padStart(4, '0');
    month = String(next.getUTCMonth() + 1).padStart(2, '0');
    day = String(next.getUTCDate()).padStart(2, '0');
  }
  return `${year}-${month}-${day}T${hour}:${p.minute}:${p.second}`;
}

// Build the relative-date anchor handed to the LLM. The instant `iso` is the
// real now; what the LLM needs is the LOCAL wall-clock in `tz`, because a UTC
// `Z` instant's date can already be the NEXT day in the evening west of UTC
// (9:11 PM PDT on Jun 4 == 2026-06-05T04:11Z). Anchoring "today" on that Z
// string makes the model resolve every event one day late. So we hand it the
// zoneless local wall-clock plus the explicit local date and weekday, and keep
// the raw instant under reference_time_utc for transparency.
function localAnchor(iso, tz) {
  const local = toNaiveLocal(iso, tz); // "2026-06-04T21:11:00" — no zone
  const d = new Date(iso);
  const weekday = isNaN(d.getTime())
    ? null
    : new Intl.DateTimeFormat('en-US', { timeZone: tz, weekday: 'long' }).format(d);
  return {
    reference_time: local,                       // local wall-clock; the LLM's "now"
    reference_date: local ? local.slice(0, 10) : null, // "today" == this date in tz
    reference_weekday: weekday,                   // anchors "Saturday"/"next Thursday"
    reference_time_utc: iso,                       // the true instant, for reference
  };
}

// Build the POST /api/skill/data items array. dedup_key stays instant-based
// (stable identity, unchanged by this fix); start_at/end_at are naive-local so
// the iOS calendar table renders the same local time as the push digest.
//
// Every mirrored event is tagged status:"pending" (Flow 3): the server stores it
// pending and the iOS calendar table renders it greyed/dashed with Confirm/Discard.
// A pending row becomes solid only when the user taps Confirm; Discard deletes it.
//
// lead_time (minutes before start, default 10) rides each item top-level so the
// server's CalendarVoiceCallSource can compute the proactive call's fire time
// (`fire = start − lead_time`). It sits alongside start_at/status/source_ref —
// the row-level fields the server consumes — NOT inside `payload` (which the
// server overwrites wholesale on edit and the iOS table renders). The detail
// fields the server's Details command speaks (location, notes, attendees) are
// already carried in `payload`; they are the announcement context.
function buildSkillDataItems(events, tz) {
  return (events || []).slice(0, 500).map((ev) => ({
    dedup_key: dedupKey(ev),
    payload: { title: ev.title, location: ev.location, attendees: ev.attendees, notes: ev.notes },
    start_at: toNaiveLocal(ev.startAt, tz),
    end_at: toNaiveLocal(ev.endAt, tz),
    lead_time: normalizeLeadTime(ev.leadTime),
    source_ref: ev.sourceRef,
    status: 'pending',
  }));
}

// ---- TTL pruning ---------------------------------------------------------
// Generic pruner for any { key: <something-with-a-timestamp> } map. `tsOf`
// extracts the ISO timestamp from each value; entries older than the 30-day
// cutoff (or with an unparseable ts) are dropped.
function pruneByTtl(map, tsOf, ttlDays) {
  const days = ttlDays == null ? SEEN_TTL_DAYS : ttlDays;
  const cutoff = Date.now() - days * 86400 * 1000;
  const out = {};
  for (const [k, v] of Object.entries(map || {})) {
    const t = Date.parse(tsOf(v));
    if (!isNaN(t) && t >= cutoff) out[k] = v;
  }
  return out;
}

// `seen` is a { key: isoTimestamp } map — the value IS the timestamp.
function pruneSeen(seen, ttlDays) {
  return pruneByTtl(seen, (iso) => iso, ttlDays);
}

module.exports = {
  SEEN_TTL_DAYS,
  DEFAULT_LEAD_TIME_MINUTES,
  isoOrNull,
  normalizeLeadTime,
  normalizeEvent,
  dedupKey,
  toNaiveLocal,
  localAnchor,
  buildSkillDataItems,
  pruneByTtl,
  pruneSeen,
};
