'use strict';

// Behavioral tests for the in-thread card-edit subcommands `update` and
// `anchor` in scripts/calendar-extractor.js. Network-free: doUpdate is exercised
// through an injected client (deps.client.upsert) and an injected input object
// (deps.input), exactly the IO-injection seam doPush uses. The invariants under
// test are the whole point of the feature:
//   - the ORIGINAL dedup_key is sent VERBATIM (never recomputed from the new time);
//   - the item rides status:"confirmed" (server flips pending -> confirmed);
//   - start_at/end_at are naive-local wall-clock (no Z / offset leaves the process);
//   - the FULL merged payload is sent (a time-only patch still carries title/etc.);
//   - missing key -> hard error (no write); empty patch -> no-op (no write).
// And the anchor output shape (the five fields, no `sessions`).
//
// Spec: docs/superpowers/specs/2026-06-22-calendar-extractor-update-anchor-implementation.md

const { test } = require('node:test');
const assert = require('node:assert/strict');

const { doUpdate, doAnchor, resolveUserTz, buildUpdateItem, patchIsEmpty } = require('../scripts/calendar-extractor');
const { dedupKey } = require('../scripts/lib');

const TZ = 'America/Los_Angeles';
const NOW = () => '2026-06-22T12:00:00.000Z';

// A recording skill_data client: captures every upsert(token, items) so a test
// can assert the EXACT item posted, without any network.
function makeClient() {
  const calls = { upsert: [] };
  return {
    calls,
    upsert: async (_token, items) => { calls.upsert.push(items); },
  };
}

// The card's original key, computed at PUSH time off the ORIGINAL start time.
// The edit moves the event to 18:00; if update recomputed the key off 18:00 it
// would differ from this and spawn a second row — the bug this feature fixes.
const ORIGINAL_KEY = '2026-06-22|design review|2026-06-22T22:00:00.000Z';

// ---- verbatim dedup_key (NEVER recomputed) -------------------------------
test('doUpdate sends the ORIGINAL dedup_key verbatim, not recomputed from the new time', async () => {
  const client = makeClient();
  await doUpdate({
    token: 't', client, tz: TZ,
    input: {
      dedup_key: ORIGINAL_KEY,
      patch: {
        title: 'Design Review',
        start_at: '2026-06-22T18:00:00-07:00', // moved 3pm -> 6pm local
        end_at: '2026-06-22T19:00:00-07:00',
        location: 'Zoom', attendees: ['Sam'], notes: 'bring laptop',
      },
    },
  });

  assert.equal(client.calls.upsert.length, 1, 'exactly one upsert');
  const [item] = client.calls.upsert[0];
  assert.equal(item.dedup_key, ORIGINAL_KEY, 'key is passed through verbatim');

  // Prove it was NOT recomputed: dedupKey() off the new 18:00 time would differ.
  const recomputed = dedupKey({ title: 'Design Review', startAt: '2026-06-23T01:00:00.000Z' });
  assert.notEqual(item.dedup_key, recomputed, 'must not be the recomputed (new-time) key');
});

// ---- status:"confirmed" rides the item -----------------------------------
test('doUpdate tags the item status "confirmed" (server flips pending -> confirmed)', async () => {
  const client = makeClient();
  await doUpdate({
    token: 't', client, tz: TZ,
    input: { dedup_key: ORIGINAL_KEY, patch: { title: 'Design Review', location: 'Zoom' } },
  });
  const [item] = client.calls.upsert[0];
  assert.equal(item.status, 'confirmed');
});

// ---- naive-local times (no Z / offset leaves the process) ----------------
test('doUpdate writes start_at/end_at as naive-local wall-clock (no Z, no offset)', async () => {
  const client = makeClient();
  await doUpdate({
    token: 't', client, tz: TZ,
    input: {
      dedup_key: ORIGINAL_KEY,
      patch: {
        title: 'Design Review',
        start_at: '2026-06-22T18:00:00-07:00',
        end_at: '2026-06-22T19:00:00-07:00',
      },
    },
  });
  const [item] = client.calls.upsert[0];
  assert.equal(item.start_at, '2026-06-22T18:00:00', '6pm PDT as zoneless local');
  assert.equal(item.end_at, '2026-06-22T19:00:00');
  // No Z / offset designator on the time fields (the dedup_key legitimately
  // ends in the original instant's `...Z`, so we check the time fields directly,
  // not the whole serialized body).
  assert.doesNotMatch(item.start_at, /[Z+]/, 'start_at carries no Z/offset');
  assert.doesNotMatch(item.end_at, /[Z+]/, 'end_at carries no Z/offset');
});

