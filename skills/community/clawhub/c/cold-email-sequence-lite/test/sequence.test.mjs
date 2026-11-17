import { test } from "node:test";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { build } from "../scripts/sequence.mjs";

const DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(DIR, "..");

const BRIEF = {
  product: "ACME scheduler",
  icp: "clinic managers",
  painPoints: ["no-show appointments"],
  cta: "worth a quick look?",
  senderName: "N",
  company: "ACME",
};

test("full brief: 2 touches, no fails", () => {
  const r = build(BRIEF);
  assert.equal(r.sequence.length, 2);
  assert.equal(r.sequence[0].day, 0);
  assert.equal(r.sequence[1].day, 7);
  assert.equal(r.checks.filter((c) => c.status === "fail").length, 0);
});

test("missing product/icp → fail checks", () => {
  const r = build({});
  assert.ok(r.checks.some((c) => c.id === "product" && c.status === "fail"));
  assert.ok(r.checks.some((c) => c.id === "icp" && c.status === "fail"));
});

test("no painPoints → placeholders + warning", () => {
  const r = build({ product: "x", icp: "y" });
  assert.ok(r.warnings.some((w) => w.includes("painPoint")));
});

test("cli stdin: valid json prints report", () => {
  try {
    const out = execFileSync("node", ["scripts/sequence.mjs", "-"], { cwd: ROOT, input: JSON.stringify(BRIEF), encoding: "utf8" });
    assert.equal(JSON.parse(out).sequence.length, 2);
  } catch (e) {
    assert.equal(e.status, 1); // warnings ok
    assert.equal(JSON.parse(e.stdout).sequence.length, 2);
  }
});
