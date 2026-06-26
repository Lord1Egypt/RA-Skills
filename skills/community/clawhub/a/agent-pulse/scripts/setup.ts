#!/usr/bin/env -S npx tsx
console.error("DEPRECATED: This skill is no longer maintained. Use x402janus skill instead.");
process.exit(1);


import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const skillDir = path.resolve(scriptDir, "..");
const cronName = "x402janus-heartbeat";
const cronMessage =
  `Run the x402janus. cd ${skillDir} && bash scripts/auto-pulse.sh. ` +
  "If success reply OK. If fail, report exact error.";

type RunResult = ReturnType<typeof spawnSync>;

function run(command: string, args: string[]): RunResult {
  const result = spawnSync(command, args, {
    cwd: skillDir,
    env: process.env,
    encoding: "utf8",
    stdio: "pipe",
  });

  if (result.error) {
    throw result.error;
  }

  return result;
}

function getOutput(result: RunResult): string {
  const out = typeof result.stdout === "string" ? result.stdout : "";
  const err = typeof result.stderr === "string" ? result.stderr : "";
  return `${out}${err}`.trim();
}

function assertSuccess(result: RunResult, step: string): void {
  if (result.status === 0) {
    return;
  }

  const output = getOutput(result);
  throw new Error(
    `${step} failed (exit ${result.status ?? "unknown"}).${output ? `\n${output}` : ""}`
  );
}

function ensureRequiredFiles(): void {
  const required = ["pulse.sh", "auto-pulse.sh"];

  for (const file of required) {
    const fullPath = path.join(scriptDir, file);
    if (!existsSync(fullPath)) {
      throw new Error(`Missing required script: ${fullPath}`);
    }
  }
}

function main(): void {
  if (!process.env.PRIVATE_KEY) {
    throw new Error("PRIVATE_KEY is required. Export PRIVATE_KEY, then rerun setup.");
  }

  ensureRequiredFiles();

  console.log("[setup] 1/3 Sending initial pulse...");
  const firstPulse = run("bash", ["scripts/pulse.sh"]);
  assertSuccess(firstPulse, "Initial pulse");
  const pulseOutput = getOutput(firstPulse);
  if (pulseOutput) {
    console.log(pulseOutput);
  }

  console.log("[setup] 2/3 Creating 6h heartbeat cron...");
  const createCron = run("openclaw", [
    "cron",
    "create",
    "--name",
    cronName,
    "--every",
    "6h",
    "--session",
    "isolated",
    "--message",
    cronMessage,
    "--timeout-seconds",
    "120",
  ]);

  if (createCron.status !== 0) {
    const createOutput = getOutput(createCron);
    if (/already exists/i.test(createOutput)) {
      console.log(`[setup] Cron already exists: ${cronName}`);
    } else {
      assertSuccess(createCron, "Cron creation");
    }
  } else {
    const createOutput = getOutput(createCron);
    if (createOutput) {
      console.log(createOutput);
    }
  }

  console.log("[setup] 3/3 Confirming cron registration...");
  const cronList = run("openclaw", ["cron", "list"]);
  assertSuccess(cronList, "Cron verification");

  const listOutput = getOutput(cronList);
  if (!listOutput.includes(cronName)) {
    throw new Error(`Cron \"${cronName}\" was not found in openclaw cron list output.`);
  }

  console.log(`[setup] ✅ Complete. ${cronName} is active and scheduled every 6h.`);
}

try {
  main();
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`[setup] ❌ ${message}`);
  process.exit(1);
}
