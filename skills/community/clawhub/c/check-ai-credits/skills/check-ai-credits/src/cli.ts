#!/usr/bin/env bun
import type { Snapshot } from "./types";
import { findProvider, registry } from "./registry";
import { loadLog, logPath, saveLog } from "./core/log";
import { calculateTrend } from "./core/trend";
import { errorSnapshot } from "./core/snapshot";
import { formatSnapshot, formatTrend } from "./format";

const HELP = `check-ai-credits — check AI provider credits/balance across 10 providers

Usage:
  check-ai-credits [provider] [options]

Providers:
  ${registry.map((p) => p.id).join(", ")}

Options:
  --json       machine-readable snapshots
  --trend      burn rate + days-left from logged history
  --list       show providers and credential detection status
  --models     include per-model month breakdown (deepinfra)
  --no-log     do not append snapshots to the trend log
  --help       this help

Trend log: $CHECK_AI_CREDITS_LOG (default ~/.check-ai-credits/log.json)
Read-only: OAuth tokens are never refreshed; secrets are never printed.`;

async function runCheck(
  ids: string[],
  opts: { json: boolean; noLog: boolean; models: boolean },
): Promise<number> {
  const selected = ids.length
    ? ids.map((id) => findProvider(id)).filter((p): p is NonNullable<typeof p> => Boolean(p))
    : registry;

  const snapshots: Snapshot[] = await Promise.all(
    selected.map((p) =>
      p.fetch({ models: opts.models }).catch((err: unknown) =>
        errorSnapshot(p.id, `adapter threw: ${err instanceof Error ? err.message : String(err)}`),
      ),
    ),
  );

  if (!opts.noLog) saveLog([...loadLog(), ...snapshots]);

  if (opts.json) {
    console.log(JSON.stringify(snapshots, null, 2));
  } else {
    for (const s of snapshots) console.log(formatSnapshot(s));
  }
  return snapshots.some((s) => s.error) ? 1 : 0;
}

function runTrend(ids: string[], json: boolean): number {
  const log = loadLog();
  const providerIds =
    ids.length > 0 ? ids : [...new Set(log.map((e) => e.provider))];
  const trends = providerIds
    .map((id) => calculateTrend(log, id))
    .filter((t): t is NonNullable<typeof t> => t !== null);
  if (json) {
    console.log(JSON.stringify(trends, null, 2));
  } else if (trends.length === 0) {
    console.log("No trend data yet (need 2+ snapshots per provider).");
    console.log(`(log: ${logPath()})`);
  } else {
    for (const t of trends) console.log(formatTrend(t));
  }
  return 0;
}

async function runList(json: boolean): Promise<number> {
  const rows = await Promise.all(
    registry.map(async (p) => ({ id: p.id, label: p.label, ...(await p.detect()) })),
  );
  if (json) {
    console.log(JSON.stringify(rows, null, 2));
  } else {
    for (const r of rows) {
      const mark = r.configured ? "✅" : "⚪️";
      console.log(`${mark} ${r.id.padEnd(12)} ${r.source ?? r.reason ?? ""}`);
    }
  }
  return 0;
}

async function main(): Promise<number> {
  const args = process.argv.slice(2);
  if (args.includes("--help") || args.includes("-h")) {
    console.log(HELP);
    return 0;
  }
  const json = args.includes("--json");
  const trendMode = args.includes("--trend");
  const noLog = args.includes("--no-log");
  const models = args.includes("--models");
  const listMode = args.includes("--list");
  const positional = args.filter((a) => !a.startsWith("--"));

  if (listMode) return runList(json);

  if (trendMode) return runTrend(positional, json);

  // unknown provider guard (positional args are provider ids)
  const unknown = positional.filter((id) => !findProvider(id));
  if (unknown.length > 0) {
    console.error(`unknown provider(s): ${unknown.join(", ")}`);
    console.error(`available: ${registry.map((p) => p.id).join(", ")}`);
    return 2;
  }

  return runCheck(positional, { json, noLog, models });
}

if (import.meta.main) {
  main().then(
    (code) => process.exit(code),
    (err: unknown) => {
      console.error(`fatal: ${err instanceof Error ? (err.stack ?? err.message) : String(err)}`);
      process.exit(1);
    },
  );
}