// ---- FULL merged payload (a time-only edit still carries title/location/etc) --
test('doUpdate sends the full merged payload — a time-only patch keeps title/location/attendees/notes', async () => {
  const client = makeClient();
  // The agent has already merged [CURRENT CARD] fields with the time change, so
  // even a "change time" edit arrives as a full patch. Assert the whole payload
  // is resent (the server overwrites payload wholesale, so omitting blanks them).
  await doUpdate({
    token: 't', client, tz: TZ,
    input: {
      dedup_key: ORIGINAL_KEY,
      patch: {
        title: 'Design Review',
        location: 'Room A',
        attendees: ['Sam', 'Alex'],
        notes: 'bring laptop',
        start_at: '2026-06-22T18:00:00-07:00',
      },
    },
  });
  const [item] = client.calls.upsert[0];
  assert.deepEqual(item.payload, {
    title: 'Design Review',
    location: 'Room A',
    attendees: ['Sam', 'Alex'],
    notes: 'bring laptop',
  });
  assert.equal(item.start_at, '2026-06-22T18:00:00');
});

// ---- lead_time preserved across an in-thread edit ------------------------
// The proactive voice-call lead must survive an edit. The agent merges
// [CURRENT CARD]'s lead_time into the full patch (like title/location); the
// upsert carries it row-level so the server re-schedules the call's fire time.
test('doUpdate carries the patch lead_time onto the upsert item', async () => {
  const client = makeClient();
  await doUpdate({
    token: 't', client, tz: TZ,
    input: {
      dedup_key: ORIGINAL_KEY,
      patch: { title: 'Flight', start_at: '2026-06-22T18:00:00-07:00', lead_time: 60 },
    },
  });
  const [item] = client.calls.upsert[0];
  assert.equal(item.lead_time, 60, 'edited card keeps its (custom) lead time');
  assert.ok(!('lead_time' in item.payload), 'lead_time is row-level, not in payload');
});

test('doUpdate defaults lead_time to 10 when the patch omits it (back-compat for old cards)', async () => {
  const client = makeClient();
  await doUpdate({
    token: 't', client, tz: TZ,
    input: {
      dedup_key: ORIGINAL_KEY,
      patch: { title: 'Design Review', location: 'Zoom' }, // no lead_time
    },
  });
  const [item] = client.calls.upsert[0];
  assert.equal(item.lead_time, 10);
});

test('buildUpdateItem emits a row-level lead_time (default 10, custom passes through)', () => {
  const dflt = buildUpdateItem(ORIGINAL_KEY, { title: 'x' }, TZ);
  assert.equal(dflt.lead_time, 10);
  const custom = buildUpdateItem(ORIGINAL_KEY, { title: 'x', lead_time: 25 }, TZ);
  assert.equal(custom.lead_time, 25);
  const invalid = buildUpdateItem(ORIGINAL_KEY, { title: 'x', lead_time: -3 }, TZ);
  assert.equal(invalid.lead_time, 10, 'invalid lead_time falls back to the default');
});

// A lead_time-only edit ("ring 30 min ahead") is a REAL change, not a no-op.
test('patchIsEmpty treats a lead_time-only patch as a change (writes through)', () => {
  assert.equal(patchIsEmpty({ lead_time: 30 }), false, 'lead_time alone is a meaningful edit');
  assert.equal(patchIsEmpty({ lead_time: 0 }), false, '0 (ring at start) is meaningful');
  assert.equal(patchIsEmpty({}), true);
});

test('doUpdate writes through a lead_time-only patch (not skipped as a no-op)', async () => {
  const client = makeClient();
  await doUpdate({
    token: 't', client, tz: TZ,
    input: { dedup_key: ORIGINAL_KEY, patch: { lead_time: 45 } },
  });
  assert.equal(client.calls.upsert.length, 1, 'lead_time-only edit still writes');
  assert.equal(client.calls.upsert[0][0].lead_time, 45);
});

// ---- end_at omitted -> null (not stale/garbage), and end-only -> start null --
test('doUpdate yields end_at:null when the patch has start_at but no end_at', async () => {
  const client = makeClient();
  await doUpdate({
    token: 't', client, tz: TZ,
    input: {
      dedup_key: ORIGINAL_KEY,
      patch: { title: 'Design Review', start_at: '2026-06-22T18:00:00-07:00' },
    },
  });
  const [item] = client.calls.upsert[0];
  assert.equal(item.start_at, '2026-06-22T18:00:00');
  assert.equal(item.end_at, null, 'omitted end_at collapses to null, not a stale value');
});

