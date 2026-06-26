#!/usr/bin/env node

import path from "node:path";
import { pathToFileURL } from "node:url";
import { detectHost } from "./host-detect.js";
import { inferSleepFromGit } from "./git-sleep.js";
import { getSystemInfo } from "./system-info.js";
import { dontDealHome, formatLocalIso, writeJsonFile } from "./utils.js";

function deriveOverallFatigue({ sleep, system }) {
  if (sleep.risk_flag === "high") {
    return "high";
  }

  if (system.is_late_night && sleep.risk_flag !== "low") {
    return "high";
  }

  if (system.is_late_night || sleep.risk_flag === "moderate") {
    return "moderate";
  }

  if (sleep.risk_flag === "low") {
    return "low";
  }

  return "unknown";
}

export async function generateSnapshot(options = {}) {
  const now = options.now ?? new Date();
  const system = getSystemInfo(now);
  const host = await detectHost(options.env);
  const sleep = await inferSleepFromGit({
    cwd: options.cwd ?? process.cwd(),
    analyzedDays: options.analyzedDays ?? 7,
    commitLimit: options.commitLimit ?? 120
  });

  return {
    generated_at: formatLocalIso(now),
    system,
    host,
    sleep,
    overall_fatigue: deriveOverallFatigue({ sleep, system })
  };
}

async function main() {
  const snapshot = await generateSnapshot();
  const snapshotPath = path.join(dontDealHome(process.env), "snapshot.json");

  await writeJsonFile(snapshotPath, snapshot);
  process.stdout.write(JSON.stringify(snapshot, null, 2) + "\n");
}

const entrypoint = process.argv[1] ? pathToFileURL(process.argv[1]).href : null;

if (entrypoint === import.meta.url) {
  main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });
}
