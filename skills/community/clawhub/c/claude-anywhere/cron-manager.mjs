#!/usr/bin/env node
/**
 * cron-manager.mjs — Scheduled task manager for Claude Anywhere
 *
 * Features:
 *   - Recurring jobs (cron expressions via node-cron)
 *   - One-time jobs (runAt timestamp)
 *   - Persistence to ~/.claude-anywhere/cron-jobs.json
 *   - Executes claude -p <prompt> and returns result via onResult callback
 *   - Per-user limit of 10 jobs
 *   - 15-minute timeout per job execution
 */

import cron from "node-cron";
import { spawn } from "child_process";
import { randomUUID } from "crypto";
import {
  writeFileSync, readFileSync, existsSync, mkdirSync,
} from "fs";
import { join } from "path";
import { homedir } from "os";

const CRON_JOBS_FILE = join(homedir(), ".claude-anywhere", "cron-jobs.json");
const MAX_JOBS_PER_USER = 10;
const JOB_TIMEOUT_MS = 15 * 60 * 1000; // 15 minutes
const MAX_STDERR_LEN = 1000;

const logger = {
  info:  (...a) => console.log( new Date().toISOString(), "[CRON]",  ...a),
  warn:  (...a) => console.warn( new Date().toISOString(), "[CRON]",  ...a),
  error: (...a) => console.error(new Date().toISOString(), "[CRON]", ...a),
};

export class CronManager {
  /**
   * @param {object} opts
   * @param {string} opts.claudePath  - path to claude binary
   * @param {string} opts.claudeCwd   - working directory for claude
   * @param {function} opts.onResult  - callback(jobId, jobName, userId, result)
   */
  constructor({ claudePath, claudeCwd, onResult }) {
    this.claudePath = claudePath || "claude";
    this.claudeCwd  = claudeCwd  || process.cwd();
    this.onResult   = onResult   || (() => {});

    // Map<jobId, node-cron task or setTimeout handle>
    this._handles = new Map();

    // Ensure storage directory exists
    mkdirSync(join(homedir(), ".claude-anywhere"), { recursive: true });

    // Load persisted jobs
    this._jobs = this._load();
  }

  // ============ Persistence ============

  _load() {
    try {
      if (existsSync(CRON_JOBS_FILE)) {
        return JSON.parse(readFileSync(CRON_JOBS_FILE, "utf-8"));
      }
    } catch (e) {
      logger.warn("Failed to load cron jobs:", e.message);
    }
    return [];
  }

  _save() {
    try {
      writeFileSync(CRON_JOBS_FILE, JSON.stringify(this._jobs, null, 2));
    } catch (e) {
      logger.warn("Failed to save cron jobs:", e.message);
    }
  }

  // ============ Natural language parsing ============