test('doUpdate yields start_at:null for an end-only patch', async () => {
  const client = makeClient();
  await doUpdate({
    token: 't', client, tz: TZ,
    input: {
      dedup_key: ORIGINAL_KEY,
      patch: { title: 'Design Review', end_at: '2026-06-22T19:00:00-07:00' },
    },
  });
  const [item] = client.calls.upsert[0];
  assert.equal(item.start_at, null);
  assert.equal(item.end_at, '2026-06-22T19:00:00');
});

// ---- naive-local across DST / Z-collapse ---------------------------------
test('doUpdate collapses a winter (PST -08:00) offset and a Z instant to wall-clock', async () => {
  const client = makeClient();
  await doUpdate({
    token: 't', client, tz: TZ,
    input: {
      dedup_key: ORIGINAL_KEY,
      patch: {
        title: 'Design Review',
        start_at: '2026-01-15T18:00:00-08:00',     // PST winter offset
        end_at: '2026-06-23T01:00:00.000Z',         // Z instant -> 18:00 PDT prev day
      },
    },
  });
  const [item] = client.calls.upsert[0];
  assert.equal(item.start_at, '2026-01-15T18:00:00', 'PST offset collapsed to wall-clock');
  assert.equal(item.end_at, '2026-06-22T18:00:00', 'Z instant collapsed to LA wall-clock');
  assert.doesNotMatch(item.start_at, /[Z+]/);
  assert.doesNotMatch(item.end_at, /[Z+]/);
});

// ---- offset-less unchanged time is NOT re-projected by the runner zone ----
// The [CURRENT CARD] block stores start_at/end_at as naive-local (no offset). On a
// NON-time edit (e.g. "location is Zoom") the agent copies that value forward. It
// must survive byte-identical regardless of the runner process zone — otherwise a
// container running a zone != the card zone silently shifts a time the user never
// touched. (Pinning the patchTimeToNaiveLocal passthrough.)
test('doUpdate passes an offset-less [CURRENT CARD] time through unchanged (no runner-zone shift)', async () => {
  const origTZ = process.env.TZ;
  process.env.TZ = 'America/New_York'; // runner zone != card zone (LA)
  try {
    const client = makeClient();
    await doUpdate({
      // No deps.tz: resolve via stdin tz (the card zone) so this exercises the
      // realistic update path, not a test-injected tz.
      token: 't', client,
      input: {
        dedup_key: ORIGINAL_KEY,
        tz: TZ,
        patch: {
          title: 'Design Review',
          location: 'Zoom',                       // the only real change
          start_at: '2026-06-22T15:00:00',        // unchanged, copied from [CURRENT CARD]
          end_at: '2026-06-22T16:00:00',
        },
      },
    });
    const [item] = client.calls.upsert[0];
    assert.equal(item.start_at, '2026-06-22T15:00:00', 'unchanged naive time is byte-identical');
    assert.equal(item.end_at, '2026-06-22T16:00:00');
    assert.equal(item.payload.location, 'Zoom');
  } finally {
    if (origTZ === undefined) delete process.env.TZ; else process.env.TZ = origTZ;
  }
});

// ---- string fields are trimmed (matches normalizeEvent) ------------------
test('doUpdate trims title/location/notes (no leading/trailing whitespace written)', async () => {
  const client = makeClient();
  await doUpdate({
    token: 't', client, tz: TZ,
    input: {
      dedup_key: ORIGINAL_KEY,
      patch: { title: '  Design Review  ', location: ' Room A ', notes: '  bring laptop  ', start_at: '2026-06-22T18:00:00-07:00' },
    },
  });
  const [item] = client.calls.upsert[0];
  assert.equal(item.payload.title, 'Design Review');
  assert.equal(item.payload.location, 'Room A');
  assert.equal(item.payload.notes, 'bring laptop');
});

// ---- WHOLESALE-PAYLOAD HAZARD: a partial patch blanks the omitted fields --
// The server overwrites payload/start_at/end_at WHOLESALE, so a patch that omits a
// field destroys it on the live row. This is by design (the agent is responsible
// for merging the full state) — pin the destructive behavior so any future change
// to it is caught.
test('doUpdate writes a partial (non-merged) patch as-is — omitted fields are blanked', async () => {
  const client = makeClient();
  await doUpdate({
    token: 't', client, tz: TZ,
    input: { dedup_key: ORIGINAL_KEY, patch: { start_at: '2026-06-22T18:00:00-07:00' } },
  });
  const [item] = client.calls.upsert[0];
  assert.equal(item.dedup_key, ORIGINAL_KEY);
  assert.deepEqual(item.payload, { title: null, location: null, attendees: [], notes: null });
  assert.equal(item.start_at, '2026-06-22T18:00:00');
  assert.equal(item.end_at, null);
});

