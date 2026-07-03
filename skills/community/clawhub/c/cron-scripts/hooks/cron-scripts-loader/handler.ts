import { readdir, readFile, stat } from "node:fs/promises";
import { watch, existsSync, mkdirSync } from "node:fs";
import { join, basename } from "node:path";
import { homedir } from "node:os";
import { spawn } from "node:child_process";
import { createRequire } from "node:module";

// Uses croner from OpenClaw's own node_modules — no extra install needed.
// Tested against OpenClaw 2026.x. If the path moves, update this line.
const _require = createRequire(import.meta.url);
const { Cron } = _require("/app/node_modules/croner/dist/croner.cjs");

const SCRIPTS_DIR = join(homedir(), ".openclaw/cron-scripts");
const DEFAULT_TZ = "UTC";
const DEFAULT_TIMEOUT_S = 120;
const LOG_PREFIX = "[cron-scripts-loader]";

interface ScriptMeta {
  schedule: string;
  name: string;
  tz: string;
  timeoutMs: number;
  filePath: string;
}

// Active jobs: filename → croner instance
const activeJobs = new Map<string, any>();

// ─── Frontmatter parser ────────────────────────────────────────────────────

function parseMeta(content: string, filePath: string): ScriptMeta | null {
  const lines = content.split("\n").slice(0, 20);
  const meta: Record<string, string> = {};

  for (const line of lines) {
    const m = line.match(/^#\s*(schedule|name|tz|timeout)\s*:\s*(.+)$/i);
    if (m) meta[m[1].toLowerCase()] = m[2].trim();
  }

  if (!meta.schedule) {
    console.warn(`${LOG_PREFIX} No "# schedule:" in ${basename(filePath)}, skipping`);
    return null;
  }

  const timeoutSec = meta.timeout ? parseInt(meta.timeout, 10) : DEFAULT_TIMEOUT_S;

  return {
    schedule: meta.schedule,
    name: meta.name || basename(filePath, ".sh"),
    tz: meta.tz || DEFAULT_TZ,
    timeoutMs: (isNaN(timeoutSec) ? DEFAULT_TIMEOUT_S : timeoutSec) * 1000,
    filePath,
  };
}

// ─── Script runner ─────────────────────────────────────────────────────────

function runScript(meta: ScriptMeta): void {
  const label = `${LOG_PREFIX}[${meta.name}]`;
  console.log(`${label} Starting run`);

  let timedOut = false;
  const child = spawn("bash", [meta.filePath], {
    stdio: ["ignore", "pipe", "pipe"],
    env: { ...process.env },
  });

  const timer = setTimeout(() => {
    timedOut = true;
    child.kill("SIGTERM");
    console.error(`${label} Timed out after ${meta.timeoutMs / 1000}s — killed`);
  }, meta.timeoutMs);

  child.stdout.on("data", (d: Buffer) => {
    for (const line of d.toString().trimEnd().split("\n")) {
      if (line) console.log(`${label} ${line}`);
    }
  });

  child.stderr.on("data", (d: Buffer) => {
    for (const line of d.toString().trimEnd().split("\n")) {
      if (line) console.error(`${label} STDERR: ${line}`);
    }
  });

  child.on("error", (err: Error) => {
    clearTimeout(timer);
    console.error(`${label} Spawn error (non-fatal): ${err.message}`);
  });

  child.on("close", (code: number | null) => {
    clearTimeout(timer);
    if (!timedOut) {
      if (code === 0) {
        console.log(`${label} Finished ok (exit 0)`);
      } else {
        console.error(`${label} Finished with exit code ${code}`);
      }
    }
  });
}

// ─── Job lifecycle ─────────────────────────────────────────────────────────

function stopJob(filename: string): void {
  const job = activeJobs.get(filename);
  if (job) {
    try { job.stop(); } catch { /* ignore */ }
    activeJobs.delete(filename);
    console.log(`${LOG_PREFIX} Stopped job: ${filename}`);
  }
}

async function loadJob(filename: string): Promise<void> {
  if (!filename.endsWith(".sh")) return;

  const filePath = join(SCRIPTS_DIR, filename);

  try {
    await stat(filePath);
  } catch {
    return;
  }

  let content: string;
  try {
    content = await readFile(filePath, "utf8");
  } catch (err: any) {
    console.error(`${LOG_PREFIX} Cannot read ${filename}: ${err.message}`);
    return;
  }

  const meta = parseMeta(content, filePath);
  if (!meta) return;

  stopJob(filename);

  try {
    const job = new Cron(
      meta.schedule,
      { timezone: meta.tz, protect: true },
      () => {
        try {
          runScript(meta);
        } catch (err: any) {
          console.error(`${LOG_PREFIX}[${meta.name}] Unexpected run error: ${err.message}`);
        }
      }
    );
    activeJobs.set(filename, job);
    const next = job.nextRun();
    console.log(
      `${LOG_PREFIX} Scheduled "${meta.name}" (${meta.schedule} ${meta.tz}) — next: ${next?.toISOString() ?? "n/a"}`
    );
  } catch (err: any) {
    console.error(`${LOG_PREFIX} Failed to schedule ${filename}: ${err.message}`);
  }
}

// ─── Directory watcher ─────────────────────────────────────────────────────

function watchDir(): void {
  const debounceTimers = new Map<string, ReturnType<typeof setTimeout>>();

  watch(SCRIPTS_DIR, (event, filename) => {
    if (!filename || !filename.endsWith(".sh")) return;

    const existing = debounceTimers.get(filename);
    if (existing) clearTimeout(existing);

    const timer = setTimeout(async () => {
      debounceTimers.delete(filename);
      const filePath = join(SCRIPTS_DIR, filename);
      if (existsSync(filePath)) {
        console.log(`${LOG_PREFIX} File changed: ${filename} — reloading`);
        await loadJob(filename);
      } else {
        console.log(`${LOG_PREFIX} File removed: ${filename} — stopping`);
        stopJob(filename);
      }
    }, 300);

    debounceTimers.set(filename, timer);
  });

  console.log(`${LOG_PREFIX} Watching ${SCRIPTS_DIR} for changes`);
}

// ─── Entry point ───────────────────────────────────────────────────────────

const handler = async (event: { type: string; action: string }) => {
  if (event.type !== "gateway" || event.action !== "startup") return;

  try {
    if (!existsSync(SCRIPTS_DIR)) {
      mkdirSync(SCRIPTS_DIR, { recursive: true });
      console.log(`${LOG_PREFIX} Created ${SCRIPTS_DIR}`);
    }

    let files: string[];
    try {
      files = await readdir(SCRIPTS_DIR);
    } catch (err: any) {
      console.error(`${LOG_PREFIX} Cannot read scripts dir: ${err.message}`);
      return;
    }

    const scripts = files.filter((f) => f.endsWith(".sh"));
    console.log(`${LOG_PREFIX} Found ${scripts.length} script(s) in ${SCRIPTS_DIR}`);

    for (const filename of scripts) {
      await loadJob(filename);
    }

    watchDir();
  } catch (err: any) {
    // Never crash the gateway
    console.error(`${LOG_PREFIX} Init error (non-fatal): ${err?.message ?? err}`);
  }
};

export default handler;
