// Tests for focus-finder (assistant-written). Run: node --test skills/focus-finder/*.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { DEFAULTS, findGaps, formatMinutes, todayIn, toBusyIntervals } from "./focus-finder.mjs";

const SCRIPT = fileURLToPath(new URL("./focus-finder.mjs", import.meta.url));
const FIXTURE = fileURLToPath(new URL("./fixtures/sample-events.json", import.meta.url));
const TZ = "America/Los_Angeles";
const h = (hh, mm = 0) => hh * 60 + mm;
const gap = (s, e) => ({ start: s, end: e, minutes: e - s });

// ---- findGaps (student-written) ----

test("findGaps: empty day is one 09:00-18:00 gap", () => {
  assert.deepEqual(findGaps([], DEFAULTS), [gap(h(9), h(18))]);
});

test("findGaps: overlapping and nested events merge", () => {
  const busy = [{ start: h(10), end: h(11) }, { start: h(10, 30), end: h(10, 45) }, { start: h(10, 50), end: h(12) }];
  assert.deepEqual(findGaps(busy, DEFAULTS), [gap(h(9), h(10)), gap(h(12), h(18))]);
});

test("findGaps: touching events leave no gap between them", () => {
  const busy = [{ start: h(10), end: h(11) }, { start: h(11), end: h(12) }];
  assert.deepEqual(findGaps(busy, DEFAULTS), [gap(h(9), h(10)), gap(h(12), h(18))]);
});

test("findGaps: events outside or across the window are clipped", () => {
  const busy = [{ start: h(7), end: h(9, 30) }, { start: h(17, 30), end: h(20) }, { start: h(5), end: h(6) }];
  assert.deepEqual(findGaps(busy, DEFAULTS), [gap(h(9, 30), h(17, 30))]);
});

test("findGaps: 45 minutes kept, 44 dropped", () => {
  const busy = [{ start: h(9, 45), end: h(10) }, { start: h(10, 44), end: h(18) }];
  assert.deepEqual(findGaps(busy, DEFAULTS), [gap(h(9), h(9, 45))]);
});

test("findGaps: unsorted input, input not mutated", () => {
  const busy = [{ start: h(15), end: h(16) }, { start: h(9), end: h(10) }];
  const copy = structuredClone(busy);
  assert.deepEqual(findGaps(busy, DEFAULTS), [gap(h(10), h(15)), gap(h(16), h(18))]);
  assert.deepEqual(busy, copy);
});

test("findGaps: fully booked day returns nothing", () => {
  assert.deepEqual(findGaps([{ start: h(8), end: h(19) }], DEFAULTS), []);
});

// ---- toBusyIntervals ----

const ev = (start, end, extra = {}) => ({ start: { dateTime: start }, end: { dateTime: end }, ...extra });

test("toBusyIntervals: Pacific offset and UTC both become LA wall-clock minutes", () => {
  const raw = [ev("2026-11-16T10:00:00-08:00", "2026-11-16T11:00:00-08:00"), ev("2026-11-16T20:00:00Z", "2026-11-16T21:00:00Z")];
  assert.deepEqual(toBusyIntervals(raw, "2026-11-16", TZ), [{ start: h(10), end: h(11) }, { start: h(12), end: h(13) }]);
});

test("toBusyIntervals: daylight time (PDT, UTC-7) handled", () => {
  const raw = [ev("2026-07-01T16:00:00Z", "2026-07-01T17:00:00Z")];
  assert.deepEqual(toBusyIntervals(raw, "2026-07-01", TZ), [{ start: h(9), end: h(10) }]);
});

test("toBusyIntervals: all-day, cancelled and free events ignored", () => {
  const raw = [
    { start: { date: "2026-11-16" }, end: { date: "2026-11-17" } },
    ev("2026-11-16T10:00:00-08:00", "2026-11-16T11:00:00-08:00", { status: "cancelled" }),
    ev("2026-11-16T12:00:00-08:00", "2026-11-16T13:00:00-08:00", { transparency: "transparent" }),
    { start: "2026-11-16", end: "2026-11-17" },
  ];
  assert.deepEqual(toBusyIntervals(raw, "2026-11-16", TZ), []);
});

test("toBusyIntervals: events on other days dropped, midnight-crossing clipped", () => {
  const raw = [
    ev("2026-11-15T10:00:00-08:00", "2026-11-15T11:00:00-08:00"),
    ev("2026-11-15T23:00:00-08:00", "2026-11-16T09:30:00-08:00"),
    ev("2026-11-16T22:00:00-08:00", "2026-11-17T02:00:00-08:00"),
    ev("2026-11-15T22:00:00-08:00", "2026-11-16T00:00:00-08:00"),
  ];
  assert.deepEqual(toBusyIntervals(raw, "2026-11-16", TZ), [{ start: 0, end: h(9, 30) }, { start: h(22), end: 24 * 60 }]);
});

