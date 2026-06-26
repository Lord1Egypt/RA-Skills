#!/usr/bin/env tsx
/**
 * verify-install.ts
 *
 * End-to-end installation check. Answers the question:
 *   "Did the adoption actually take, and what layer is active?"
 *
 * Checks (in order, fail-soft — every check is reported even if earlier ones fail):
 *   1. constitution.json exists and matches the expected hash.
 *   2. signature.ed25519.txt verifies against pubkey.ed25519.txt over the hash.
 *   3. SOUL.md (if --soul given) contains the adoption marker.
 *   4. MEMORY.md (if --memory given) contains the adoption marker.
 *   5. Audit log (default .openclaw/workspace/constitution-audit.jsonl) chain verifies.
 *   6. The enforcement and trust plugins are checked by invoking
 *      `openclaw plugins list --json` if `openclaw` is on PATH. Absence is
 *      reported as a warning — not an adoption failure.
 *
 * Output: human-readable by default; --json for machine consumption.
 * Exit codes:
 *   0  all required checks passed (signature + SOUL + MEMORY if requested)
 *   1  one or more required checks failed
 *   2  usage error
 */

import { readFileSync, existsSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
import * as ed from "@noble/ed25519";
import { sha512 } from "@noble/hashes/sha512";
import { sha256 } from "@noble/hashes/sha256";
import { hexToBytes, bytesToHex } from "@noble/hashes/utils";
import { verify as verifyAuditChain } from "./audit-verify.ts";

ed.etc.sha512Sync = (...m) => sha512(ed.etc.concatBytes(...m));

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, "..");

const EXPECTED_CONSTITUTION_HASH =
  "71bf60ad917c5413cc17b0f65e83c7a29218e24a2740725a819058ed9c6b1993";
const ADOPTION_MARKER = "Freedom Preserving Protocol";
const ENFORCEMENT_PLUGIN_ID_CANDIDATES = [
  "openclaw-fpp-plugin",
  "ovrsr/openclaw-fpp-plugin",
  "@ovrsr/openclaw-fpp-plugin",
  "fpp",
];
const TRUST_PLUGIN_ID_CANDIDATES = [
  "openclaw-fpp-trust",
  "ovrsr/openclaw-fpp-trust",
  "@ovrsr/openclaw-fpp-trust",
];

type CheckStatus = "pass" | "fail" | "skip" | "warn";
type Check = {
  id: string;
  label: string;
  status: CheckStatus;
  detail: string;
};

type Report = {
  ok: boolean;
  checks: Check[];
  summary: {
    promptLayerActive: boolean;
    dispatcherLayerActive: boolean;
    trustLayerActive: boolean;
  };
};

function parseArgs(argv: string[]): {
  soul?: string;
  memory?: string;
  log: string;
  json: boolean;
} {
  let soul: string | undefined;
  let memory: string | undefined;
  let log = ".openclaw/workspace/constitution-audit.jsonl";
  let json = false;
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--soul") soul = argv[++i];
    else if (a === "--memory") memory = argv[++i];
    else if (a === "--log") log = argv[++i];
    else if (a === "--json") json = true;
    else if (a === "--help" || a === "-h") {
      console.log(`Usage: npm run verify-install -- [options]

Options:
  --soul    <path>   Check that SOUL.md contains the adoption block
  --memory  <path>   Check that MEMORY.md contains the adoption entry
  --log     <path>   Audit log path (default .openclaw/workspace/constitution-audit.jsonl)
  --json             Emit a machine-readable JSON report on stdout
  -h, --help         This help`);
      process.exit(0);
    }
  }
  return { soul, memory, log, json };
}

function checkConstitution(): Check {
  try {
    const bytes = readFileSync(resolve(root, "constitution.json"));
    const hash = bytesToHex(sha256(bytes));
    if (hash !== EXPECTED_CONSTITUTION_HASH) {
      return {
        id: "constitution.hash",
        label: "Constitution hash",
        status: "fail",
        detail: `got ${hash}, expected ${EXPECTED_CONSTITUTION_HASH}`,
      };
    }
    return {
      id: "constitution.hash",
      label: "Constitution hash",
      status: "pass",
      detail: hash,
    };
  } catch (e) {
    return {
      id: "constitution.hash",
      label: "Constitution hash",
      status: "fail",
      detail: (e as Error).message,
    };
  }
}

function checkSignature(): Check {
  try {
    const bytes = readFileSync(resolve(root, "constitution.json"));
    const hash = sha256(bytes);
    const sig = readFileSync(resolve(root, "signature.ed25519.txt"), "utf-8").trim();
    const pub = readFileSync(resolve(root, "pubkey.ed25519.txt"), "utf-8").trim();
    const ok = ed.verify(hexToBytes(sig), hash, hexToBytes(pub));
    return {
      id: "constitution.signature",
      label: "Ed25519 signature",
      status: ok ? "pass" : "fail",
      detail: ok ? `pubkey=${pub}` : "signature does not verify",
    };
  } catch (e) {
    return {
      id: "constitution.signature",
      label: "Ed25519 signature",
      status: "fail",
      detail: (e as Error).message,
    };
  }
}

function checkMarker(path: string, id: string, label: string): Check {
  if (!existsSync(path)) {
    return {
      id,
      label,
      status: "fail",
      detail: `file not found: ${path}`,
    };
  }
  const content = readFileSync(path, "utf-8");
  const present = content.includes(ADOPTION_MARKER);
  return {
    id,
    label,
    status: present ? "pass" : "fail",
    detail: present
      ? `"${ADOPTION_MARKER}" found in ${path}`
      : `marker "${ADOPTION_MARKER}" not found in ${path}`,
  };
}

