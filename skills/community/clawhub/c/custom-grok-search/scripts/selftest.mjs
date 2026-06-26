#!/usr/bin/env node
/**
 * selftest.mjs
 *
 * Lightweight sanity tests for grok-search scripts.
 * Makes a handful of real API calls.
 */

import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function runNode(args, { timeoutMs = 180000 } = {}) {
  return new Promise((resolve) => {
    const p = spawn(process.execPath, args, {
      cwd: __dirname,
      env: process.env,
      stdio: ["ignore", "pipe", "pipe"],
    });

    let stdout = "";
    let stderr = "";
    p.stdout.on("data", (d) => (stdout += d.toString("utf8")));
    p.stderr.on("data", (d) => (stderr += d.toString("utf8")));

    const t = setTimeout(() => {
      p.kill("SIGKILL");
      resolve({ code: 124, stdout, stderr: stderr + "\n(timeout)" });
    }, timeoutMs);

    p.on("close", (code) => {
      clearTimeout(t);
      resolve({ code, stdout, stderr });
    });
  });
}

function assert(cond, msg) {
  if (!cond) throw new Error(msg);
}

function assertJsonShape(obj, { mode, max }) {
  assert(obj && typeof obj === "object", "output is not an object");
  assert(typeof obj.query === "string", "missing query string");
  assert(obj.mode === mode, `mode mismatch: expected ${mode}, got ${obj.mode}`);
  assert(Array.isArray(obj.results), "results is not an array");
  assert(Array.isArray(obj.citations), "citations is not an array");
  assert(obj.results.length <= max, `results length > max (${obj.results.length} > ${max})`);

  const set = new Set(obj.citations);
  assert(set.size === obj.citations.length, "citations contain duplicates");
}

async function testJson({ name, argv, mode, max }) {
  const { code, stdout, stderr } = await runNode(argv);
  assert(code === 0, `${name}: non-zero exit code ${code}\nstderr: ${stderr}`);

  let parsed;
  try {
    parsed = JSON.parse(stdout);
  } catch {
    throw new Error(`${name}: stdout is not valid JSON\nstdout: ${stdout.slice(0, 400)}\nstderr: ${stderr}`);
  }

  assertJsonShape(parsed, { mode, max });
  if (mode === "x" && parsed.citations.length) {
    const hasX = parsed.citations.some((u) => /https?:\/\/(x\.com|twitter\.com)\//i.test(u));
    assert(hasX, `${name}: expected at least one X link citation`);
  }
}

async function testLinksOnly({ name, argv }) {
  const { code, stdout, stderr } = await runNode(argv);
  assert(code === 0, `${name}: non-zero exit code ${code}\nstderr: ${stderr}`);
  const lines = stdout
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter(Boolean);
  assert(lines.length > 0, `${name}: expected some links on stdout`);
  for (const l of lines) assert(/^https?:\/\//.test(l), `${name}: non-url line: ${l}`);
}

async function testText({ name, argv }) {
  const { code, stdout, stderr } = await runNode(argv);
  assert(code === 0, `${name}: non-zero exit code ${code}\nstderr: ${stderr}`);
  assert(stdout.includes("Results:"), `${name}: expected pretty output with Results:`);
}

async function testModels() {
  const { code, stdout, stderr } = await runNode(["./models.mjs"]);
  assert(code === 0, `models: non-zero exit code ${code}\nstderr: ${stderr}`);
  const lines = stdout
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter(Boolean);
  assert(lines.length > 0, "models: expected some model ids");
}

async function main() {
  await testJson({
    name: "web-json",
    argv: ["./grok_search.mjs", "OpenClaw", "--web", "--max", "3"],
    mode: "web",
    max: 3,
  });

  await testLinksOnly({
    name: "web-links-only",
    argv: ["./grok_search.mjs", "OpenClaw", "--web", "--links-only"],
  });

  await testText({
    name: "web-pretty-text",
    argv: ["./grok_search.mjs", "OpenClaw", "--web", "--text", "--max", "3"],
  });

  await testModels();
  console.log("OK: custom-grok-search selftest passed");
}

main().catch((e) => {
  console.error("SELFTEST FAILED:");
  console.error(e?.stack || String(e));
  process.exit(1);
});
