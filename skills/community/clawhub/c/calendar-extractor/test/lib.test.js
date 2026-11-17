'use strict';

const { test } = require('node:test');
const assert = require('node:assert/strict');

const {
  SEEN_TTL_DAYS,
  DEFAULT_LEAD_TIME_MINUTES,
  isoOrNull,
  normalizeLeadTime,
  normalizeEvent,
  dedupKey,
  toNaiveLocal,
  zonelessLocalToUtcIso,
  buildSkillDataItems,
  pruneSeen,
} = require('../scripts/lib');

// ---- isoOrNull -----------------------------------------------------------
test('isoOrNull returns null for falsy / unparseable, ISO for valid', () => {
  assert.equal(isoOrNull(null), null);
  assert.equal(isoOrNull(''), null);
  assert.equal(isoOrNull('not a date'), null);
  assert.equal(isoOrNull('2026-06-03T10:00:00Z'), '2026-06-03T10:00:00.000Z');
});

// ---- normalizeEvent ------------------------------------------------------
test('normalizeEvent rejects non-objects and title-less input', () => {
  assert.equal(normalizeEvent(null), null);
  assert.equal(normalizeEvent('x'), null);
  assert.equal(normalizeEvent({}), null);
  assert.equal(normalizeEvent({ title: '   ' }), null);
});

test('normalizeEvent reads title/name/event_name aliases', () => {
  assert.equal(normalizeEvent({ name: 'Standup' }).title, 'Standup');
  assert.equal(normalizeEvent({ event_name: 'Demo' }).title, 'Demo');
  assert.equal(normalizeEvent({ title: '  Sync  ' }).title, 'Sync');
});

test('normalizeEvent coerces attendees (array, string, missing)', () => {
  assert.deepEqual(normalizeEvent({ title: 'a', attendees: ['  X ', '', 'Y'] }).attendees, ['X', 'Y']);
  assert.deepEqual(normalizeEvent({ title: 'a', attendees: ' solo ' }).attendees, ['solo']);
  assert.deepEqual(normalizeEvent({ title: 'a' }).attendees, []);
});

test('normalizeEvent maps date/location/notes aliases and nulls', () => {
  const ev = normalizeEvent({
    title: 'Lunch',
    date: '2026-06-04T12:00:00Z',
    address: 'Cafe',
    description: 'bring slides',
  });
  assert.equal(ev.startAt, '2026-06-04T12:00:00.000Z');
  assert.equal(ev.location, 'Cafe');
  assert.equal(ev.notes, 'bring slides');
  assert.equal(ev.endAt, null);

  const bare = normalizeEvent({ title: 'x' });
  assert.equal(bare.location, null);
  assert.equal(bare.notes, null);
  assert.equal(bare.startAt, null);
});

test('normalizeEvent carries source_ref and source_kind', () => {
  const a = normalizeEvent({ title: 'x', session_id: 'sid-1', source: 'AUDIO' });
  assert.equal(a.sourceRef, 'sid-1');
  assert.equal(a.sourceKind, 'audio');

  const k = normalizeEvent({ title: 'x', source_ref: 'kb-9', source_kind: 'keyboard' });
  assert.equal(k.sourceRef, 'kb-9');
  assert.equal(k.sourceKind, 'keyboard');

  const none = normalizeEvent({ title: 'x' });
  assert.equal(none.sourceRef, null);
  assert.equal(none.sourceKind, null);
});

// ---- normalizeLeadTime ---------------------------------------------------
// The "Javis calls you" engine rings at `start − lead_time`. lead_time is
// per-event minutes-before-start, default 10, and must be backward-compatible:
// any absent/invalid value collapses to the default so pre-existing events
// (extracted before the field existed) still ring 10 min ahead.
test('normalizeLeadTime defaults to 10 for absent/empty/null', () => {
  assert.equal(DEFAULT_LEAD_TIME_MINUTES, 10);
  assert.equal(normalizeLeadTime(undefined), 10);
  assert.equal(normalizeLeadTime(null), 10);
  assert.equal(normalizeLeadTime(''), 10);
  assert.equal(normalizeLeadTime('   '), 10);  // whitespace-only -> NaN -> default
});

