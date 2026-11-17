'use strict';

// R12: calendar-extractor ships canary-probe.json, the E3 probe the javis-server
// openclaw release job runs on the canary before flipping the default image.
// Shape contract (spec §4): { prompt: string, timeout_s: int, expect, marker } with
// expect in { "run_ok", "skill_data_rows>=1" }. A skill_data_rows>=1 probe must also
// carry `marker` (a string every probe row's payload contains, so the server's E3
// count and cleanup touch probe rows only, never the owner's real calendar rows)
// and a `{run_id}` placeholder in the prompt (the server fills a fresh id per run,
// so the skill's 30-day `seen` dedup never drops a repeat probe). The server
// rejects anything else, so a bad file here would make E3 fail on every release.

const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');

const PROBE = path.join(__dirname, '..', 'canary-probe.json');
const PKG = path.join(__dirname, '..', 'package.json');
const EXPECTS = new Set(['run_ok', 'skill_data_rows>=1']);

function loadProbe() {
  return JSON.parse(fs.readFileSync(PROBE, 'utf8'));
}

test('R12 canary-probe.json shape: exactly prompt, timeout_s, expect, marker', () => {
  assert.ok(fs.existsSync(PROBE), 'calendar-extractor must ship canary-probe.json');
  const probe = loadProbe();
  assert.deepEqual(Object.keys(probe).sort(), ['expect', 'marker', 'prompt', 'timeout_s']);
  assert.equal(typeof probe.marker, 'string');
  assert.ok(probe.marker.trim().length > 0, 'marker must not be empty');
  assert.equal(typeof probe.prompt, 'string');
  assert.ok(probe.prompt.trim().length > 0, 'prompt must not be empty');
  assert.ok(Number.isInteger(probe.timeout_s), 'timeout_s must be an integer');
  assert.ok(probe.timeout_s > 0 && probe.timeout_s <= 600, 'timeout_s must be 1..600 s');
  assert.ok(EXPECTS.has(probe.expect), `expect must be one of ${[...EXPECTS].join(', ')}`);
});

test('R12 calendar-extractor probe expects a skill_data row', () => {
  assert.equal(loadProbe().expect, 'skill_data_rows>=1');
});

test('F2 probe marker is in the event title, so probe rows (and only they) carry it', () => {
  const { prompt, marker } = loadProbe();
  assert.equal(marker, 'HiJavis canary probe');
  assert.ok(prompt.includes(`"${marker} {run_id}"`), 'the event title must be "<marker> {run_id}"');
});

test('F1 probe title carries {run_id}, so every run is a fresh event past the 30-day seen dedup', () => {
  const { prompt } = loadProbe();
  const { normalizeEvent, dedupKey } = require('../scripts/lib.js');
  const title = (id) => prompt.replace(/\{run_id\}/g, id).match(/titled "([^"]+)"/)[1];
  const ev = (id) => normalizeEvent({ title: title(id), start_at: '2099-06-12T10:00:00-07:00' });
  assert.notEqual(dedupKey(ev('a1b2c3d4')), dedupKey(ev('e5f6a7b8')));
  assert.ok(!prompt.replace(/\{run_id\}/g, 'x').includes('{'), 'no other placeholder');
});

test('R12 probe prompt carries one unambiguous, marked, far-future event', () => {
  const { prompt } = loadProbe();
  // Unique marker title so the server's E3 cleanup can pick out probe rows only.
  assert.match(prompt, /HiJavis canary probe \{run_id\}/);
  // Dispatcher-shaped: an embedded UNIT CONTEXT the skill uses as source of truth.
  assert.match(prompt, /UNIT CONTEXT/);
  assert.match(prompt, /reference_date: \d{4}-\d{2}-\d{2}/);
  assert.match(prompt, /tz: [A-Za-z]+\/[A-Za-z_]+/);
  // Absolute date, so the result never depends on "today". The event is years
  // ahead, outside any "Javis calls you" voice-call arming window.
  const m = prompt.match(/(\d{4})-(\d{2})-(\d{2}) at (\d{1,2}):(\d{2})/);
  assert.ok(m, 'prompt must state an absolute YYYY-MM-DD at HH:MM event time');
  assert.ok(Number(m[1]) >= new Date().getUTCFullYear() + 2, 'event must be far in the future');
});

test('R12 probe file ships in the bundle (no files allowlist excludes it)', () => {
  const pkg = JSON.parse(fs.readFileSync(PKG, 'utf8'));
  if (pkg.files) {
    assert.ok(pkg.files.includes('canary-probe.json'), 'package.json files must list canary-probe.json');
  }
});