// ---- non-silent failure: an upsert HTTP error propagates (no false success) --
test('doUpdate propagates a /api/skill/data failure (does not claim success)', async () => {
  const logs = [];
  const origLog = console.log;
  console.log = (...a) => { logs.push(a.join(' ')); };
  try {
    const client = { upsert: async () => { throw new Error('POST /api/skill/data -> HTTP 500'); } };
    await assert.rejects(
      doUpdate({
        token: 't', client, tz: TZ,
        input: { dedup_key: ORIGINAL_KEY, patch: { title: 'Design Review', location: 'Zoom' } },
      }),
      /HTTP 500/
    );
  } finally {
    console.log = origLog;
  }
  assert.ok(!logs.some((l) => /Updated card/.test(l)), 'no success line printed before the throw');
});

// ---- missing key -> hard error, no write ---------------------------------
test('doUpdate throws and writes nothing when dedup_key is missing', async () => {
  const client = makeClient();
  await assert.rejects(
    doUpdate({ token: 't', client, tz: TZ, input: { patch: { title: 'x' } } }),
    /non-empty dedup_key/
  );
  assert.equal(client.calls.upsert.length, 0, 'no write on missing key');
});

test('doUpdate throws and writes nothing when dedup_key is whitespace-only', async () => {
  const client = makeClient();
  await assert.rejects(
    doUpdate({ token: 't', client, tz: TZ, input: { dedup_key: '   ', patch: { title: 'x' } } }),
    /non-empty dedup_key/
  );
  assert.equal(client.calls.upsert.length, 0);
});

// ---- empty patch -> no-op, no write --------------------------------------
test('doUpdate is a no-op (no write) for an empty / whitespace-only patch', async () => {
  const client = makeClient();
  await doUpdate({ token: 't', client, tz: TZ, input: { dedup_key: ORIGINAL_KEY, patch: {} } });
  assert.equal(client.calls.upsert.length, 0, 'empty patch writes nothing');

  await doUpdate({
    token: 't', client, tz: TZ,
    input: { dedup_key: ORIGINAL_KEY, patch: { title: '   ', notes: '', attendees: [] } },
  });
  assert.equal(client.calls.upsert.length, 0, 'whitespace-only patch writes nothing');

  await doUpdate({ token: 't', client, tz: TZ, input: { dedup_key: ORIGINAL_KEY } });
  assert.equal(client.calls.upsert.length, 0, 'missing patch writes nothing');
});

// ---- update does NOT push to iOS -----------------------------------------
test('doUpdate never calls the iOS push path (only the skill_data upsert)', async () => {
  const calls = { upsert: 0, push: 0, mirror: 0 };
  const client = {
    upsert: async () => { calls.upsert++; },
    push: async () => { calls.push++; },
    mirror: async () => { calls.mirror++; },
  };
  await doUpdate({
    token: 't', client, tz: TZ,
    input: { dedup_key: ORIGINAL_KEY, patch: { title: 'Design Review', location: 'Zoom' } },
  });
  assert.equal(calls.upsert, 1);
  assert.equal(calls.push, 0, 'no /api/agent/push from update');
  assert.equal(calls.mirror, 0, 'no pending mirror from update');
});

// ---- anchor output shape (the five fields, no sessions) ------------------
test('doAnchor prints only the anchor (five fields + tz), no sessions', async () => {
  let emitted;
  await doAnchor({ tz: TZ, now: NOW, emit: (o) => { emitted = o; } });
  assert.deepEqual(Object.keys(emitted).sort(), [
    'reference_date', 'reference_time', 'reference_time_utc', 'reference_weekday', 'tz',
  ]);
  assert.equal(emitted.reference_time, '2026-06-22T05:00:00'); // 12:00Z -> 05:00 PDT
  assert.equal(emitted.reference_date, '2026-06-22');
  assert.equal(emitted.reference_weekday, 'Monday');
  assert.equal(emitted.reference_time_utc, NOW());
  assert.equal(emitted.tz, TZ);
  assert.ok(!('sessions' in emitted), 'anchor carries no sessions / transcript');
});