  /**
   * Parse a natural language description into a scheduled task spec.
   * Calls claude -p with a lightweight model (--model sonnet) for fast, cheap parsing.
   * @param {string} userInput  - Raw user description, e.g. "每天早上9点检查服务器"
   * @returns {Promise<{ ok: boolean, parsed?: { type, schedule, prompt, name }, error?: string }>}
   */
  parseNaturalLanguage(userInput) {
    const PARSE_TIMEOUT_MS = 30_000;
    const now = new Date().toISOString();

    const systemPrompt = `You are a cron job parser. Parse the following natural language request into a scheduled task.

User request: "${userInput.replace(/"/g, '\\"')}"
Current time: ${now}
Timezone: Asia/Shanghai

Respond in JSON only, no other text:
{
  "type": "cron" or "once",
  "schedule": "cron expression (5 fields)" or "ISO 8601 datetime for once",
  "prompt": "the task/prompt to execute at scheduled time",
  "name": "short name for the task (max 20 chars)"
}

Examples:
- "每天早上9点检查服务器" → {"type":"cron","schedule":"0 9 * * *","prompt":"检查服务器状态并汇报","name":"检查服务器"}
- "30分钟后提醒我开会" → {"type":"once","schedule":"${this._addMinutes(now, 30)}","prompt":"提醒：该开会了","name":"开会提醒"}
- "every weekday at 8pm sync data" → {"type":"cron","schedule":"0 20 * * 1-5","prompt":"sync data","name":"sync data"}`;

    return new Promise((resolve) => {
      const args = [
        "-p", systemPrompt,
        "--max-turns", "1",
        "--output-format", "text",
        "--model", "sonnet",
        "--dangerously-skip-permissions",
      ];

      const proc = spawn(this.claudePath, args, {
        cwd: this.claudeCwd,
        env: { ...process.env },
        stdio: ["pipe", "pipe", "pipe"],
      });

      let stdout = "";
      let stderr = "";
      let timedOut = false;

      const timer = setTimeout(() => {
        timedOut = true;
        proc.kill("SIGTERM");
        logger.warn("Natural language parse timed out after 30s");
      }, PARSE_TIMEOUT_MS);

      proc.stdout.on("data", c => { stdout += c.toString(); });
      proc.stderr.on("data", c => { if (stderr.length < MAX_STDERR_LEN) stderr += c.toString(); });

      proc.on("close", code => {
        clearTimeout(timer);
        proc.stdout.removeAllListeners();
        proc.stderr.removeAllListeners();
        proc.removeAllListeners();

        if (timedOut) {
          resolve({ ok: false, error: "Parse timed out (30s). Please try again." });
          return;
        }

        const raw = stdout.trim();
        if (!raw) {
          logger.error(`Parse claude exit ${code}: ${stderr.slice(0, 200)}`);
          resolve({ ok: false, error: "No response from Claude. Please try again." });
          return;
        }

        // Extract JSON from response (may be wrapped in markdown code block)
        const jsonMatch = raw.match(/```(?:json)?\s*([\s\S]*?)```/) || [null, raw];
        const jsonStr = jsonMatch[1].trim();

        try {
          const parsed = JSON.parse(jsonStr);
          if (!parsed.type || !parsed.schedule || !parsed.prompt || !parsed.name) {
            resolve({ ok: false, error: "Could not understand your request. Please describe it differently." });
            return;
          }
          resolve({ ok: true, parsed });
        } catch {
          logger.warn(`Parse JSON failed, raw: ${raw.slice(0, 200)}`);
          resolve({ ok: false, error: "Could not understand your request. Please describe it differently." });
        }
      });

      proc.on("error", err => {
        clearTimeout(timer);
        proc.stdout.removeAllListeners();
        proc.stderr.removeAllListeners();
        proc.removeAllListeners();
        resolve({ ok: false, error: `Failed to start Claude: ${err.message}` });
      });

      proc.stdin.end();
    });
  }

  /** Helper: add minutes to an ISO string, returns new ISO string */
  _addMinutes(isoStr, minutes) {
    return new Date(new Date(isoStr).getTime() + minutes * 60_000).toISOString();
  }

  // ============ Claude execution ============

  _runClaude(prompt) {
    return new Promise((resolve) => {
      const knowledgeDirs = (process.env.KNOWLEDGE_DIR || "").split(",").map(d => d.trim()).filter(Boolean);
      const args = [
        "-p", prompt,
        "--max-turns", "100",
        "--output-format", "json",
        "--dangerously-skip-permissions",
        ...knowledgeDirs.flatMap(d => ["--add-dir", d]),
      ];

      const proc = spawn(this.claudePath, args, {
        cwd: this.claudeCwd,
        env: { ...process.env },
        stdio: ["pipe", "pipe", "pipe"],
      });

      let stdout = "";
      let stderr = "";
      let timedOut = false;

      const timer = setTimeout(() => {
        timedOut = true;
        proc.kill("SIGTERM");
        logger.warn(`Claude timed out after ${JOB_TIMEOUT_MS / 1000}s`);
      }, JOB_TIMEOUT_MS);

      proc.stdout.on("data", c => { stdout += c.toString(); });
      proc.stderr.on("data", c => { if (stderr.length < MAX_STDERR_LEN) stderr += c.toString(); });

      proc.on("close", code => {
        clearTimeout(timer);
        proc.stdout.removeAllListeners();
        proc.stderr.removeAllListeners();
        proc.removeAllListeners();

        if (timedOut) {
          resolve({ text: "⚠️ Job timed out (15 min limit reached)", ok: false });
          return;
        }

        if (code === 0 || stdout.trim()) {
          try {
            const json = JSON.parse(stdout.trim());
            resolve({ text: json.result || json.text || stdout.trim(), ok: true });
          } catch {
            resolve({ text: stdout.trim(), ok: true });
          }
        } else {
          logger.error(`Claude exit ${code}: ${stderr.slice(0, 200)}`);
          resolve({ text: `⚠️ Claude error (code=${code})`, ok: false });
        }
      });

      proc.on("error", err => {
        clearTimeout(timer);
        proc.stdout.removeAllListeners();
        proc.stderr.removeAllListeners();
        proc.removeAllListeners();
        resolve({ text: `⚠️ Failed to start Claude: ${err.message}`, ok: false });
      });

      proc.stdin.end();
    });
  }

