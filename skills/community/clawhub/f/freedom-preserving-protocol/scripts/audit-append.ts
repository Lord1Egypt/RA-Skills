#!/usr/bin/env tsx
/**
 * audit-append.ts
 *
 * Append a hash-chained JSONL entry to the constitution audit log. Each entry
 * references the SHA-256 hash of the previous entry; the first entry uses
 * "0".repeat(64) as previousHash. The "hash" field is computed over the
 * canonical JSON of the entry with the hash field omitted.
 *
 * Schema (per line):
 *   {
 *     "previousHash":   "<sha256 hex of previous entry, or 0000...0000>",
 *     "timestamp":      "<ISO 8601>",
 *     "adoptionIntact": true | false,
 *     "lawsInvoked":    ["law1", "law3", ...],
 *     "actionsReviewed": <integer >= 0>,
 *     "abstentions":     <integer >= 0>,
 *     "escalations":     <integer >= 0>,
 *     "notes":           "<string, no PII>",
 *     "kind":            "heartbeat" | "adoption" | "revocation" | "tamper_detected",
 *     "constitutionHash":"71bf60a...",
 *     "hash":            "<sha256 hex of this entry minus hash field>"
 *   }
 *
 * Constitutional rationale:
 *   - Law 2 (corrigibility): tamper-evident audit trail.
 *   - Law 3 (reversibility): append-only; never edits past entries.
 *   - Law 5 (scoped exploration): summary statistics only, no PII or content.
 */

import {
  appendFileSync,
  readFileSync,
  writeFileSync,
  existsSync,
  mkdirSync,
} from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { sha256 } from "@noble/hashes/sha256";
import { bytesToHex, utf8ToBytes } from "@noble/hashes/utils";
import { computeMerkleRoot } from "./merkle.ts";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, "..");

// ---- canonical JSON --------------------------------------------------------

/**
 * Canonical JSON: sorted keys, no extra whitespace. This is required so the
 * hash is reproducible across runtimes and verifiers.
 */
function canonicalize(value: unknown): string {
  if (value === null || typeof value !== "object") {
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    return "[" + value.map(canonicalize).join(",") + "]";
  }
  const obj = value as Record<string, unknown>;
  const keys = Object.keys(obj).sort();
  return (
    "{" +
    keys
      .map((k) => JSON.stringify(k) + ":" + canonicalize(obj[k]))
      .join(",") +
    "}"
  );
}

function hashEntry(entry: Record<string, unknown>): string {
  const { hash: _ignored, ...rest } = entry;
  void _ignored;
  return bytesToHex(sha256(utf8ToBytes(canonicalize(rest))));
}

// ---- args ------------------------------------------------------------------

const KINDS = new Set([
  "heartbeat",
  "adoption",
  "revocation",
  "tamper_detected",
]);

type Args = {
  log: string;
  kind: string;
  laws: string[];
  actions: number;
  abstentions: number;
  escalations: number;
  notes: string;
  adoptionIntact: boolean;
};

function parseArgs(argv: string[]): Args {
  const args: Args = {
    log: ".openclaw/workspace/constitution-audit.jsonl",
    kind: "heartbeat",
    laws: [],
    actions: 0,
    abstentions: 0,
    escalations: 0,
    notes: "",
    adoptionIntact: true,
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--log") args.log = argv[++i];
    else if (a === "--kind") args.kind = argv[++i];
    else if (a === "--laws") args.laws = argv[++i].split(",").filter(Boolean);
    else if (a === "--actions") args.actions = parseInt(argv[++i], 10);
    else if (a === "--abstentions") args.abstentions = parseInt(argv[++i], 10);
    else if (a === "--escalations") args.escalations = parseInt(argv[++i], 10);
    else if (a === "--notes") args.notes = argv[++i];
    else if (a === "--adoption-broken") args.adoptionIntact = false;
    else if (a === "--help" || a === "-h") {
      printHelp();
      process.exit(0);
    }
  }
  return args;
}

function printHelp() {
  console.log(`Usage: npm run audit:append -- [options]

Options:
  --log <path>           Audit log path (default: .openclaw/workspace/constitution-audit.jsonl)
  --kind <kind>          One of: heartbeat | adoption | revocation | tamper_detected
  --laws <l1,l2,...>     Comma-separated law ids invoked since last entry
  --actions <n>          Count of tool calls reviewed since last entry
  --abstentions <n>      Count of abstentions since last entry
  --escalations <n>      Count of escalations since last entry
  --notes <text>         Free-text note (no PII; bounded by sanitizer below)
  --adoption-broken      Mark adoptionIntact=false (use with --kind tamper_detected)
  -h, --help             This help

Output: appends one JSON line to <log>. Idempotency is not guaranteed by this
script (you may legitimately want two heartbeats with identical content); use
audit:verify after to check chain integrity.
`);
}

// ---- read tail of existing log --------------------------------------------

