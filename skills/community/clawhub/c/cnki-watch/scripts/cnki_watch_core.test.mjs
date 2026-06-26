import test from "node:test";
import assert from "node:assert/strict";

import {
  appendSeenFingerprints,
  buildCronPrompt,
  fingerprintRecord,
  parseScheduleSpec,
} from "./cnki_watch_core.mjs";

test("parse daily schedule", () => {
  const parsed = parseScheduleSpec("daily@09:15", "Asia/Shanghai");
  assert.equal(parsed.kind, "cron");
  assert.deepEqual(parsed.cliArgs, ["--cron", "15 9 * * *", "--tz", "Asia/Shanghai", "--exact"]);
});

test("parse weekly schedule with chinese weekday", () => {
  const parsed = parseScheduleSpec("weekly@周一@08:30", "Asia/Shanghai");
  assert.deepEqual(parsed.cliArgs, ["--cron", "30 8 * * 1", "--tz", "Asia/Shanghai", "--exact"]);
});

test("parse workday schedule", () => {
  const parsed = parseScheduleSpec("workday@18:00", "Asia/Shanghai");
  assert.deepEqual(parsed.cliArgs, ["--cron", "0 18 * * 1-5", "--tz", "Asia/Shanghai", "--exact"]);
});

test("parse every schedule", () => {
  const parsed = parseScheduleSpec("every:6h");
  assert.deepEqual(parsed.cliArgs, ["--every", "6h"]);
});

test("record fingerprint prefers url or id", () => {
  const first = fingerprintRecord({
    record_id: "",
    title: "Test",
    source: "Journal",
    publish_date: "2026-03-08",
    url: "https://example.com/detail",
  });
  const second = fingerprintRecord({
    record_id: "",
    title: "Test changed",
    source: "Journal",
    publish_date: "2026-03-08",
    url: "https://example.com/detail",
  });
  assert.equal(first, second);
});

test("appendSeenFingerprints preserves newest entries first", () => {
  const result = appendSeenFingerprints(["old-1", "old-2"], ["new-1", "old-1", "new-2"], 4);
  assert.deepEqual(result, ["new-1", "old-1", "new-2", "old-2"]);
});

test("cron prompt contains exact command", () => {
  const prompt = buildCronPrompt("/tmp/cnki-watch", "sub-1");
  assert.match(prompt, /node '\/tmp\/cnki-watch\/scripts\/cnki_watch\.mjs' run-subscription --id 'sub-1' --json/);
});