  // ============ Job execution ============

  async _executeJob(job) {
    logger.info(`Executing job [${job.id.slice(0, 8)}] "${job.name}" for user ${job.userId}`);
    const result = await this._runClaude(job.prompt);
    logger.info(`Job [${job.id.slice(0, 8)}] done: ${result.text.length} chars`);

    try {
      await this.onResult(job.id, job.name, job.userId, result.text);
    } catch (e) {
      logger.error(`onResult callback error for job ${job.id}:`, e.message);
    }

    // If one-time job, remove after execution
    if (job.type === "once") {
      this.remove(job.id);
    }
  }

  // ============ Schedule a cron job ============

  _scheduleRecurring(job) {
    if (!cron.validate(job.schedule)) {
      logger.warn(`Invalid cron expression for job ${job.id}: "${job.schedule}"`);
      return false;
    }

    const task = cron.schedule(job.schedule, () => {
      this._executeJob(job).catch(e => logger.error(`Job execution error [${job.id}]:`, e.message));
    }, {
      scheduled: true,
      timezone: process.env.TZ || "Asia/Shanghai",
    });

    this._handles.set(job.id, task);
    logger.info(`Scheduled recurring job [${job.id.slice(0, 8)}] "${job.name}" @ "${job.schedule}"`);
    return true;
  }

  // ============ Schedule a one-time job ============

  _scheduleOnce(job) {
    const delay = new Date(job.runAt).getTime() - Date.now();
    if (delay < 0) {
      logger.warn(`One-time job ${job.id} is in the past, skipping`);
      return false;
    }

    const handle = setTimeout(() => {
      this._executeJob(job).catch(e => logger.error(`Job execution error [${job.id}]:`, e.message));
    }, delay);

    this._handles.set(job.id, handle);
    logger.info(`Scheduled once job [${job.id.slice(0, 8)}] "${job.name}" at ${job.runAt} (in ${Math.round(delay / 1000)}s)`);
    return true;
  }

  // ============ Public API ============

  /**
   * Add a recurring cron job.
   * @param {object} params
   * @param {string} [params.id]        - UUID (auto-generated if omitted)
   * @param {string} params.name        - Human-readable name
   * @param {string} params.schedule    - Cron expression (e.g. "0 9 * * *")
   * @param {string} params.prompt      - Prompt to send to Claude
   * @param {string} params.userId      - User ID (for routing result)
   * @returns {{ ok: boolean, job?: object, error?: string }}
   */
  add({ id, name, schedule, prompt, userId }) {
    if (!cron.validate(schedule)) {
      return { ok: false, error: `Invalid cron expression: "${schedule}"` };
    }

    const userJobs = this._jobs.filter(j => j.userId === userId);
    if (userJobs.length >= MAX_JOBS_PER_USER) {
      return { ok: false, error: `Maximum ${MAX_JOBS_PER_USER} jobs per user reached` };
    }

    const job = {
      id:        id || randomUUID(),
      name:      name || prompt.slice(0, 30),
      schedule,
      prompt,
      userId,
      type:      "cron",
      createdAt: Date.now(),
    };

    this._jobs.push(job);
    this._save();
    this._scheduleRecurring(job);

    return { ok: true, job };
  }

  /**
   * Add a one-time job.
   * @param {object} params
   * @param {string} [params.id]
   * @param {string} params.name
   * @param {string} params.runAt    - ISO datetime string or "+Xm/+Xh/+Xd"
   * @param {string} params.prompt
   * @param {string} params.userId
   * @returns {{ ok: boolean, job?: object, error?: string }}
   */
  addOnce({ id, name, runAt, prompt, userId }) {
    // Resolve relative time
    const resolvedAt = parseRunAt(runAt);
    if (!resolvedAt) {
      return { ok: false, error: `Invalid time format: "${runAt}"` };
    }

    if (new Date(resolvedAt).getTime() <= Date.now()) {
      return { ok: false, error: "Scheduled time must be in the future" };
    }

    const userJobs = this._jobs.filter(j => j.userId === userId);
    if (userJobs.length >= MAX_JOBS_PER_USER) {
      return { ok: false, error: `Maximum ${MAX_JOBS_PER_USER} jobs per user reached` };
    }

    const job = {
      id:        id || randomUUID(),
      name:      name || prompt.slice(0, 30),
      runAt:     resolvedAt,
      prompt,
      userId,
      type:      "once",
      createdAt: Date.now(),
    };

    this._jobs.push(job);
    this._save();
    this._scheduleOnce(job);

    return { ok: true, job };
  }

