/**
 * tracking.ts — Persistence layer for tracking.json and runs.jsonl.
 *
 * `TrackingRepository` manages two runtime files under `.careerclaw/`:
 *
 *   tracking.json  — keyed object of TrackingEntry records, one per
 *                    saved job_id. First-seen wins for status; re-runs
 *                    update `last_seen_at` only.
 *
 *   runs.jsonl     — append-only newline-delimited JSON log; one
 *                    BriefingRun per line. Never rewritten, only grown.
 *
 * Dry-run mode: all write operations are no-ops. The repository is
 * fully functional for reads; callers can inspect what *would* have
 * been written via the return values of upsertEntry() / appendRun().
 *
 * The runtime directory is created automatically on first write if it
 * does not exist.
 */

import { readFileSync, writeFileSync, appendFileSync, mkdirSync, existsSync } from "fs";
import { dirname } from "path";
import type { TrackingEntry, BriefingRun, NormalizedJob, ScoredJob } from "./models.js";
import { TRACKING_PATH, RUNS_PATH } from "./config.js";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

/** In-memory store: job_id → TrackingEntry. */
type TrackingStore = Record<string, TrackingEntry>;

export interface UpsertResult {
  /** Number of new entries created this call. */
  created: number;
  /** Number of entries already present (last_seen_at updated). */
  already_present: number;
}

// ---------------------------------------------------------------------------
// TrackingRepository
// ---------------------------------------------------------------------------

export class TrackingRepository {
  private readonly trackingPath: string;
  private readonly runsPath: string;
  private readonly dryRun: boolean;

  constructor(options?: {
    trackingPath?: string;
    runsPath?: string;
    dryRun?: boolean;
  }) {
    this.trackingPath = options?.trackingPath ?? TRACKING_PATH;
    this.runsPath = options?.runsPath ?? RUNS_PATH;
    this.dryRun = options?.dryRun ?? false;
  }

  // -------------------------------------------------------------------------
  // Read
  // -------------------------------------------------------------------------

  /**
   * Load tracking.json from disk.
   * Returns an empty store when the file does not yet exist.
   */
  load(): TrackingStore {
    if (!existsSync(this.trackingPath)) return {};
    try {
      const raw = readFileSync(this.trackingPath, "utf8");
      return JSON.parse(raw) as TrackingStore;
    } catch {
      // Corrupt or unreadable file — start fresh rather than crashing.
      return {};
    }
  }

  // -------------------------------------------------------------------------
  // Write — tracking.json
  // -------------------------------------------------------------------------

  /**
   * Persist the in-memory store to tracking.json.
   * No-op in dry-run mode.
   */
  save(store: TrackingStore): void {
    if (this.dryRun) return;
    this.ensureDir(this.trackingPath);
    writeFileSync(this.trackingPath, JSON.stringify(store, null, 2), "utf8");
  }

  /**
   * Upsert a batch of jobs into the tracking store.
   *
   * Behaviour:
   *   - New job_id → creates a TrackingEntry with status "saved"
   *   - Existing job_id → updates last_seen_at only; status is preserved
   *
   * Writes the updated store to disk unless dry-run.
   * Returns counts of created vs already_present entries.
   */
  upsertEntries(
    jobs: NormalizedJob[],
    scored?: ScoredJob[]
  ): UpsertResult {
    const store = this.load();
    const now = new Date().toISOString();
    let created = 0;
    let already_present = 0;

    for (const job of jobs) {
      const existing = store[job.job_id];
      if (existing) {
        // Update last_seen_at; preserve all other fields including status.
        existing.last_seen_at = now;
        existing.updated_at = now;
        already_present++;
      } else {
        store[job.job_id] = makeEntry(job, now);
        created++;
      }
    }

    this.save(store);
    return { created, already_present };
  }

  // -------------------------------------------------------------------------
  // Write — runs.jsonl
  // -------------------------------------------------------------------------

  /**
   * Append a BriefingRun record to runs.jsonl.
   * Each call adds exactly one newline-terminated JSON line.
   * No-op in dry-run mode.
   */
  appendRun(run: BriefingRun): void {
    if (this.dryRun) return;
    this.ensureDir(this.runsPath);
    appendFileSync(this.runsPath, JSON.stringify(run) + "\n", "utf8");
  }

  // -------------------------------------------------------------------------
  // Helpers
  // -------------------------------------------------------------------------

  private ensureDir(filePath: string): void {
    const dir = dirname(filePath);
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }
  }
}

// ---------------------------------------------------------------------------
// Factory helpers
// ---------------------------------------------------------------------------

function makeEntry(job: NormalizedJob, now: string): TrackingEntry {
  return {
    job_id: job.job_id,
    status: "saved",
    title: job.title,
    company: job.company,
    url: job.url,
    source: job.source,
    saved_at: now,
    applied_at: null,
    updated_at: now,
    last_seen_at: now,
    notes: null,
  };
}
