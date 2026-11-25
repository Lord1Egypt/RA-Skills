import { test } from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { fileURLToPath } from "node:url";

const SCRIPT = fileURLToPath(new URL("../scripts/cors.js", import.meta.url));
const run = (input) =>
  new Promise((resolve) => {
    const p = execFile(process.execPath, [SCRIPT, "-"], (err, stdout) =>
      resolve({ code: err?.code ?? 0, stdout }),
    );
    p.stdin.write(input); p.stdin.end();
  });

test("wildcard + credentials fails", async () => {
  const { code, stdout } = await run("HTTP/1.1 200\nAccess-Control-Allow-Origin: *\nAccess-Control-Allow-Credentials: true\n");
  assert.equal(code, 1);
  const r = JSON.parse(stdout);
  assert.equal(r.findings[0].id, "wildcard-with-credentials");
});

test("reflected origin + credentials warns, missing Vary warns", async () => {
  const { code, stdout } = await run("Access-Control-Allow-Origin: https://evil.example\nAccess-Control-Allow-Credentials: true\n");
  assert.equal(code, 0);
  const r = JSON.parse(stdout);
  const ids = r.findings.map((f) => f.id);
  assert.ok(ids.includes("reflected-with-credentials"));
  assert.ok(ids.includes("missing-vary-origin"));
});

test("allowlisted origin with Vary gives no warn", async () => {
  const { stdout } = await run("Access-Control-Allow-Origin: https://app.example\nVary: Origin\n");
  const r = JSON.parse(stdout);
  assert.equal(r.findings.filter((f) => f.severity !== "info").length, 0);
});

test("null origin warns", async () => {
  const { stdout } = await run("Access-Control-Allow-Origin: null\n");
  const r = JSON.parse(stdout);
  assert.ok(r.findings.some((f) => f.id === "null-origin-accepted"));
});

test("specific ACAO origin produces upgrade hint", async () => {
  const { stdout } = await run("Access-Control-Allow-Origin: https://app.example\nVary: Origin\n");
  const r = JSON.parse(stdout);
  assert.equal(r.upgrade.skill, "cors-misconfig-check");
  assert.ok(r.upgrade.reasons.length > 0);
});

test("wildcard-only headers have no upgrade field", async () => {
  const { stdout } = await run("Access-Control-Allow-Origin: *\n");
  assert.equal(JSON.parse(stdout).upgrade, undefined);
});
