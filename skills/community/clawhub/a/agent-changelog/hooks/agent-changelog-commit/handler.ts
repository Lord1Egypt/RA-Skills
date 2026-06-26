import { execSync } from "node:child_process";
import {
  appendFileSync,
  existsSync,
  mkdirSync,
  readFileSync,
  rmdirSync,
  unlinkSync,
} from "node:fs";
import { join } from "node:path";

function run(cmd: string, cwd: string): string {
  try {
    return execSync(cmd, { cwd, encoding: "utf-8", timeout: 15_000 }).trim();
  } catch {
    return "";
  }
}

function getTracked(workspace: string): string[] {
  const cfgPath = join(workspace, ".agent-changelog.json");
  try {
    const cfg = JSON.parse(readFileSync(cfgPath, "utf-8"));
    if (Array.isArray(cfg.tracked) && cfg.tracked.length > 0) return cfg.tracked;
  } catch {}
  return [];
}

async function acquireLock(lockDir: string): Promise<boolean> {
  for (let i = 0; i < 50; i++) {
    try {
      mkdirSync(lockDir);
      return true;
    } catch {
      await new Promise((r) => setTimeout(r, 100));
    }
  }
  return false;
}

const handler = async (event: any) => {
  if (event.type !== "message" || event.action !== "sent") return;

  const workspace =
    process.env.OPENCLAW_WORKSPACE ?? `${process.env.HOME}/.openclaw/workspace`;

  if (!existsSync(join(workspace, ".git"))) return;

  const lockDir = join(workspace, ".version-lock");
  const acquired = await acquireLock(lockDir);
  if (!acquired) {
    console.error("[agent-changelog-commit] Could not acquire lock, skipping");
    return;
  }

  try {
    // Detect changes since the last git add (working tree vs index).
    const changed = run("git diff --name-only", workspace)
      .split("\n")
      .filter(Boolean);

    if (changed.length === 0) return;

    // Read sender identity written by the capture hook
    let user = "unknown";
    let userId = "unknown";
    let channel = "unknown";
    const ctxPath = join(workspace, ".version-context");
    if (existsSync(ctxPath)) {
      try {
        const ctx = JSON.parse(readFileSync(ctxPath, "utf-8"));
        user = ctx.user ?? "unknown";
        userId = ctx.userId ?? "unknown";
        channel = ctx.channel ?? "unknown";
      } catch {}
    }

    // Append entry to pending log
    const entry = JSON.stringify({ ts: Date.now(), user, userId, channel, files: changed });
    appendFileSync(join(workspace, "pending_commits.jsonl"), entry + "\n");

    // Stage tracked files
    for (const f of getTracked(workspace)) {
      run(`git add "${f}" 2>/dev/null || true`, workspace);
    }
  } catch (err) {
    console.error(
      "[agent-changelog-commit] Error:",
      err instanceof Error ? err.message : String(err)
    );
  } finally {
    try { rmdirSync(lockDir); } catch {}
    try { unlinkSync(join(workspace, ".version-context")); } catch {}
  }
};

export default handler;
