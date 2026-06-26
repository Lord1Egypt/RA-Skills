#!/usr/bin/env tsx
/**
 * audit-verify.ts
 *
 * Verify the integrity of a hash-chained constitution audit log.
 *
 * Checks:
 *   1. Every line is valid JSON with the expected fields.
 *   2. The first entry's previousHash is 0000...0000 (64 hex zeros).
 *   3. Every subsequent entry's previousHash matches the previous entry's hash.
 *   4. Every entry's hash field equals sha256(canonical(entry minus hash)).
 *   5. The constitutionHash field matches the actual constitution.json hash.
 *
 * Exit codes:
 *   0  chain valid
 *   1  chain integrity failure (tamper detected)
 *   2  usage error
 */

import { readFileSync, existsSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { sha256 } from "@noble/hashes/sha256";
import { bytesToHex, utf8ToBytes } from "@noble/hashes/utils";
import { computeMerkleRoot } from "./merkle.ts";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, "..");

function canonicalize(value: unknown): string {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return "[" + value.map(canonicalize).join(",") + "]";
  const obj = value as Record<string, unknown>;
  const keys = Object.keys(obj).sort();
  return (
    "{" +
    keys.map((k) => JSON.stringify(k) + ":" + canonicalize(obj[k])).join(",") +
    "}"
  );
}

function hashEntry(entry: Record<string, unknown>): string {
  const { hash: _ignored, ...rest } = entry;
  void _ignored;
  return bytesToHex(sha256(utf8ToBytes(canonicalize(rest))));
}

function constitutionHash(): string {
  return bytesToHex(sha256(readFileSync(resolve(root, "constitution.json"))));
}

function parseArgs(argv: string[]): { log: string; json: boolean } {
  let log = ".openclaw/workspace/constitution-audit.jsonl";
  let json = false;
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--log") log = argv[++i];
    else if (a === "--json") json = true;
    else if (a === "--help" || a === "-h") {
      console.log(
        `Usage: npm run audit:verify -- [--log <path>] [--json]\n\nExits 0 if chain is intact, 1 if tampered. Use --json for machine output.`,
      );
      process.exit(0);
    }
  }
  return { log, json };
}

type Report = {
  ok: boolean;
  entries: number;
  errors: string[];
  expectedConstitutionHash: string;
  lastHash?: string;
  merkleRoot?: string;
};

function verify(logPath: string): Report {
  const report: Report = {
    ok: true,
    entries: 0,
    errors: [],
    expectedConstitutionHash: constitutionHash(),
  };

  if (!existsSync(logPath)) {
    report.ok = false;
    report.errors.push(`audit log not found: ${logPath}`);
    return report;
  }

  const content = readFileSync(logPath, "utf-8").trim();
  if (!content) {
    return report;
  }

  const lines = content.split("\n").filter((l) => l.trim().length > 0);
  const ZERO = "0".repeat(64);
  let prevHash = ZERO;

  for (let i = 0; i < lines.length; i++) {
    let entry: Record<string, unknown>;
    try {
      entry = JSON.parse(lines[i]) as Record<string, unknown>;
    } catch (e) {
      report.ok = false;
      report.errors.push(`line ${i + 1}: invalid JSON: ${(e as Error).message}`);
      return report;
    }

    if (entry.previousHash !== prevHash) {
      report.ok = false;
      report.errors.push(
        `line ${i + 1}: previousHash mismatch (expected ${prevHash.slice(0, 16)}..., got ${String(entry.previousHash).slice(0, 16)}...)`,
      );
    }

    const recomputed = hashEntry(entry);
    if (entry.hash !== recomputed) {
      report.ok = false;
      report.errors.push(
        `line ${i + 1}: hash mismatch (claimed ${String(entry.hash).slice(0, 16)}..., recomputed ${recomputed.slice(0, 16)}...)`,
      );
    }

    if (entry.constitutionHash !== report.expectedConstitutionHash) {
      report.ok = false;
      report.errors.push(
        `line ${i + 1}: constitutionHash mismatch — the constitution.json has changed since this entry was written, or the entry was forged`,
      );
    }

    prevHash = String(entry.hash);
    report.entries += 1;
  }

  report.lastHash = prevHash;

  const entryHashes = lines.map((line) => {
    try {
      return (JSON.parse(line) as Record<string, unknown>).hash as string;
    } catch {
      return "";
    }
  }).filter(Boolean);
  report.merkleRoot = computeMerkleRoot(entryHashes);

  const merkleFile = logPath.replace(/\.jsonl$/, ".merkle");
  if (existsSync(merkleFile)) {
    try {
      const stored = JSON.parse(readFileSync(merkleFile, "utf-8").trim());
      if (stored.root !== report.merkleRoot) {
        report.ok = false;
        report.errors.push(
          `Merkle root mismatch (stored ${String(stored.root).slice(0, 16)}..., computed ${report.merkleRoot.slice(0, 16)}...)`,
        );
      }
    } catch { /* merkle file unreadable; not a chain failure */ }
  }

  return report;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const report = verify(resolve(args.log));

  if (args.json) {
    console.log(JSON.stringify(report, null, 2));
  } else {
    console.log(`Audit log: ${args.log}`);
    console.log(`Entries:   ${report.entries}`);
    console.log(`Constitution hash: ${report.expectedConstitutionHash}`);
    if (report.lastHash) console.log(`Last hash: ${report.lastHash}`);
    if (report.ok) {
      console.log("\nChain integrity: OK");
    } else {
      console.error("\nChain integrity: FAILED");
      for (const e of report.errors) console.error(`  - ${e}`);
    }
  }

  process.exit(report.ok ? 0 : 1);
}

// Only run main if invoked directly (not when imported).
const isDirectInvocation =
  import.meta.url === `file://${process.argv[1]?.replace(/\\/g, "/")}` ||
  import.meta.url === `file:///${process.argv[1]?.replace(/\\/g, "/")}`;

if (isDirectInvocation) {
  main();
}

export { verify, type Report };