test('normalizeLeadTime accepts numbers and numeric strings, floors fractions', () => {
  assert.equal(normalizeLeadTime(15), 15);
  assert.equal(normalizeLeadTime('20'), 20);
  assert.equal(normalizeLeadTime('  5  '), 5);
  assert.equal(normalizeLeadTime(12.9), 12);   // whole minutes only
  assert.equal(normalizeLeadTime(0), 0);        // 0 is valid — ring at start
});

test('normalizeLeadTime rejects negative/non-finite, falling back to the default', () => {
  assert.equal(normalizeLeadTime(-5), 10);
  assert.equal(normalizeLeadTime('-1'), 10);
  assert.equal(normalizeLeadTime(NaN), 10);
  assert.equal(normalizeLeadTime(Infinity), 10);
  assert.equal(normalizeLeadTime('abc'), 10);
});

test('normalizeEvent reads lead_time (default 10) onto the event', () => {
  assert.equal(normalizeEvent({ title: 'x' }).leadTime, 10);          // absent -> default
  assert.equal(normalizeEvent({ title: 'x', lead_time: 15 }).leadTime, 15);
  assert.equal(normalizeEvent({ title: 'x', lead_time: '30' }).leadTime, 30);
  assert.equal(normalizeEvent({ title: 'x', lead_time: 0 }).leadTime, 0);
  assert.equal(normalizeEvent({ title: 'x', lead_time: -4 }).leadTime, 10); // invalid -> default
});

// ---- dedupKey ------------------------------------------------------------
test('dedupKey is stable for equivalent events', () => {
  const a = normalizeEvent({ title: 'Team  Sync', start_at: '2026-06-03T17:00:00Z' });
  const b = normalizeEvent({ name: 'team sync', start: '2026-06-03T17:00:00Z' });
  assert.equal(dedupKey(a), dedupKey(b));
});

test('dedupKey differs by day, title, and start time', () => {
  const base = normalizeEvent({ title: 'Sync', start_at: '2026-06-03T17:00:00Z' });
  const otherTitle = normalizeEvent({ title: 'Standup', start_at: '2026-06-03T17:00:00Z' });
  const otherTime = normalizeEvent({ title: 'Sync', start_at: '2026-06-03T18:00:00Z' });
  const noDate = normalizeEvent({ title: 'Sync' });
  assert.notEqual(dedupKey(base), dedupKey(otherTitle));
  assert.notEqual(dedupKey(base), dedupKey(otherTime));
  assert.ok(dedupKey(noDate).startsWith('nodate|'));
});

// ---- toNaiveLocal / buildSkillDataItems (naive-local mirror) -------------
test('toNaiveLocal renders the instant as naive wall-clock in tz (no Z)', () => {
  // 04:00Z Jun 6 == 21:00 Jun 5 in Los Angeles (PDT, -7).
  assert.equal(toNaiveLocal('2026-06-06T04:00:00.000Z', 'America/Los_Angeles'), '2026-06-05T21:00:00');
  // Same instant in New York (EDT, -4) == 00:00 Jun 6.
  assert.equal(toNaiveLocal('2026-06-06T04:00:00.000Z', 'America/New_York'), '2026-06-06T00:00:00');
  // No Z / offset designator on the output.
  assert.doesNotMatch(toNaiveLocal('2026-06-06T04:00:00.000Z', 'America/Los_Angeles'), /[Z+]/);
  assert.equal(toNaiveLocal(null, 'America/Los_Angeles'), null);
  assert.equal(toNaiveLocal('not-a-date', 'America/Los_Angeles'), null);
});

