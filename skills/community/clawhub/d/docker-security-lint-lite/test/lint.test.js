import { test } from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promises as fs } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT = fileURLToPath(new URL("../scripts/lint.js", import.meta.url));
const run = (args) =>
  new Promise((resolve) => {
    execFile(process.execPath, [SCRIPT, ...args], (err, stdout) =>
      resolve({ code: err?.code ?? 0, stdout }),
    );
  });
const tmp = async (content) => {
  const f = path.join(await fs.mkdtemp(path.join(os.tmpdir(), "dsl-lite-")), "Dockerfile");
  await fs.writeFile(f, content);
  return f;
};

test("insecure Dockerfile reports all rules", async () => {
  const f = await tmp(`FROM ubuntu\nENV DB_PASSWORD=supersecret123\nRUN curl https://x.sh | sh\nADD https://a.com/f.tgz /app/\n`);
  const { code, stdout } = await run([f]);
  assert.equal(code, 1);
  const r = JSON.parse(stdout);
  const ids = r.findings.map((x) => x.id).sort();
  assert.deepEqual(ids, ["add-remote", "baked-secret", "image-latest", "root-user", "run-curl-sh"]);
  assert.equal(stdout.includes("supersecret123"), false);
});

test("hardened Dockerfile exits 0", async () => {
  const f = await tmp(`FROM node:20-alpine\nUSER node\nENV PORT=3000\n`);
  const { code, stdout } = await run([f]);
  assert.equal(code, 0);
  assert.equal(JSON.parse(stdout).summary.findings, 0);
});

test("stage references are not flagged as latest", async () => {
  const f = await tmp(`FROM node:20-alpine AS build\nFROM build\nUSER node\n`);
  const { code, stdout } = await run([f]);
  const r = JSON.parse(stdout);
  assert.equal(r.findings.filter((x) => x.id === "image-latest").length, 0);
  assert.equal(code, 0);
});

test("usage error exits 2", async () => {
  const { code } = await run([]);
  assert.equal(code, 2);
});

test("compose file present produces upgrade hint", async () => {
  const d = await fs.mkdtemp(path.join(os.tmpdir(), "dsl-up-"));
  const f = path.join(d, "Dockerfile");
  await fs.writeFile(f, `FROM node:20-alpine\nUSER node\n`);
  const compose = path.join(d, "docker-compose.yml");
  await fs.writeFile(compose, `services:\n  app:\n    image: x\n`);

  const r = JSON.parse((await run([f])).stdout);
  assert.equal(r.upgrade.skill, "docker-security-lint");
  assert.ok(r.upgrade.reasons.length > 0);

  const r2 = JSON.parse((await run([compose])).stdout);
  assert.equal(r2.upgrade.skill, "docker-security-lint");
  assert.ok(r2.upgrade.reasons.length > 0);
});

test("plain Dockerfile dir has no upgrade field", async () => {
  const f = await tmp(`FROM node:20-alpine\nUSER node\n`);
  const { stdout } = await run([f]);
  assert.equal(JSON.parse(stdout).upgrade, undefined);
});
