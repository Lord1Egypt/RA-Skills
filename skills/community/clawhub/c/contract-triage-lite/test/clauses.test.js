import { test } from "node:test";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { analyze, segment } from "../scripts/clauses.js";

const DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(DIR, "..");

const NASTY = `1. INTELLECTUAL PROPERTY
All work product and inventions shall be the sole and exclusive property of Client. Contractor hereby irrevocably assigns all rights, title and interest and waives all moral rights.

2. PAYMENT
Client shall pay net 90 days following acceptance.
`;

const CLEAN = `1. PAYMENT
Client shall pay net 15 days of invoice. Late payments accrue 1.5% monthly interest. A 50% deposit is due on signing.
`;

test("segments numbered clauses", () => {
  const clauses = segment(NASTY);
  assert.equal(clauses.length, 2);
  assert.match(clauses[0].heading, /INTELLECTUAL PROPERTY/);
});

test("nasty contract: high flags on ip + payment", () => {
  const r = analyze(NASTY);
  const cats = r.flags.filter((f) => f.severity === "high").map((f) => f.category);
  assert.ok(cats.includes("ip-assignment"));
  assert.ok(cats.includes("payment"));
});

test("clean contract: no high flags", () => {
  const r = analyze(CLEAN);
  assert.equal(r.summary.high, 0);
});

test("missing payment detected", () => {
  const r = analyze("Section 1.\nContractor shall perform services.");
  assert.ok(r.missing.some((m) => m.category === "payment"));
});

test("full-only categories produce upgrade hint", () => {
  const r = analyze(`1. TERMINATION
Either party may terminate this agreement with 30 days written notice.

2. CONFIDENTIALITY
All shared information is confidential and subject to non-disclosure.
`);
  assert.equal(r.upgrade.skill, "contract-triage-nda-msa-riREDACTED-SECRET");
  assert.ok(r.upgrade.reasons.length > 0);
});

test("4-category-only contract has no upgrade field", () => {
  assert.equal(analyze(CLEAN).upgrade, undefined);
});

test("cli: exit 1 on flags", () => {
  try {
    execFileSync("node", ["scripts/clauses.js", "-"], {
      cwd: ROOT,
      input: NASTY,
      encoding: "utf8",
    });
    assert.fail("should have exited 1");
  } catch (e) {
    assert.equal(e.status, 1);
    assert.ok(JSON.parse(e.stdout).summary.high >= 1);
  }
});