// ---- zonelessLocalToUtcIso (absolute-instant conversion) -----------------
// Per 2026-07-24-calendar-absolute-instant-timezone-design.md §B: a ZONELESS
// wall-clock is interpreted in `tz` (NOT the process/container TZ) and returned
// as the corresponding UTC instant with Z; a zoned input keeps its instant.
test('zonelessLocalToUtcIso interprets a zoneless wall-clock in tz, independent of process.env.TZ', () => {
  const savedTz = process.env.TZ;
  // Pin the process TZ to the buggy container zone. The OLD `new Date(zoneless)`
  // path would read "7pm" as 7pm PDT here; the helper must ignore process TZ and
  // read it as 7pm Asia/Shanghai (UTC+8) -> 11:00Z.
  process.env.TZ = 'America/Los_Angeles';
  try {
    assert.equal(zonelessLocalToUtcIso('2026-07-24T19:00:00', 'Asia/Shanghai'), '2026-07-24T11:00:00Z');
    assert.equal(zonelessLocalToUtcIso('2026-07-24T20:00:00', 'Asia/Shanghai'), '2026-07-24T12:00:00Z');
    // A space-separated wall-clock is accepted too.
    assert.equal(zonelessLocalToUtcIso('2026-01-15 09:00:00', 'America/Los_Angeles'), '2026-01-15T17:00:00Z'); // PST -8
    assert.equal(zonelessLocalToUtcIso('2026-07-15T09:00:00', 'America/Los_Angeles'), '2026-07-15T16:00:00Z'); // PDT -7
  } finally {
    if (savedTz === undefined) delete process.env.TZ; else process.env.TZ = savedTz;
  }
});

test('zonelessLocalToUtcIso keeps the instant of an already-zoned input (Z or offset)', () => {
  // Z input -> same instant, normalized to second-precision Z.
  assert.equal(zonelessLocalToUtcIso('2026-06-06T04:00:00Z', 'America/Los_Angeles'), '2026-06-06T04:00:00Z');
  assert.equal(zonelessLocalToUtcIso('2026-06-06T04:00:00.000Z', 'America/New_York'), '2026-06-06T04:00:00Z');
  // A ±HH:MM offset is a real instant regardless of tz: 19:00+08:00 == 11:00Z.
  assert.equal(zonelessLocalToUtcIso('2026-07-24T19:00:00+08:00', 'America/Los_Angeles'), '2026-07-24T11:00:00Z');
  // Falsy / unparseable -> null (matches toNaiveLocal's contract).
  assert.equal(zonelessLocalToUtcIso(null, 'Asia/Shanghai'), null);
  assert.equal(zonelessLocalToUtcIso('not-a-date', 'Asia/Shanghai'), null);
});

// The canonical bicycle repro (spec "Canonical acceptance test case"): a user in
// Asia/Shanghai types "July 24 7-8pm". The extractor must emit the correct
// absolute instant 11:00Z/12:00Z REGARDLESS of the container TZ — proving the
// container-tz bug is gone. ev.startAt/endAt are the LLM's zoneless wall-clock.
test('buildSkillDataItems emits the correct UTC instant for a zoneless event, independent of container TZ', () => {
  const savedTz = process.env.TZ;
  process.env.TZ = 'America/Los_Angeles'; // pin the buggy container zone
  try {
    const ev = {
      title: 'bring son to ride bicycle',
      startAt: '2026-07-24T19:00:00', endAt: '2026-07-24T20:00:00', // zoneless, LLM local wall-clock
      location: null, attendees: [], notes: null, sourceRef: 'sid-1', sourceKind: 'keyboard', leadTime: 10,
    };
    const [item] = buildSkillDataItems([ev], 'Asia/Shanghai');
    assert.equal(item.start_at, '2026-07-24T11:00:00Z'); // 7pm Shanghai == 11:00Z, not 7pm PDT
    assert.equal(item.end_at, '2026-07-24T12:00:00Z');
    assert.match(item.start_at, /Z$/);
  } finally {
    if (savedTz === undefined) delete process.env.TZ; else process.env.TZ = savedTz;
  }
});

test('buildSkillDataItems emits absolute-instant (Z) start/end and instant-based dedup_key', () => {
  const ev = normalizeEvent({
    title: 'Meeting', start_at: '2026-06-06T04:00:00Z', end_at: '2026-06-06T04:30:00Z',
    source_ref: '521', source_kind: 'keyboard',
  });
  const [item] = buildSkillDataItems([ev], 'America/Los_Angeles');
  // Absolute-instant semantics: a zoned input keeps its instant, serialized as
  // UTC ISO with Z (the server marks is_utc and iOS renders it device-local).
  assert.equal(item.start_at, '2026-06-06T04:00:00Z');
  assert.equal(item.end_at, '2026-06-06T04:30:00Z');
  assert.match(item.start_at, /Z$/);
  assert.equal(item.dedup_key, dedupKey(ev));          // dedup identity unchanged
  assert.equal(item.source_ref, '521');
  assert.equal(item.status, 'pending');                // Flow 3: written pending, confirm-to-solid
  assert.equal(item.lead_time, 10);                    // default voice-call lead
  assert.deepEqual(item.payload, { title: 'Meeting', location: null, attendees: [], notes: null });
});

