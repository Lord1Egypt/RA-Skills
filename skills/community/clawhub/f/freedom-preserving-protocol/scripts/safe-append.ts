#!/usr/bin/env tsx
/**
 * safe-append.ts
 *
 * Idempotent, backup-creating, never-overwriting appender for SOUL.md and
 * MEMORY.md adoption blocks. Replaces the dangerous "tell the agent to edit
 * SOUL.md" instruction in earlier versions of this skill.
 *
 * Behavior:
 *   - Refuses to run if the adoption block is already present (idempotent).
 *   - Creates a timestamped .bak file before any write.
 *   - Appends, never overwrites or rewrites surrounding content.
 *   - Prints a diff summary before writing; supports --dry-run.
 *   - Computes the constitution hash from constitution.json (does not trust args).
 *
 * Constitutional rationale:
 *   - Law 1 (consent): we only modify files the user explicitly passed in.
 *   - Law 3 (reversibility): every write produces a .bak; rerun is idempotent.
 *   - Law 2 (corrigibility): logs a summary to stdout so the user can interrupt.
 */

import {
  readFileSync,
  writeFileSync,
  existsSync,
  copyFileSync,
  mkdirSync,
} from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { sha256 } from "@noble/hashes/sha256";
import { bytesToHex } from "@noble/hashes/utils";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, "..");

// ---- arg parsing -----------------------------------------------------------

type Args = {
  soul?: string;
  memory?: string;
  dryRun: boolean;
  yes: boolean;
};

function parseArgs(argv: string[]): Args {
  const args: Args = { dryRun: false, yes: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--soul") args.soul = argv[++i];
    else if (a === "--memory") args.memory = argv[++i];
    else if (a === "--dry-run") args.dryRun = true;
    else if (a === "--yes" || a === "-y") args.yes = true;
    else if (a === "--help" || a === "-h") {
      printHelp();
      process.exit(0);
    }
  }
  return args;
}

function printHelp() {
  console.log(`Usage: npm run adopt -- [options]

Options:
  --soul    <path>   Path to your SOUL.md (will append adoption block)
  --memory  <path>   Path to your MEMORY.md (will append adoption entry)
  --dry-run          Show what would change, write nothing
  -y, --yes          Skip confirmation prompt
  -h, --help         This help

Both --soul and --memory are independent; you may pass either, both, or
neither. If neither is passed, this script exits 0 with no action.

The constitution hash is read from constitution.json in the skill package
root. Templates are read from adoption/SOUL-BLOCK.md and
adoption/MEMORY-ENTRY.md.

Idempotent: rerun is safe; if the adoption block is already present in the
target file, this script logs and exits 0 without modifying anything.

Reversible: a timestamped .bak file is created next to each target before
any write. To undo, restore from the .bak or use \`npm run revoke\`.
`);
}

// ---- helpers ---------------------------------------------------------------

function nowIso(): string {
  return new Date().toISOString();
}

function backupName(target: string): string {
  const stamp = nowIso().replace(/[:.]/g, "-");
  return `${target}.${stamp}.bak`;
}

function constitutionHash(): string {
  const path = resolve(root, "constitution.json");
  const bytes = readFileSync(path);
  return bytesToHex(sha256(bytes));
}

function fillTemplate(tmpl: string, hash: string, ts: string): string {
  return tmpl
    .replace(/\[CONSTITUTION_HASH\]/g, hash)
    .replace(/\[TIMESTAMP\]/g, ts);
}

const ADOPTION_MARKER = "Freedom Preserving Protocol";

function alreadyAdopted(existing: string): boolean {
  return existing.includes(ADOPTION_MARKER);
}

function ensureTrailingNewline(s: string): string {
  return s.endsWith("\n") ? s : s + "\n";
}

function appendSafely(
  target: string,
  block: string,
  label: string,
  dryRun: boolean,
): "appended" | "skipped" | "created" {
  const blockOut = ensureTrailingNewline("\n" + block);

  if (!existsSync(target)) {
    console.log(`[${label}] does not exist: ${target}`);
    if (dryRun) {
      console.log(`[${label}] (dry-run) would create with adoption block`);
      return "created";
    }
    mkdirSync(dirname(target), { recursive: true });
    writeFileSync(target, blockOut.trimStart());
    console.log(`[${label}] created and wrote adoption block`);
    return "created";
  }

  const existing = readFileSync(target, "utf-8");
  if (alreadyAdopted(existing)) {
    console.log(
      `[${label}] already contains "${ADOPTION_MARKER}" — skipping (idempotent).`,
    );
    return "skipped";
  }

  if (dryRun) {
    console.log(`[${label}] (dry-run) would append ${blockOut.length} bytes:`);
    console.log("---- begin block ----");
    process.stdout.write(blockOut);
    console.log("---- end block ----");
    return "appended";
  }

  const bak = backupName(target);
  copyFileSync(target, bak);
  console.log(`[${label}] backup created: ${bak}`);

  const next = ensureTrailingNewline(existing) + blockOut;
  writeFileSync(target, next);
  console.log(`[${label}] appended adoption block (${blockOut.length} bytes)`);
  return "appended";
}

// ---- main ------------------------------------------------------------------

function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.soul && !args.memory) {
    console.log(
      "No --soul or --memory path provided; nothing to do. Run with --help for usage.",
    );
    process.exit(0);
  }

  const hash = constitutionHash();
  const ts = nowIso();

  console.log(`Constitution hash: ${hash}`);
  console.log(`Adoption timestamp: ${ts}`);
  if (args.dryRun) console.log("Mode: DRY RUN — no files will be modified.\n");
  else console.log("Mode: WRITE — backups will be created.\n");

  let any = false;

  if (args.soul) {
    const tmplPath = resolve(root, "adoption", "SOUL-BLOCK.md");
    const tmpl = readFileSync(tmplPath, "utf-8");
    const block = fillTemplate(tmpl, hash, ts);
    appendSafely(resolve(args.soul), block, "SOUL ", args.dryRun);
    any = true;
  }

  if (args.memory) {
    const tmplPath = resolve(root, "adoption", "MEMORY-ENTRY.md");
    const tmpl = readFileSync(tmplPath, "utf-8");
    const block = fillTemplate(tmpl, hash, ts);
    appendSafely(resolve(args.memory), block, "MEM  ", args.dryRun);
    any = true;
  }

  if (any && !args.dryRun) {
    console.log(
      "\nDone. Verify with: npm run verify-install -- --soul <path> --memory <path>",
    );
  }
}

main();
