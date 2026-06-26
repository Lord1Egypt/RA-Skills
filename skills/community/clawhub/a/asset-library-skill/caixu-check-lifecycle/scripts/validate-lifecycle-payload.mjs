#!/usr/bin/env node

import { readFileSync } from "node:fs";

function fail(message) {
  console.error(message);
  process.exit(1);
}

const filePath = process.argv[2];
if (!filePath) {
  fail("Usage: node validate-lifecycle-payload.mjs <payload.json>");
}

const payload = JSON.parse(readFileSync(filePath, "utf8"));

if (!payload || typeof payload !== "object") {
  fail("Payload must be an object.");
}

for (const key of [
  "library_id",
  "as_of_date",
  "window_days",
  "lifecycle_events",
  "rule_matches",
  "missing_items",
  "readiness"
]) {
  if (!(key in payload)) {
    fail(`Missing required key: ${key}`);
  }
}

if (!/^\d{4}-\d{2}-\d{2}$/.test(String(payload.as_of_date))) {
  fail("as_of_date must be YYYY-MM-DD.");
}

if (typeof payload.window_days !== "number" || payload.window_days <= 0) {
  fail("window_days must be a positive number.");
}

const readiness = payload.readiness;
if (!readiness || typeof readiness !== "object") {
  fail("readiness must be an object.");
}

if (typeof readiness.ready_for_submission !== "boolean") {
  fail("readiness.ready_for_submission must be boolean.");
}

console.log(JSON.stringify({ ok: true }));
