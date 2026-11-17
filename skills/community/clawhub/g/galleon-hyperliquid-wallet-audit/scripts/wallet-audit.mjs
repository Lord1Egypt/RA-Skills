#!/usr/bin/env node
import { mkdir, readFile, stat, writeFile } from "node:fs/promises";
import { realpathSync } from "node:fs";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { analyzeCapture, captureWallet, renderReport } from "./audit-engine.mjs";

function parse(args) {
  const result = new Map();
  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (!arg.startsWith("--")) throw new Error(`unexpected positional argument: ${arg}`);
    const name = arg.slice(2);
    if (result.has(name)) throw new Error(`duplicate option: --${name}`);
    if (name === "json") { result.set(name, true); continue; }
    if (!args[i + 1] || args[i + 1].startsWith("--")) throw new Error(`--${name} requires a value`);
    result.set(name, args[++i]);
  }
  return result;
}
function required(flags, name) { const value = flags.get(name); if (typeof value !== "string" || !value) throw new Error(`--${name} is required`); return value; }
function time(value, label) {
  const parsed = /^\d+$/.test(value) ? Number(value) : /^\d{4}-\d\d-\d\dT.*(?:Z|[+-]\d\d:\d\d)$/.test(value) ? Date.parse(value) : NaN;
  if (!Number.isSafeInteger(parsed) || parsed < 0) throw new Error(`${label} requires epoch milliseconds or ISO time with a timezone`);
  return parsed;
}
function positiveInteger(flags, name, fallback) {
  if (!flags.has(name)) return fallback;
  const value = required(flags, name);
  if (!/^\d+$/.test(value)) throw new Error(`--${name} requires a positive integer`);
  return Number(value);
}
async function persist(out, capture, report) {
  // A new output directory avoids replacing an earlier observation or unrelated files.
  await mkdir(out, { recursive: false });
  await writeFile(join(out, "capture.json"), `${JSON.stringify(capture, null, 2)}\n`, { flag: "wx" });
  await mkdir(join(out, "evidence"));
  for (const e of capture.evidence) {
    const prefix = `${String(e.sequence).padStart(3, "0")}-${e.type}`;
    await writeFile(join(out, "evidence", `${prefix}.request.json`), e.requestText, { flag: "wx" });
    if (e.responseText !== null) await writeFile(join(out, "evidence", `${prefix}.response.txt`), e.responseText, { flag: "wx" });
  }
  if (report) {
    await writeFile(join(out, "report.json"), `${JSON.stringify(report, null, 2)}\n`, { flag: "wx" });
    await writeFile(join(out, "report.md"), renderReport(report), { flag: "wx" });
  }
}
export async function runAudit(args = process.argv.slice(2)) {
  const [command = "help", ...rest] = args;
  if (["help", "--help", "-h"].includes(command)) {
    process.stdout.write(`Read-only Hyperliquid wallet audit (Node.js >=20)

node scripts/wallet-audit.mjs capture --address 0x… --network mainnet|testnet --start <ISO-with-timezone|epoch-ms> --end <ISO-with-timezone|epoch-ms> --out <new-directory> [--max-pages 10] [--timeout-ms 15000] [--json]
node scripts/wallet-audit.mjs analyze --input capture.json --out <new-directory> [--json]
node scripts/wallet-audit.mjs example --out <new-directory> [--json]

capture makes sequential public /info POST reads; no login or keys. analyze and example are offline.
Output: capture.json, report.json, report.md and raw evidence/*.request.json and *.response.txt.
--max-pages bounds each history type (1..50), --timeout-ms bounds each read (1..60000).
Amounts in JSON are decimal strings; observedNetUsdc is not a full portfolio return.
Exit 0: report produced, including explicit partial coverage. Exit 1: invalid input/evidence or failed output.
`);
    return;
  }
  if (!["capture", "analyze", "example"].includes(command)) throw new Error(`unknown audit command: ${command}`);
  const flags = parse(rest);
  const allowed = command === "capture" ? ["address", "network", "start", "end", "out", "max-pages", "timeout-ms", "json"] : command === "analyze" ? ["input", "out", "json"] : ["out", "json"];
  for (const key of flags.keys()) if (!allowed.includes(key)) throw new Error(`unknown option: --${key}`);
  const out = resolve(required(flags, "out"));
  let capture;
  if (command === "capture") {
    capture = await captureWallet({ address: required(flags, "address"), network: required(flags, "network"), startTime: time(required(flags, "start"), "--start"), endTime: time(required(flags, "end"), "--end") }, { maxPages: positiveInteger(flags, "max-pages", 10), timeoutMs: positiveInteger(flags, "timeout-ms", 15000) });
  } else {
    const input = command === "example" ? fileURLToPath(new URL("../examples/capture.json", import.meta.url)) : resolve(required(flags, "input"));
    if ((await stat(input)).size > 167772160) throw new Error("capture file exceeds 160 MiB bound");
    capture = JSON.parse(await readFile(input, "utf8"));
  }
  let report;
  try { report = analyzeCapture(capture); }
  catch (error) { if (command === "capture") await persist(out, capture, null); throw error; }
  await persist(out, capture, report);
  const result = { ok: true, source: report.source, coverage: report.coverage.status, completeWindow: report.coverage.completeWindow, observedNetUsdc: report.outcome.observedNetUsdc, files: { capture: join(out, "capture.json"), report: join(out, "report.json"), markdown: join(out, "report.md"), evidence: join(out, "evidence") } };
  process.stdout.write(flags.has("json") ? `${JSON.stringify(result, null, 2)}\n` : `Audit written: ${result.files.markdown}\nCoverage: ${result.coverage}; complete window unverified. Observed net: ${result.observedNetUsdc ?? "unavailable"} USDC (${result.source}).\n`);
  return result;
}
if (process.argv[1] && realpathSync(process.argv[1]) === realpathSync(fileURLToPath(import.meta.url))) {
  runAudit().catch((error) => {
    const message = error instanceof Error ? error.message : String(error);
    if (process.argv.includes("--json")) process.stdout.write(`${JSON.stringify({ ok: false, error: { code: "AUDIT_FAILED", message } })}\n`);
    else process.stderr.write(`error: ${message}\n`);
    process.exitCode = 1;
  });
}