function readPreviousHash(logPath: string): string {
  const ZERO = "0".repeat(64);
  if (!existsSync(logPath)) return ZERO;
  const content = readFileSync(logPath, "utf-8").trim();
  if (!content) return ZERO;
  const lines = content.split("\n").filter((l) => l.trim().length > 0);
  if (lines.length === 0) return ZERO;
  const last = lines[lines.length - 1];
  try {
    const parsed = JSON.parse(last) as Record<string, unknown>;
    const h = parsed.hash;
    if (typeof h === "string" && /^[0-9a-f]{64}$/.test(h)) return h;
  } catch {
    /* fallthrough */
  }
  console.error(
    `WARNING: previous audit tail entry is malformed; refusing to chain from ${last.slice(0, 80)}...`,
  );
  process.exit(2);
}

function collectLeaves(logPath: string): string[] {
  if (!existsSync(logPath)) return [];
  const content = readFileSync(logPath, "utf-8").trim();
  if (!content) return [];
  const leaves: string[] = [];
  for (const line of content.split("\n")) {
    if (!line.trim()) continue;
    try {
      const entry = JSON.parse(line) as Record<string, unknown>;
      if (typeof entry.hash === "string") leaves.push(entry.hash);
    } catch { /* skip malformed */ }
  }
  return leaves;
}

function updateMerkleRoot(logPath: string): string {
  const leaves = collectLeaves(logPath);
  const root = computeMerkleRoot(leaves);
  const merkleFile = logPath.replace(/\.jsonl$/, ".merkle");
  writeFileSync(merkleFile, JSON.stringify({ root, leaves: leaves.length, updatedAt: new Date().toISOString() }) + "\n");
  return root;
}

function constitutionHash(): string {
  const path = resolve(root, "constitution.json");
  return bytesToHex(sha256(readFileSync(path)));
}

// ---- main ------------------------------------------------------------------

export type AppendOptions = {
  log: string;
  kind: "heartbeat" | "adoption" | "revocation" | "tamper_detected";
  laws?: string[];
  actions?: number;
  abstentions?: number;
  escalations?: number;
  notes?: string;
  adoptionIntact?: boolean;
};

export function appendAuditEntry(opts: AppendOptions): {
  hash: string;
  previousHash: string;
  logPath: string;
} {
  if (!KINDS.has(opts.kind)) {
    throw new Error(`Invalid kind: ${opts.kind}`);
  }
  const notes = opts.notes ?? "";
  if (notes.length > 280) {
    throw new Error("notes must be <= 280 chars (PII risk).");
  }
  const logPath = resolve(opts.log);
  mkdirSync(dirname(logPath), { recursive: true });
  const previousHash = readPreviousHash(logPath);

  const entry: Record<string, unknown> = {
    previousHash,
    timestamp: new Date().toISOString(),
    kind: opts.kind,
    adoptionIntact: opts.adoptionIntact ?? true,
    lawsInvoked: opts.laws ?? [],
    actionsReviewed: Math.max(0, opts.actions ?? 0),
    abstentions: Math.max(0, opts.abstentions ?? 0),
    escalations: Math.max(0, opts.escalations ?? 0),
    notes,
    constitutionHash: constitutionHash(),
  };
  entry.hash = hashEntry(entry);

  appendFileSync(logPath, JSON.stringify(entry) + "\n");
  const merkleRoot = updateMerkleRoot(logPath);
  return { hash: entry.hash as string, previousHash, logPath, merkleRoot };
}

function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!KINDS.has(args.kind)) {
    console.error(
      `Invalid --kind: ${args.kind}. Must be one of: ${[...KINDS].join(", ")}`,
    );
    process.exit(2);
  }
  if (args.actions < 0 || args.abstentions < 0 || args.escalations < 0) {
    console.error("Counts must be non-negative.");
    process.exit(2);
  }
  if (args.notes.length > 280) {
    console.error("--notes must be <= 280 chars (PII risk; keep it terse).");
    process.exit(2);
  }

  const result = appendAuditEntry({
    log: args.log,
    kind: args.kind as AppendOptions["kind"],
    laws: args.laws,
    actions: args.actions,
    abstentions: args.abstentions,
    escalations: args.escalations,
    notes: args.notes,
    adoptionIntact: args.adoptionIntact,
  });

  console.log(`Appended ${args.kind} entry to ${result.logPath}`);
  console.log(`  previousHash: ${result.previousHash.slice(0, 16)}...`);
  console.log(`  thisHash:     ${result.hash.slice(0, 16)}...`);
}

const isDirectInvocation =
  import.meta.url === `file://${process.argv[1]?.replace(/\\/g, "/")}` ||
  import.meta.url === `file:///${process.argv[1]?.replace(/\\/g, "/")}`;

if (isDirectInvocation) {
  main();
}

export { canonicalize, hashEntry, updateMerkleRoot };
