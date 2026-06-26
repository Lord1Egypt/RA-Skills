/**
 * sources.ts — Source aggregation layer.
 *
 * `fetchAllJobs()` is the single entry point for the briefing pipeline.
 * It calls both adapters independently (per-source error isolation), merges
 * results, and deduplicates by `job_id` (first-seen wins).
 *
 * Downstream layers (matching engine, gap analysis) are source-agnostic —
 * they only see `NormalizedJob[]`.
 */

import type { NormalizedJob, JobSource } from "./models.js";
import { fetchRemoteOkJobs } from "./adapters/remoteok.js";
import { fetchHnJobs } from "./adapters/hackernews.js";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface FetchResult {
  jobs: NormalizedJob[];
  /** Per-source job counts for run instrumentation. */
  counts: Partial<Record<JobSource, number>>;
  /** Per-source errors — non-empty means a source was degraded. */
  errors: Partial<Record<JobSource, string>>;
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Fetch jobs from all configured sources and return a deduplicated list.
 *
 * Failures in individual sources are caught and recorded in `errors` —
 * the pipeline continues with whatever sources succeeded. This mirrors
 * the Python careerclaw per-source resilience pattern.
 */
export async function fetchAllJobs(): Promise<FetchResult> {
  const counts: Partial<Record<JobSource, number>> = {};
  const errors: Partial<Record<JobSource, string>> = {};
  const allJobs: NormalizedJob[] = [];

  // Run both adapters concurrently; isolate failures per source
  const [remoteokResult, hnResult] = await Promise.allSettled([
    fetchRemoteOkJobs(),
    fetchHnJobs(),
  ]);

  if (remoteokResult.status === "fulfilled") {
    counts["remoteok"] = remoteokResult.value.length;
    allJobs.push(...remoteokResult.value);
  } else {
    errors["remoteok"] = String(remoteokResult.reason);
    counts["remoteok"] = 0;
  }

  if (hnResult.status === "fulfilled") {
    counts["hackernews"] = hnResult.value.length;
    allJobs.push(...hnResult.value);
  } else {
    errors["hackernews"] = String(hnResult.reason);
    counts["hackernews"] = 0;
  }

  return {
    jobs: deduplicate(allJobs),
    counts,
    errors,
  };
}

// ---------------------------------------------------------------------------
// Deduplication
// ---------------------------------------------------------------------------

/**
 * Deduplicate a list of jobs by `job_id`.
 * First-seen wins — preserves RemoteOK order before HN order.
 */
export function deduplicate(jobs: NormalizedJob[]): NormalizedJob[] {
  const seen = new Set<string>();
  const result: NormalizedJob[] = [];
  for (const job of jobs) {
    if (!seen.has(job.job_id)) {
      seen.add(job.job_id);
      result.push(job);
    }
  }
  return result;
}