// ---- THE TZ FIX: anchor resolves the user's zone, not the container's UTC ---
// Reproduces the e2e finding: at 01:36 UTC (= 6:36 PM PDT on Jun 22) a BARE
// anchor in a UTC container resolved "today" to Jun 23 and the edit landed a day
// late. With the server's authoritative zone (injected via deps.fetchTz), "today"
// is correctly Jun 22. deps.fetchTz overrides the network call so this is offline.
const EVENING_UTC = () => '2026-06-23T01:36:00.000Z'; // 6:36 PM PDT, Jun 22

test('doAnchor resolves "today" in the SERVER zone, not the container UTC (the off-by-one fix)', async () => {
  let emitted;
  await doAnchor({
    now: EVENING_UTC,                              // no explicit tz on this turn
    fetchTz: async () => 'America/Los_Angeles',    // the server's authoritative zone
    token: 't',
    emit: (o) => { emitted = o; },
  });
  assert.equal(emitted.tz, 'America/Los_Angeles');
  assert.equal(emitted.reference_date, '2026-06-22', '"today" is the LOCAL day, not the UTC day (Jun 23)');
  assert.equal(emitted.reference_time, '2026-06-22T18:36:00');
});

test('doAnchor: an explicit --tz / [CURRENT CARD] zone wins over the server lookup', async () => {
  let emitted; let fetched = 0;
  await doAnchor({
    now: EVENING_UTC, tzFlag: 'America/New_York',
    fetchTz: async () => { fetched++; return 'America/Los_Angeles'; },
    token: 't', emit: (o) => { emitted = o; },
  });
  assert.equal(emitted.tz, 'America/New_York', 'explicit zone wins');
  assert.equal(emitted.reference_date, '2026-06-22'); // 9:36 PM EDT, still Jun 22
  assert.equal(fetched, 0, 'no server lookup when an explicit zone is supplied');
});

test('doAnchor falls back to TZ env when no explicit zone and the server lookup yields nothing', async () => {
  const origTZ = process.env.TZ;
  process.env.TZ = 'UTC';
  try {
    let emitted;
    await doAnchor({
      now: EVENING_UTC, fetchTz: async () => null, token: 't',
      emit: (o) => { emitted = o; },
    });
    assert.equal(emitted.tz, 'UTC');
    assert.equal(emitted.reference_date, '2026-06-23', 'UTC fallback keeps the documented (last-resort) behavior');
  } finally {
    if (origTZ === undefined) delete process.env.TZ; else process.env.TZ = origTZ;
  }
});

// ---- UTC-fallback warning (the "no tz anywhere" gap is loud, not silent) ---
test('resolveUserTz warns to stderr when it falls back to UTC (no tz anywhere)', async () => {
  const origTZ = process.env.TZ; process.env.TZ = 'UTC';
  const errs = []; const origErr = console.error; console.error = (...a) => errs.push(a.join(' '));
  try {
    const tz = await resolveUserTz({ fetchTz: async () => null }); // server has no tz
    assert.equal(tz, 'UTC');
    assert.ok(errs.some((l) => /no user timezone available/.test(l)), 'warns on UTC fallback');
  } finally {
    console.error = origErr;
    if (origTZ === undefined) delete process.env.TZ; else process.env.TZ = origTZ;
  }
});

test('resolveUserTz does NOT warn when a real zone is resolved', async () => {
  const errs = []; const origErr = console.error; console.error = (...a) => errs.push(a.join(' '));
  try {
    const tz = await resolveUserTz({ explicitTz: 'America/Los_Angeles' });
    assert.equal(tz, 'America/Los_Angeles');
    assert.equal(errs.length, 0, 'no warning when a real zone is found');
  } finally {
    console.error = origErr;
  }
});

// ---- update also resolves the server zone when the agent omits stdin tz ----
test('doUpdate uses the SERVER zone when the patch carries no tz (no UTC day-shift)', async () => {
  const client = makeClient();
  await doUpdate({
    token: 't', client,                            // no deps.tz
    fetchTz: async () => 'America/Los_Angeles',     // server zone
    input: {
      dedup_key: ORIGINAL_KEY,                      // no stdin tz
      patch: { title: 'Design Review', start_at: '2026-06-23T03:00:00.000Z' }, // 8pm PDT Jun 22
    },
  });
  const [item] = client.calls.upsert[0];
  assert.equal(item.start_at, '2026-06-22T20:00:00', 'Z instant collapses in the server zone (Jun 22 8pm), not UTC');
  assert.doesNotMatch(item.start_at, /[Z+]/);
});
