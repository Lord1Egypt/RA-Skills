#!/usr/bin/env tsx
/**
 * revoke.ts
 *
 * Safe revocation of Freedom Preserving Protocol adoption. Preserves history
 * rather than deleting it. Every step is reversible (backups created) and
 * auditable (final entry appended to the hash-chained log).
 *
 * Steps performed (in order, each with --dry-run support):
 *   1. Verify the audit log chain is intact (refuse to revoke from a forged log).
 *   2. Append a "[REVOKED yyyy-mm-ddTHH:MM:SSZ — reason]" annotation to the
 *      SOUL.md adoption block (does NOT delete the block).
 *   3. Append a revocation entry to MEMORY.md (does NOT edit the original entry).
 *   4. Append a kind=revocation hash-chained entry to the audit log.
 *   5. Print the openclaw command to disable the companion plugin (does not
 *      execute it — that requires user-level shell access and consent).
 *   6. Write a .fpp-revoked marker file alongside the audit log so future
 *      heartbeats can detect the revocation.
 *
 * Constitutional rationale:
 *   - Law 1 (consent): user explicitly invoked this; we don't presume.
 *   - Law 2 (corrigibility): revocation itself is auditable.
 *   - Law 3 (reversibility): backups created; original adoption block preserved.
 *   - Law 5 (scoped exploration): does not touch files outside the args.
 */

import {
  readFileSync,
  writeFileSync,
  existsSync,
  copyFileSync,
  appendFileSync,
  mkdirSync,
} from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { appendAuditEntry } from "./audit-append.ts";
import { verify as verifyAuditChain } from "./audit-verify.ts";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, "..");
void root;

type Args = {
  soul?: string;
  memory?: string;
  log: string;
  reason: string;
  dryRun: boolean;
};

function parseArgs(argv: string[]): Args {
  const args: Args = {
    log: ".openclaw/workspace/constitution-audit.jsonl",
    reason: "",
    dryRun: false,
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--soul") args.soul = argv[++i];
    else if (a === "--memory") args.memory = argv[++i];
    else if (a === "--log") args.log = argv[++i];
    else if (a === "--reason") args.reason = argv[++i];
    else if (a === "--dry-run") args.dryRun = true;
    else if (a === "--help" || a === "-h") {
      console.log(`Usage: npm run revoke -- [options]

Required:
  --reason <text>    Free-text reason for revocation (kept in audit log)

Targets (at least one):
  --soul    <path>   Annotate SOUL.md adoption block as revoked
  --memory  <path>   Append revocation entry to MEMORY.md

Options:
  --log <path>       Audit log path (default .openclaw/workspace/constitution-audit.jsonl)
  --dry-run          Show what would change without writing
  -h, --help         This help

The original adoption block in SOUL.md is NOT deleted — it is annotated with
a [REVOKED ...] tag so the historical fact of adoption remains legible.

To disable the companion plugin, follow the printed command (this script
does not run it for you).`);
      process.exit(0);
    }
  }
  return args;
}

function nowIso(): string {
  return new Date().toISOString();
}

function backupName(target: string): string {
  return `${target}.${nowIso().replace(/[:.]/g, "-")}.bak`;
}

const ADOPTION_MARKER = "Freedom Preserving Protocol";

function annotateSoul(path: string, reason: string, ts: string, dryRun: boolean) {
  if (!existsSync(path)) {
    console.log(`[SOUL ] file not found: ${path} — skipping`);
    return;
  }
  const content = readFileSync(path, "utf-8");
  if (!content.includes(ADOPTION_MARKER)) {
    console.log(
      `[SOUL ] no adoption block found (marker "${ADOPTION_MARKER}" absent) — skipping`,
    );
    return;
  }
  const tag = `\n\n> **[REVOKED ${ts}]** Reason: ${reason}\n`;
  const annotated = content.includes(`[REVOKED `)
    ? content
    : insertAfterMarker(content, ADOPTION_MARKER, tag);

  if (annotated === content) {
    console.log(`[SOUL ] already annotated as revoked — skipping`);
    return;
  }
  if (dryRun) {
    console.log(`[SOUL ] (dry-run) would annotate adoption block with:`);
    console.log(tag);
    return;
  }
  const bak = backupName(path);
  copyFileSync(path, bak);
  writeFileSync(path, annotated);
  console.log(`[SOUL ] backup created: ${bak}`);
  console.log(`[SOUL ] adoption block annotated as REVOKED`);
}

function insertAfterMarker(content: string, marker: string, insertion: string) {
  const i = content.indexOf(marker);
  if (i < 0) return content;
  const afterHeading = content.indexOf("\n", i);
  if (afterHeading < 0) return content + insertion;
  return content.slice(0, afterHeading) + insertion + content.slice(afterHeading);
}

