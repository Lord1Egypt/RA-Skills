#!/usr/bin/env tsx
/**
 * audit-proof.ts
 *
 * Generate or verify a Merkle inclusion proof for a specific audit entry.
 * Proves an entry exists in the chain without revealing the full log.
 *
 * Usage:
 *   npm run audit:proof -- --index 3                          # generate proof for entry 3
 *   npm run audit:proof -- --verify proof.json                # verify a proof file
 *   npm run audit:proof -- --index 3 --out proof.json         # save proof to file
 *
 * Constitutional rationale:
 *   - Law 1 (privacy by necessity): agent can prove compliance on a single
 *     entry without disclosing its full behavioral history.
 */

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";
import {
  computeMerkleRoot,
  createMerkleProof,
  verifyMerkleProof,
  type MerkleProof,
} from "./merkle.ts";

function usage() {
  console.log(`Usage: npm run audit:proof -- [options]

Generate:
  --index <n>        Entry index (0-based) to prove
  --log <path>       Audit log path (default: .openclaw/workspace/constitution-audit.jsonl)
  --out <path>       Write proof JSON to file (default: stdout)

Verify:
  --verify <path>    Verify a proof JSON file against the current log

  --json             Machine-readable output
  -h, --help         This help`);
}

type Args = {
  mode: "generate" | "verify";
  log: string;
  index: number;
  out?: string;
  verifyPath?: string;
  json: boolean;
};

function parseArgs(argv: string[]): Args {
  const args: Args = {
    mode: "generate",
    log: ".openclaw/workspace/constitution-audit.jsonl",
    index: -1,
    json: false,
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--index") args.index = parseInt(argv[++i], 10);
    else if (a === "--log") args.log = argv[++i];
    else if (a === "--out") args.out = argv[++i];
    else if (a === "--verify") {
      args.mode = "verify";
      args.verifyPath = argv[++i];
    } else if (a === "--json") args.json = true;
    else if (a === "--help" || a === "-h") {
      usage();
      process.exit(0);
    }
  }
  return args;
}

function loadLeaves(logPath: string): string[] {
  if (!existsSync(logPath)) {
    console.error(`Audit log not found: ${logPath}`);
    process.exit(2);
  }
  const content = readFileSync(logPath, "utf-8").trim();
  if (!content) return [];
  return content
    .split("\n")
    .filter((l) => l.trim())
    .map((line) => {
      const entry = JSON.parse(line) as Record<string, unknown>;
      return entry.hash as string;
    });
}

function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.mode === "verify") {
    if (!args.verifyPath) {
      console.error("--verify requires a proof file path");
      process.exit(2);
    }
    const proof: MerkleProof = JSON.parse(
      readFileSync(resolve(args.verifyPath), "utf-8"),
    );
    const valid = verifyMerkleProof(proof);

    const leaves = loadLeaves(resolve(args.log));
    const currentRoot = computeMerkleRoot(leaves);
    const rootMatch = proof.root === currentRoot;

    if (args.json) {
      console.log(
        JSON.stringify({ valid, rootMatch, proofRoot: proof.root, currentRoot }, null, 2),
      );
    } else {
      console.log(`Proof valid:        ${valid ? "YES" : "NO"}`);
      console.log(`Root matches log:   ${rootMatch ? "YES" : "NO"}`);
      console.log(`Proof root:         ${proof.root}`);
      console.log(`Current log root:   ${currentRoot}`);
      if (!rootMatch) {
        console.log(
          "\nThe log has changed since this proof was generated. The proof is valid for the root it was created against, but does not match the current log state.",
        );
      }
    }
    process.exit(valid && rootMatch ? 0 : 1);
  }

  if (args.index < 0) {
    console.error("--index is required (0-based entry index)");
    process.exit(2);
  }

  const leaves = loadLeaves(resolve(args.log));
  if (args.index >= leaves.length) {
    console.error(
      `Index ${args.index} out of range (log has ${leaves.length} entries)`,
    );
    process.exit(2);
  }

  const proof = createMerkleProof(leaves, args.index);
  if (!proof) {
    console.error("Failed to create proof");
    process.exit(1);
  }

  const proofJson = JSON.stringify(proof, null, 2);
  if (args.out) {
    writeFileSync(resolve(args.out), proofJson + "\n");
    console.log(`Proof written to ${args.out}`);
    console.log(`  entry:  ${args.index}`);
    console.log(`  leaf:   ${proof.leaf.slice(0, 16)}...`);
    console.log(`  root:   ${proof.root.slice(0, 16)}...`);
    console.log(`  steps:  ${proof.path.length}`);
  } else if (args.json) {
    console.log(proofJson);
  } else {
    console.log(`Merkle inclusion proof for entry ${args.index}:`);
    console.log(`  leaf:   ${proof.leaf}`);
    console.log(`  root:   ${proof.root}`);
    console.log(`  steps:  ${proof.path.length}`);
    console.log(`\nFull proof JSON:`);
    console.log(proofJson);
  }
}

main();
