#!/usr/bin/env node
import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { ensureStateDir, isProcessAlive, paths, readJson, updateStatus, writeJsonAtomic } from "./common.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const HEARTBEAT_STALE_MS = 90_000;

async function main() {
  await ensureStateDir();

  const pidInfo = await readJson(paths.pid, {});
  const status = await readJson(paths.status, {});
  const pid = typeof pidInfo.pid === "number" ? pidInfo.pid : 0;
  const heartbeatAt = typeof status.heartbeatAt === "string" ? Date.parse(status.heartbeatAt) : 0;
  const isHealthy = isProcessAlive(pid) && heartbeatAt > 0 && Date.now() - heartbeatAt < HEARTBEAT_STALE_MS;

  if (isHealthy) {
    process.exit(0);
  }

  const child = spawn(process.execPath, [path.join(__dirname, "realtime.mjs")], {
    detached: true,
    stdio: "ignore",
    env: process.env,
  });

  child.unref();

  await writeJsonAtomic(paths.pid, {
    pid: child.pid,
    startedAt: new Date().toISOString(),
  });

  await updateStatus({
    state: "starting",
    mode: process.env.FEEDTO_DISABLE_REALTIME === "1" ? "polling" : "realtime",
    message: "Bootstrapped FeedTo background listener",
    heartbeatAt: new Date().toISOString(),
  });
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