  /**
   * List jobs for a user.
   * @param {string} userId
   * @returns {object[]}
   */
  list(userId) {
    return this._jobs.filter(j => j.userId === userId);
  }

  /**
   * Remove a job by ID.
   * @param {string} jobId
   * @returns {boolean} true if removed
   */
  remove(jobId) {
    const idx = this._jobs.findIndex(j => j.id === jobId);
    if (idx === -1) return false;

    // Stop the scheduled task
    const handle = this._handles.get(jobId);
    if (handle) {
      if (typeof handle.stop === "function") {
        handle.stop(); // node-cron task
      } else {
        clearTimeout(handle); // setTimeout handle
      }
      this._handles.delete(jobId);
    }

    this._jobs.splice(idx, 1);
    this._save();
    logger.info(`Removed job [${jobId.slice(0, 8)}]`);
    return true;
  }

  /**
   * Start all persisted jobs (call once at startup).
   */
  start() {
    const now = Date.now();
    let started = 0;
    let skipped = 0;

    for (const job of this._jobs) {
      if (job.type === "cron") {
        if (this._scheduleRecurring(job)) started++;
        else skipped++;
      } else if (job.type === "once") {
        if (new Date(job.runAt).getTime() > now) {
          if (this._scheduleOnce(job)) started++;
          else skipped++;
        } else {
          // Past one-time jobs: remove silently
          logger.info(`Removing past one-time job [${job.id.slice(0, 8)}] "${job.name}"`);
          skipped++;
        }
      }
    }

    // Remove past one-time jobs from storage
    const before = this._jobs.length;
    this._jobs = this._jobs.filter(j => {
      if (j.type !== "once") return true;
      return new Date(j.runAt).getTime() > now;
    });
    if (this._jobs.length !== before) this._save();

    logger.info(`Started ${started} jobs, skipped/removed ${skipped}`);
  }
}

// ============ Helpers ============

/**
 * Parse a runAt string. Supports:
 *   - "+30m"  → 30 minutes from now
 *   - "+2h"   → 2 hours from now
 *   - "+1d"   → 1 day from now
 *   - ISO 8601 string (e.g. "2026-03-23T09:00:00" or "2026-03-23T09:00")
 * Returns ISO string or null.
 */
export function parseRunAt(input) {
  if (!input) return null;

  const rel = input.match(/^\+(\d+)(m|h|d)$/i);
  if (rel) {
    const amount = parseInt(rel[1], 10);
    const unit   = rel[2].toLowerCase();
    const ms     = unit === "m" ? amount * 60_000
                 : unit === "h" ? amount * 3_600_000
                 : /* d */        amount * 86_400_000;
    return new Date(Date.now() + ms).toISOString();
  }

  // Try ISO parse (allow "YYYY-MM-DDTHH:mm" without seconds)
  const d = new Date(input);
  if (!isNaN(d.getTime())) return d.toISOString();

  return null;
}

/**
 * Describe a cron expression in human-readable English.
 * Very basic — handles common patterns only.
 */
export function describeCron(expr) {
  const parts = expr.trim().split(/\s+/);
  if (parts.length < 5) return expr;
  const [min, hour, dom, , dow] = parts;

  if (dom === "*" && dow === "*") {
    if (min === "0" && /^\d+$/.test(hour)) return `daily at ${hour.padStart(2, "0")}:00`;
    if (/^\*\/(\d+)$/.test(min) && hour === "*") {
      const interval = min.match(/\*\/(\d+)/)[1];
      return `every ${interval} min`;
    }
    if (/^\d+$/.test(min) && /^\d+$/.test(hour)) return `daily at ${hour.padStart(2, "0")}:${min.padStart(2, "0")}`;
    return expr;
  }
  if (dow !== "*" && /^[0-6](-[0-6])?$/.test(dow)) {
    const days = { "1-5": "weekdays", "0": "Sun", "1": "Mon", "2": "Tue", "3": "Wed", "4": "Thu", "5": "Fri", "6": "Sat" };
    const dayStr = days[dow] || `dow ${dow}`;
    if (/^\d+$/.test(min) && /^\d+$/.test(hour)) {
      return `${dayStr} at ${hour.padStart(2, "0")}:${min.padStart(2, "0")}`;
    }
  }
  return expr;
}
