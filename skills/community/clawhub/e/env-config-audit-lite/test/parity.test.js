import { test } from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promises as fs } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT = fileURLToPath(new URL("../scripts/parity.js", import.meta.url));
const run = (args) =>
  new Promise((resolve) => {
    execFile(process.execPath, [SCRIPT, ...args], (err, stdout) =>
      resolve({ code: err?.code ?? 0, stdout }),
    );
  });
const pair = async (env, ex) => {
  const d = await fs.mkdtemp(path.join(os.tmpdir(), "env-lite-"));
  const a = path.join(d, ".env"), b = path.join(d, ".env.example");
  await fs.writeFile(a, env); await fs.writeFile(b, ex);
  return [a, b];
};

test("reports missing, extra and empty keys without values", async () => {
  const [a, b] = await pair("A=1\nB=\nEXTRA=x\n", "A=\nB=\nMISSING=\n");
  const { code, stdout } = await run([a, b]);
  assert.equal(code, 1);
  const r = JSON.parse(stdout);
  assert.deepEqual(r.missingInEnv, ["MISSING"]);
  assert.deepEqual(r.extraInEnv, ["EXTRA"]);
  assert.deepEqual(r.emptyRequired, ["B"]);
  assert.equal(stdout.includes("supersecret"), false);
});

test("clean parity exits 0", async () => {
  const [a, b] = await pair("A=1\nB=2\n", "A=\nB=\n");
  const { code } = await run([a, b]);
  assert.equal(code, 0);
});

test("usage error exits 2", async () => {
  const { code } = await run(["only.env"]);
  assert.equal(code, 2);
});

test("duplicate keys produce upgrade hint", async () => {
  const [a, b] = await pair("A=1\nA=2\nB=x\n", "A=\nB=\n");
  const { stdout } = await run([a, b]);
  const r = JSON.parse(stdout);
  assert.equal(r.upgrade.skill, "env-config-audit");
  assert.ok(r.upgrade.reasons.length > 0);
});

test("clean parity has no upgrade field", async () => {
  const [a, b] = await pair("A=1\nB=2\n", "A=\nB=\n");
  const { stdout } = await run([a, b]);
  assert.equal(JSON.parse(stdout).upgrade, undefined);
});
