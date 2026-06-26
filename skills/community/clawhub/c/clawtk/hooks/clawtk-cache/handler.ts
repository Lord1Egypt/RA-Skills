import { readFileSync, writeFileSync, existsSync } from "fs";
import { join } from "path";
import { homedir } from "os";
import { execFileSync } from "child_process";

// ── Types ───────────────────────────────────────────────────────────────────

interface ClawTKState {
  tier: "free" | "pro" | "cloud";
}

interface ToolCallEvent {
  event: "before_tool_call" | "tool_result_persist";
  toolName: string;
  parameters: Record<string, unknown>;
  sessionId: string;
  result?: string;
}

interface HookResult {
  cached?: boolean;
  cachedResult?: string;
  skip?: boolean;
  message?: string;
}

// ── Config ──────────────────────────────────────────────────────────────────

const OPENCLAW_DIR = join(homedir(), ".openclaw");
const STATE_FILE = join(OPENCLAW_DIR, "clawtk-state.json");
const CACHE_DB = join(OPENCLAW_DIR, "clawtk-cache.db");

const MAX_CACHE_ENTRIES = 5000;

// Tools that are safe to cache (read-only, deterministic for a given state)
const CACHEABLE_TOOLS = new Set([
  "read_file",
  "list_directory",
  "search_files",
  "glob",
  "grep",
  "bash",
]);

// Bash commands safe to cache (read-only)
const CACHEABLE_BASH_PATTERNS = [
  /^(ls|tree|find|wc|du|df|cat|head|tail|file|stat)\b/,
  /^git\s+(status|log|diff|show|branch|tag|remote)\b/,
  /^(npm|yarn|pnpm)\s+(list|ls|outdated|info)\b/,
  /^(python|node|ruby|go)\s+--version\b/,
  /^(which|where|type|command\s+-v)\b/,
  /^rtk\b/,
];

// Bash commands that must NEVER be cached (side effects)
const UNCACHEABLE_BASH_PATTERNS = [
  /^(rm|mv|cp|mkdir|touch|chmod|chown)\b/,
  /^git\s+(add|commit|push|pull|checkout|merge|rebase|reset)\b/,
  /^(npm|yarn|pnpm)\s+(install|run|exec|publish)\b/,
  /\|/,
  />>?/,
  /&&/,
];

// ── Helpers ─────────────────────────────────────────────────────────────────

function loadState(): ClawTKState | null {
  if (!existsSync(STATE_FILE)) return null;
  try {
    return JSON.parse(readFileSync(STATE_FILE, "utf-8"));
  } catch {
    return null;
  }
}

function isPro(state: ClawTKState): boolean {
  return state.tier === "pro" || state.tier === "cloud";
}

function hashKey(toolName: string, params: Record<string, unknown>): string {
  const key = `${toolName}:${JSON.stringify(params, Object.keys(params).sort())}`;
  let hash = 0x811c9dc5;
  for (let i = 0; i < key.length; i++) {
    hash ^= key.charCodeAt(i);
    hash = (hash * 0x01000193) | 0;
  }
  return (hash >>> 0).toString(36);
}

function isCacheableBashCommand(command: string): boolean {
  const trimmed = command.trim();
  for (const pattern of UNCACHEABLE_BASH_PATTERNS) {
    if (pattern.test(trimmed)) return false;
  }
  for (const pattern of CACHEABLE_BASH_PATTERNS) {
    if (pattern.test(trimmed)) return true;
  }
  return false;
}

function isCacheable(
  toolName: string,
  params: Record<string, unknown>
): boolean {
  if (!CACHEABLE_TOOLS.has(toolName)) return false;
  if (toolName === "bash") {
    const command = (params.command as string) || "";
    return isCacheableBashCommand(command);
  }
  return true;
}

// ── SQLite Operations ───────────────────────────────────────────────────────
// Uses sqlite3 CLI via execFileSync (no shell injection risk) to avoid
// native module dependencies. Keeps the hook zero-dependency.