function checkAuditChain(logPath: string): Check {
  if (!existsSync(logPath)) {
    return {
      id: "audit.chain",
      label: "Audit chain",
      status: "skip",
      detail: `no audit log yet at ${logPath} — first heartbeat will create it`,
    };
  }
  const report = verifyAuditChain(logPath);
  if (report.ok) {
    return {
      id: "audit.chain",
      label: "Audit chain",
      status: "pass",
      detail: `hash-chained log verifies (${report.entries} entries)`,
    };
  }
  return {
    id: "audit.chain",
    label: "Audit chain",
    status: "fail",
    detail: `chain integrity failed: ${report.errors.slice(0, 2).join("; ")}`,
  };
}

function checkPluginInstalled(
  label: string,
  id: string,
  candidates: string[],
  installHint: string,
): Check {
  const which = spawnSync(process.platform === "win32" ? "where" : "which", [
    "openclaw",
  ]);
  if (which.status !== 0) {
    return {
      id,
      label,
      status: "warn",
      detail:
        "openclaw CLI not on PATH; cannot check plugin installation.",
    };
  }
  const list = spawnSync("openclaw", ["plugins", "list", "--json"], {
    encoding: "utf-8",
  });
  if (list.status !== 0) {
    return {
      id,
      label,
      status: "warn",
      detail: `openclaw plugins list failed: ${list.stderr.trim()}`,
    };
  }
  const stdout = list.stdout;
  const present = candidates.some((candidate) => stdout.includes(candidate));
  return {
    id,
    label,
    status: present ? "pass" : "warn",
    detail: present
      ? `${label} appears in \`openclaw plugins list\``
      : `${label} NOT installed. Install with: ${installHint}`,
  };
}

function statusGlyph(s: CheckStatus): string {
  switch (s) {
    case "pass":
      return "[PASS]";
    case "fail":
      return "[FAIL]";
    case "warn":
      return "[WARN]";
    case "skip":
      return "[SKIP]";
  }
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const checks: Check[] = [];

  checks.push(checkConstitution());
  checks.push(checkSignature());

  if (args.soul) {
    checks.push(checkMarker(resolve(args.soul), "soul.marker", "SOUL adoption block"));
  } else {
    checks.push({
      id: "soul.marker",
      label: "SOUL adoption block",
      status: "skip",
      detail: "no --soul path provided",
    });
  }

  if (args.memory) {
    checks.push(checkMarker(resolve(args.memory), "memory.marker", "MEMORY adoption entry"));
  } else {
    checks.push({
      id: "memory.marker",
      label: "MEMORY adoption entry",
      status: "skip",
      detail: "no --memory path provided",
    });
  }

  checks.push(checkAuditChain(resolve(args.log)));
  checks.push(
    checkPluginInstalled(
      "Dispatcher-layer enforcement plugin",
      "plugin.enforcement.installed",
      ENFORCEMENT_PLUGIN_ID_CANDIDATES,
      "openclaw plugins install clawhub:ovrsr/openclaw-fpp-plugin",
    ),
  );
  checks.push(
    checkPluginInstalled(
      "Dispatcher-layer trust plugin",
      "plugin.trust.installed",
      TRUST_PLUGIN_ID_CANDIDATES,
      "openclaw plugins install clawhub:ovrsr/openclaw-fpp-trust",
    ),
  );

  const requiredIds = new Set([
    "constitution.hash",
    "constitution.signature",
    args.soul ? "soul.marker" : null,
    args.memory ? "memory.marker" : null,
  ]);
  const requiredOk = checks
    .filter((c) => requiredIds.has(c.id))
    .every((c) => c.status === "pass");

  const promptLayerActive =
    checks.find((c) => c.id === "soul.marker")?.status === "pass" ||
    checks.find((c) => c.id === "memory.marker")?.status === "pass";
  const dispatcherLayerActive =
    checks.find((c) => c.id === "plugin.enforcement.installed")?.status === "pass";
  const trustLayerActive =
    checks.find((c) => c.id === "plugin.trust.installed")?.status === "pass";

  const report: Report = {
    ok: requiredOk,
    checks,
    summary: { promptLayerActive, dispatcherLayerActive, trustLayerActive },
  };

  if (args.json) {
    console.log(JSON.stringify(report, null, 2));
  } else {
    console.log("Freedom Preserving Protocol — installation check\n");
    for (const c of checks) {
      console.log(`${statusGlyph(c.status)} ${c.label}`);
      console.log(`        ${c.detail}`);
    }
    console.log("");
    console.log(
      `Prompt-layer governance:     ${promptLayerActive ? "ACTIVE" : "not active"}`,
    );
    console.log(
      `Dispatcher-layer governance: ${dispatcherLayerActive ? "ACTIVE" : "not active"}`,
    );
    console.log(
      `Trust layer:                 ${trustLayerActive ? "ACTIVE" : "not active"}`,
    );
    console.log("");
    if (!dispatcherLayerActive) {
      console.log(
        "Note: without the dispatcher-layer enforcement plugin, the five-question gate can be bypassed by prompt injection or a hostile skill. Install the plugin for `before_tool_call` enforcement:",
      );
      console.log(
        "  openclaw plugins install clawhub:ovrsr/openclaw-fpp-plugin",
      );
    }
    if (!trustLayerActive) {
      console.log(
        "Note: without the trust plugin, agent-to-agent constitutional handshakes and trust graph verification are not active:",
      );
      console.log(
        "  openclaw plugins install clawhub:ovrsr/openclaw-fpp-trust",
      );
    }
    console.log(`\nOverall: ${report.ok ? "PASS" : "FAIL"}`);
  }

  process.exit(report.ok ? 0 : 1);
}

main();