function appendMemoryRevocation(
  path: string,
  reason: string,
  ts: string,
  dryRun: boolean,
) {
  const block = [
    "",
    "## Constitutional Adoption — REVOKED",
    "",
    `- Revoked: ${ts}`,
    `- Reason: ${reason}`,
    "- Original adoption block (above) intentionally retained for historical legibility.",
    "- Audit log: a kind=revocation entry has been appended to constitution-audit.jsonl.",
    "",
  ].join("\n");

  if (!existsSync(path)) {
    if (dryRun) {
      console.log(`[MEM  ] (dry-run) would create ${path} with revocation block`);
      return;
    }
    mkdirSync(dirname(path), { recursive: true });
    writeFileSync(path, block.trimStart());
    console.log(`[MEM  ] created and wrote revocation block`);
    return;
  }
  if (dryRun) {
    console.log(`[MEM  ] (dry-run) would append revocation block:`);
    console.log(block);
    return;
  }
  const bak = backupName(path);
  copyFileSync(path, bak);
  appendFileSync(path, block);
  console.log(`[MEM  ] backup created: ${bak}`);
  console.log(`[MEM  ] revocation block appended`);
}

function appendAuditRevocation(logPath: string, reason: string, dryRun: boolean) {
  if (dryRun) {
    console.log(
      `[AUDIT] (dry-run) would append kind=revocation entry to ${logPath}`,
    );
    return;
  }
  try {
    const result = appendAuditEntry({
      log: logPath,
      kind: "revocation",
      notes: reason.slice(0, 280),
      adoptionIntact: false,
    });
    console.log(`[AUDIT] revocation entry appended to ${result.logPath}`);
    console.log(`        previousHash: ${result.previousHash.slice(0, 16)}...`);
    console.log(`        thisHash:     ${result.hash.slice(0, 16)}...`);
  } catch (e) {
    console.error(`[AUDIT] failed to append revocation entry: ${(e as Error).message}`);
  }
}

function writeMarker(logPath: string, reason: string, ts: string, dryRun: boolean) {
  const markerPath = resolve(dirname(logPath), ".fpp-revoked");
  const content = `Freedom Preserving Protocol — revoked ${ts}\nReason: ${reason}\n`;
  if (dryRun) {
    console.log(`[MARK ] (dry-run) would write marker to ${markerPath}`);
    return;
  }
  mkdirSync(dirname(markerPath), { recursive: true });
  writeFileSync(markerPath, content);
  console.log(`[MARK ] revocation marker written to ${markerPath}`);
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.reason || args.reason.trim().length === 0) {
    console.error(
      "Refusing to revoke without --reason. Revocation should be transparent and motivated.",
    );
    process.exit(2);
  }
  if (!args.soul && !args.memory) {
    console.log(
      "No --soul or --memory provided. The audit log will still receive a revocation entry. Continuing.",
    );
  }

  const ts = nowIso();
  console.log(`Revocation timestamp: ${ts}`);
  console.log(`Reason: ${args.reason}`);
  if (args.dryRun) console.log("Mode: DRY RUN\n");
  else console.log("Mode: WRITE — backups will be created.\n");

  const logResolved = resolve(args.log);
  if (existsSync(logResolved)) {
    const chainReport = verifyAuditChain(logResolved);
    if (!chainReport.ok) {
      console.error(
        `[AUDIT] Chain integrity check FAILED — refusing to revoke from a potentially forged log.`,
      );
      for (const e of chainReport.errors.slice(0, 3)) {
        console.error(`        ${e}`);
      }
      console.error(
        `\nFix the audit chain first (see docs/TROUBLESHOOTING.md#5), then retry.`,
      );
      process.exit(1);
    }
    console.log(`[AUDIT] Chain integrity verified (${chainReport.entries} entries)\n`);
  }

  if (args.soul) annotateSoul(resolve(args.soul), args.reason, ts, args.dryRun);
  if (args.memory)
    appendMemoryRevocation(resolve(args.memory), args.reason, ts, args.dryRun);
  appendAuditRevocation(resolve(args.log), args.reason, args.dryRun);
  writeMarker(resolve(args.log), args.reason, ts, args.dryRun);

  console.log("\nIf the companion plugin is installed, disable it with:");
  console.log("  openclaw plugins disable openclaw-fpp-plugin");
  console.log("  (or your equivalent for your OpenClaw version)\n");

  console.log(
    "Revocation complete. History preserved; future heartbeats should treat .fpp-revoked as authoritative.",
  );
}

main();
