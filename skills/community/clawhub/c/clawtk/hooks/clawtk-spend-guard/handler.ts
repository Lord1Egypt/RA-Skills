import { readFileSync, appendFileSync, existsSync } from "fs";
import { join } from "path";
import { homedir } from "os";

// ── Types ───────────────────────────────────────────────────────────────────

interface ClawTKState {
  tier: "free" | "pro" | "cloud";
  spendCaps: {
    daily: number;
    weekly: number;
  };
  overrideUntil: string | null;
}

interface SpendEntry {
  timestamp: string;
  tokens: number;
  estimatedCost: number;
  toolName: string;
  toolCallHash: string;
}

interface ToolCallEvent {
  toolName: string;
  parameters: Record<string, unknown>;
  sessionId: string;
  tokensSoFar?: number;
}

interface HookResult {
  block?: boolean;
  blockReason?: string;
  warn?: boolean;
  message?: string;
}

// ── Config ──────────────────────────────────────────────────────────────────

const OPENCLAW_DIR = join(homedir(), ".openclaw");
const STATE_FILE = join(OPENCLAW_DIR, "clawtk-state.json");
const SPEND_LOG = join(OPENCLAW_DIR, "clawtk-spend.jsonl");

// Retry loop detection: same tool call pattern N times within this window
const RETRY_LOOP_THRESHOLD = 3;
const RETRY_LOOP_WINDOW_MS = 60_000;

// Cost estimation: rough tokens-per-tool-call average
// Actual costs depend on model, but this gives a ballpark for cap enforcement
const AVG_TOKENS_PER_TOOL_CALL = 2000;
const COST_PER_1K_TOKENS = 0.003; // ~$3/M tokens blended average

// ── Helpers ─────────────────────────────────────────────────────────────────

function loadState(): ClawTKState | null {
  if (!existsSync(STATE_FILE)) return null;
  try {
    return JSON.parse(readFileSync(STATE_FILE, "utf-8"));
  } catch {
    return null;
  }
}

function hashToolCall(event: ToolCallEvent): string {
  const key = `${event.toolName}:${JSON.stringify(event.parameters)}`;
  let hash = 0;
  for (let i = 0; i < key.length; i++) {
    const char = key.charCodeAt(i);
    hash = ((hash << 5) - hash + char) | 0;
  }
  return hash.toString(36);
}

function loadRecentSpend(): SpendEntry[] {
  if (!existsSync(SPEND_LOG)) return [];

  try {
    const lines = readFileSync(SPEND_LOG, "utf-8").trim().split("\n");
    const now = Date.now();
    const weekAgo = now - 7 * 24 * 60 * 60 * 1000;

    return lines
      .filter((line) => line.trim())
      .map((line) => {
        try {
          return JSON.parse(line) as SpendEntry;
        } catch {
          return null;
        }
      })
      .filter((entry): entry is SpendEntry => {
        if (!entry) return false;
        return new Date(entry.timestamp).getTime() > weekAgo;
      });
  } catch {
    return [];
  }
}

function logSpend(entry: SpendEntry): void {
  appendFileSync(SPEND_LOG, JSON.stringify(entry) + "\n");
}

function isOverrideActive(state: ClawTKState): boolean {
  if (!state.overrideUntil) return false;
  return new Date(state.overrideUntil).getTime() > Date.now();
}

// ── Retry Loop Detection ────────────────────────────────────────────────────

function detectRetryLoop(
  entries: SpendEntry[],
  currentHash: string
): boolean {
  const now = Date.now();
  const recentSame = entries.filter(
    (e) =>
      e.toolCallHash === currentHash &&
      now - new Date(e.timestamp).getTime() < RETRY_LOOP_WINDOW_MS
  );
  return recentSame.length >= RETRY_LOOP_THRESHOLD;
}

// ── Spend Cap Check ─────────────────────────────────────────────────────────

function checkSpendCaps(
  entries: SpendEntry[],
  caps: ClawTKState["spendCaps"]
): { exceeded: boolean; level: "ok" | "warning" | "exceeded"; detail: string } {
  const now = Date.now();
  const dayAgo = now - 24 * 60 * 60 * 1000;
  const weekAgo = now - 7 * 24 * 60 * 60 * 1000;

  const dailySpend = entries
    .filter((e) => new Date(e.timestamp).getTime() > dayAgo)
    .reduce((sum, e) => sum + e.estimatedCost, 0);

  const weeklySpend = entries
    .filter((e) => new Date(e.timestamp).getTime() > weekAgo)
    .reduce((sum, e) => sum + e.estimatedCost, 0);

  if (dailySpend >= caps.daily) {
    return {
      exceeded: true,
      level: "exceeded",
      detail: `Daily spend cap reached: $${dailySpend.toFixed(2)} / $${caps.daily} limit. Run /clawtk override for a 1-hour bypass.`,
    };
  }

  if (weeklySpend >= caps.weekly) {
    return {
      exceeded: true,
      level: "exceeded",
      detail: `Weekly spend cap reached: $${weeklySpend.toFixed(2)} / $${caps.weekly} limit. Run /clawtk override for a 1-hour bypass.`,
    };
  }

  if (dailySpend >= caps.daily * 0.8) {
    return {
      exceeded: false,
      level: "warning",
      detail: `Approaching daily cap: $${dailySpend.toFixed(2)} / $${caps.daily} (${Math.round((dailySpend / caps.daily) * 100)}%)`,
    };
  }

  return { exceeded: false, level: "ok", detail: "" };
}

// ── Main Hook Handler ───────────────────────────────────────────────────────

export default function handler(event: ToolCallEvent): HookResult {
  const state = loadState();
  if (!state) return {}; // ClawTK not set up, pass through

  const callHash = hashToolCall(event);
  const entries = loadRecentSpend();

  // Check for retry loops (always active, even during override)
  if (detectRetryLoop(entries, callHash)) {
    return {
      block: true,
      blockReason: `ClawTK: Retry loop detected — "${event.toolName}" called ${RETRY_LOOP_THRESHOLD}+ times in ${RETRY_LOOP_WINDOW_MS / 1000}s. This pattern can burn hundreds of dollars. The loop has been stopped. If this was intentional, run /clawtk override to continue.`,
    };
  }

  // Log this tool call
  const estimatedCost =
    (AVG_TOKENS_PER_TOOL_CALL / 1000) * COST_PER_1K_TOKENS;

  logSpend({
    timestamp: new Date().toISOString(),
    tokens: AVG_TOKENS_PER_TOOL_CALL,
    estimatedCost,
    toolName: event.toolName,
    toolCallHash: callHash,
  });

  // Skip cap check if override is active
  if (isOverrideActive(state)) return {};

  // Check spend caps
  const capStatus = checkSpendCaps(entries, state.spendCaps);

  if (capStatus.exceeded) {
    return {
      block: true,
      blockReason: `ClawTK: ${capStatus.detail}`,
    };
  }

  if (capStatus.level === "warning") {
    return {
      warn: true,
      message: `ClawTK: ${capStatus.detail}`,
    };
  }

  return {};
}