function sqlite3(sql: string): string {
  try {
    return execFileSync("sqlite3", ["-json", CACHE_DB, sql], {
      encoding: "utf-8",
      stdio: ["pipe", "pipe", "pipe"],
      timeout: 5000,
    }).trim();
  } catch {
    return "";
  }
}

function sqlite3Exec(sql: string): void {
  try {
    execFileSync("sqlite3", [CACHE_DB, sql], {
      stdio: "pipe",
      timeout: 5000,
    });
  } catch {
    // Non-fatal
  }
}

function ensureDb(): boolean {
  if (!existsSync(CACHE_DB)) {
    try {
      sqlite3Exec(`
        CREATE TABLE IF NOT EXISTS cache (
          hash TEXT PRIMARY KEY,
          tool_name TEXT NOT NULL,
          result TEXT NOT NULL,
          hit_count INTEGER DEFAULT 1,
          created_at TEXT DEFAULT (datetime('now')),
          last_hit TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_cache_tool ON cache(tool_name);
        CREATE INDEX IF NOT EXISTS idx_cache_created ON cache(created_at);
      `);
      return true;
    } catch {
      return false;
    }
  }
  return true;
}

function getCached(hash: string): string | null {
  const result = sqlite3(
    `SELECT result FROM cache WHERE hash = '${hash}' AND datetime(created_at) > datetime('now', '-4 hours') LIMIT 1`
  );
  if (!result || result === "[]") return null;

  try {
    const rows = JSON.parse(result);
    if (rows.length === 0) return null;

    // Bump hit count
    sqlite3Exec(
      `UPDATE cache SET hit_count = hit_count + 1, last_hit = datetime('now') WHERE hash = '${hash}'`
    );
    return rows[0].result;
  } catch {
    return null;
  }
}

function setCache(hash: string, toolName: string, result: string): void {
  // Write result to a temp file to avoid SQL injection from result content
  const tmpFile = join(OPENCLAW_DIR, `.clawtk-cache-tmp-${hash}`);
  try {
    writeFileSync(tmpFile, result, "utf-8");
    sqlite3Exec(
      `INSERT OR REPLACE INTO cache (hash, tool_name, result, hit_count, created_at, last_hit) VALUES ('${hash}', '${toolName}', readfile('${tmpFile}'), 1, datetime('now'), datetime('now'))`
    );
  } catch {
    // Non-fatal
  } finally {
    try {
      const { unlinkSync } = require("fs");
      unlinkSync(tmpFile);
    } catch {
      // cleanup failure is fine
    }
  }

  // Prune if over max
  sqlite3Exec(
    `DELETE FROM cache WHERE hash IN (SELECT hash FROM cache ORDER BY last_hit ASC LIMIT max(0, (SELECT count(*) FROM cache) - ${MAX_CACHE_ENTRIES}))`
  );
}

// ── Main Hook Handler ───────────────────────────────────────────────────────

export default function handler(event: ToolCallEvent): HookResult {
  const state = loadState();
  if (!state || !isPro(state)) return {};

  // Ensure sqlite3 CLI is available (declared as optionalBins in SKILL.md)
  try {
    execFileSync("which", ["sqlite3"], { stdio: "pipe" });
  } catch {
    // sqlite3 not installed — caching disabled, all other features work normally
    return {};
  }

  if (!ensureDb()) return {};

  const { toolName, parameters } = event;

  if (event.event === "before_tool_call") {
    if (!isCacheable(toolName, parameters)) return {};

    const hash = hashKey(toolName, parameters);
    const cached = getCached(hash);

    if (cached) {
      return {
        cached: true,
        cachedResult: cached,
        message: `[clawtk] Cache hit — saved ~${Math.round(cached.length / 4)} tokens`,
      };
    }
    return {};
  }

  if (event.event === "tool_result_persist") {
    if (!isCacheable(toolName, parameters)) return {};
    if (!event.result) return {};
    if (event.result.length > 50_000 || event.result.length < 10) return {};

    const hash = hashKey(toolName, parameters);
    setCache(hash, toolName, event.result);
    return {};
  }

  return {};
}