// ---- lead_time emission (proactive voice-call fire time) ------------------
test('buildSkillDataItems emits lead_time top-level (default 10, carried per-event)', () => {
  const dflt = normalizeEvent({ title: 'Standup', start_at: '2026-06-06T17:00:00Z' });
  const custom = normalizeEvent({ title: 'Flight', start_at: '2026-06-06T15:00:00Z', lead_time: 60 });
  const [a, b] = buildSkillDataItems([dflt, custom], 'America/Los_Angeles');
  // Top-level row field (server reads it to compute fire = start − lead_time),
  // NOT inside payload (which the server overwrites wholesale + iOS renders).
  assert.equal(a.lead_time, 10);
  assert.equal(b.lead_time, 60);
  assert.ok(!('lead_time' in a.payload), 'lead_time is row-level, not in payload');
});

test('buildSkillDataItems carries the detail fields (location/attendees/notes) into payload', () => {
  // These feed the server adapter's Details announcement context (spec §4B/§5).
  const ev = normalizeEvent({
    title: 'Design Review', start_at: '2026-06-06T22:00:00Z',
    location: 'Zoom', attendees: ['Sam', 'Alex'], notes: 'bring laptop',
  });
  const [item] = buildSkillDataItems([ev], 'America/Los_Angeles');
  assert.deepEqual(item.payload, {
    title: 'Design Review', location: 'Zoom', attendees: ['Sam', 'Alex'], notes: 'bring laptop',
  });
});

test('buildSkillDataItems tags every event status "pending" (Flow 3)', () => {
  const events = [
    normalizeEvent({ title: 'A', start_at: '2026-06-06T04:00:00Z' }),
    normalizeEvent({ title: 'B' }),                       // no start_at
    normalizeEvent({ title: 'C', start_at: '2026-06-07T15:00:00Z' }),
  ];
  const items = buildSkillDataItems(events, 'America/Los_Angeles');
  assert.equal(items.length, 3);
  for (const item of items) assert.equal(item.status, 'pending');
});

test('buildSkillDataItems preserves null start/end and tolerates empty input', () => {
  const ev = normalizeEvent({ title: 'TBD' }); // no start_at
  const [item] = buildSkillDataItems([ev], 'America/Los_Angeles');
  assert.equal(item.start_at, null);
  assert.equal(item.end_at, null);
  assert.deepEqual(buildSkillDataItems(null, 'America/Los_Angeles'), []);
  assert.deepEqual(buildSkillDataItems([], 'America/Los_Angeles'), []);
});

// ---- pruning by TTL ------------------------------------------------------
test('pruneSeen drops entries older than TTL and unparseable ones', () => {
  const now = Date.now();
  const fresh = new Date(now - 1 * 86400 * 1000).toISOString();
  const stale = new Date(now - (SEEN_TTL_DAYS + 1) * 86400 * 1000).toISOString();
  const seen = { keep: fresh, drop: stale, bad: 'not-a-date' };
  const out = pruneSeen(seen);
  assert.deepEqual(Object.keys(out), ['keep']);
  assert.equal(out.keep, fresh);
});

test('pruneSeen on empty / missing map yields {}', () => {
  assert.deepEqual(pruneSeen(null), {});
  assert.deepEqual(pruneSeen({}), {});
});

test('prune honors a custom ttlDays', () => {
  const now = Date.now();
  const tenDaysAgo = new Date(now - 10 * 86400 * 1000).toISOString();
  // With a 5-day TTL the 10-day-old entry is stale.
  assert.deepEqual(pruneSeen({ k: tenDaysAgo }, 5), {});
  // With a 30-day TTL it survives.
  assert.deepEqual(Object.keys(pruneSeen({ k: tenDaysAgo }, 30)), ['k']);
});