test("toBusyIntervals: dateTime without offset is LA wall-clock, plain ISO strings accepted", () => {
  const raw = [{ start: "2026-11-16T14:00:00", end: "2026-11-16T15:00:00" }];
  assert.deepEqual(toBusyIntervals(raw, "2026-11-16", TZ), [{ start: h(14), end: h(15) }]);
});

test("toBusyIntervals: accepts array, {events}, {items}; junk gives []", () => {
  const one = [ev("2026-11-16T10:00:00-08:00", "2026-11-16T11:00:00-08:00")];
  const want = [{ start: h(10), end: h(11) }];
  assert.deepEqual(toBusyIntervals(one, "2026-11-16", TZ), want);
  assert.deepEqual(toBusyIntervals({ events: one }, "2026-11-16", TZ), want);
  assert.deepEqual(toBusyIntervals({ items: one }, "2026-11-16", TZ), want);
  for (const junk of [null, 42, "x", {}, { events: "no" }]) assert.deepEqual(toBusyIntervals(junk, "2026-11-16", TZ), []);
});

test("toBusyIntervals: malformed events skipped without crashing", () => {
  const raw = [null, 7, {}, { start: {} , end: {} }, ev("not a date+00:00", "2026-11-16T11:00:00Z"),
    ev("2026-11-16T11:00:00-08:00", "2026-11-16T10:00:00-08:00"), { start: { dateTime: 5 }, end: { dateTime: 6 } }];
  assert.deepEqual(toBusyIntervals(raw, "2026-11-16", TZ), []);
});

// ---- helpers ----

test("formatMinutes pads and handles end of day", () => {
  assert.equal(formatMinutes(h(9)), "09:00");
  assert.equal(formatMinutes(h(17, 5)), "17:05");
  assert.equal(formatMinutes(24 * 60), "24:00");
});

test("todayIn uses the LA date, not UTC", () => {
  assert.equal(todayIn(TZ, new Date("2026-11-17T05:00:00Z")), "2026-11-16");
});

// ---- CLI ----

const run = (args, input) => spawnSync(process.execPath, [SCRIPT, ...args], { input, encoding: "utf8" });

test("CLI: fixture gives the expected gaps (text)", () => {
  const r = run(["--date", "2026-11-16"], readFileSync(FIXTURE, "utf8"));
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /^Focus blocks on 2026-11-16/);
  assert.match(r.stdout, /13:00–14:45 \(105 min\)/);
  assert.match(r.stdout, /15:00–18:00 \(180 min\)/);
  assert.doesNotMatch(r.stdout, /09:30–10:00/); // 30 min, below 45
  assert.doesNotMatch(r.stdout, /synthetic|Lunch|Holiday/i); // never prints titles
});

test("CLI: --json output and --min", () => {
  const r = run(["--date", "2026-11-16", "--json", "--min", "30"], readFileSync(FIXTURE, "utf8"));
  assert.equal(r.status, 0, r.stderr);
  assert.deepEqual(JSON.parse(r.stdout), {
    date: "2026-11-16", timeZone: TZ, minMinutes: 30,
    gaps: [
      { start: "09:30", end: "10:00", minutes: 30 },
      { start: "11:30", end: "12:00", minutes: 30 },
      { start: "13:00", end: "14:45", minutes: 105 },
      { start: "15:00", end: "18:00", minutes: 180 },
    ],
  });
});

test("CLI: no gaps prints a clear message", () => {
  const r = run(["--date", "2026-11-16"], JSON.stringify([ev("2026-11-16T08:00:00-08:00", "2026-11-16T19:00:00-08:00")]));
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /No focus blocks of 45\+ minutes/);
});

for (const [name, args, input] of [
  ["invalid JSON", [], "nope"],
  ["bad --date", ["--date", "16/11/2026"], "[]"],
  ["impossible --date", ["--date", "2026-13-40"], "[]"],
  ["bad --min", ["--min", "abc"], "[]"],
  ["--min zero", ["--min", "0"], "[]"],
  ["unknown flag", ["--write"], "[]"],
  ["positional arg", ["extra"], "[]"],
]) {
  test(`CLI: ${name} exits 2`, () => {
    const r = run(args, input);
    assert.equal(r.status, 2);
    assert.match(r.stderr, /^focus-finder: /);
  });
}
