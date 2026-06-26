import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { appConfig } from "../config.js";
import type { RuntimeLogEvent, ToolName } from "../types.js";

function ensureLogDirectory(): void {
  fs.mkdirSync(path.dirname(appConfig.runtime.logPath), { recursive: true });
}

export function createRequestId(): string {
  return crypto.randomUUID();
}

export function logEvent(
  requestId: string,
  action: ToolName,
  status: string,
  details: Record<string, unknown>
): void {
  ensureLogDirectory();
  const event: RuntimeLogEvent = {
    requestId,
    action,
    status,
    timestamp: new Date().toISOString(),
    details
  };

  fs.appendFileSync(appConfig.runtime.logPath, `${JSON.stringify(event)}\n`, "utf8");
}

export function readLogEvents(): RuntimeLogEvent[] {
  if (!fs.existsSync(appConfig.runtime.logPath)) {
    return [];
  }

  const content = fs.readFileSync(appConfig.runtime.logPath, "utf8");
  return content
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      try {
        return JSON.parse(line) as RuntimeLogEvent;
      } catch {
        return undefined;
      }
    })
    .filter((event): event is RuntimeLogEvent => Boolean(event));
}
