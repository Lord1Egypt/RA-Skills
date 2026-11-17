import fs from "node:fs";
import { homedir } from "node:os";
import { dirname, join } from "node:path";
import type { Snapshot } from "../types";

/** Snapshot history: env override first, else ~/.check-ai-credits/log.json. */
export function logPath(): string {
  return process.env.CHECK_AI_CREDITS_LOG ?? join(homedir(), ".check-ai-credits", "log.json");
}

export function loadLog(path = logPath()): Snapshot[] {
  try {
    const parsed: unknown = JSON.parse(fs.readFileSync(path, "utf8"));
    return Array.isArray(parsed) ? (parsed as Snapshot[]) : [];
  } catch {
    return [];
  }
}

export function saveLog(entries: Snapshot[], path = logPath()): void {
  try {
    fs.mkdirSync(dirname(path), { recursive: true });
    fs.writeFileSync(path, `${JSON.stringify(entries, null, 2)}\n`, "utf8");
  } catch (err) {
    // logging must never break a check run
    process.stderr.write(`warn: could not write trend log at ${path}: ${(err as Error).message}\n`);
  }
}
