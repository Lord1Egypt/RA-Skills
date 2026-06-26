/**
 * briefing.ts — Daily briefing pipeline orchestrator.
 *
 * `runBriefing()` is the single entry point that wires every module
 * into the complete end-to-end workflow:
 *
 *   fetch → deduplicate → rank → draft → persist → return bundle
 *
 * Design principles (from Phase 4 architecture doc):
 *   - Skill-first: accepts UserProfile as a parameter, not a file path.
 *     The caller (CLI or OpenClaw agent) is responsible for loading the
 *     profile; the orchestrator never touches the filesystem for input.
 *   - Dual-mode output: structured BriefingResult JSON for agents +
 *     per-stage timings for observability.
 *   - Dry-run: suppresses all writes; counts are still accurate.
 *   - Testable: fetchFn and repo are injectable; no live network calls
 *     required in tests.
 *   - Graceful degradation: if the fetch stage returns zero jobs (e.g.
 *     both adapters failed), the pipeline short-circuits cleanly with
 *     an empty result rather than crashing.
 */

import { randomUUID } from "crypto";
import { createRequire } from "module";
import type {
  UserProfile,
  ScoredJob,
  OutreachDraft,
  BriefingRun,
  BriefingResult,
  ResumeIntelligence,
} from "./models.js";
import { fetchAllJobs, type FetchResult } from "./sources.js";
import { rankJobs } from "./matching/index.js";
import { draftOutreach } from "./drafting.js";
import { enhanceDraft, type EnhanceOptions } from "./llm-enhance.js";
import { checkLicense, type CheckLicenseOptions } from "./license.js";
import { TrackingRepository } from "./tracking.js";
import { DEFAULT_TOP_K } from "./config.js";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface BriefingOptions {
  /** Number of top matches to return (default: DEFAULT_TOP_K = 3). */
  topK?: number;
  /** Suppress all file writes when true. Counts remain accurate. */
  dryRun?: boolean;
  /**
   * Injectable fetch function — defaults to the real fetchAllJobs().
   * Pass a stub in tests to avoid live network calls.
   */
  fetchFn?: () => Promise<FetchResult>;
  /**
   * Injectable TrackingRepository — defaults to a new instance with
   * standard paths. Pass a tmpdir-backed instance in tests.
   */
  repo?: TrackingRepository;
  /**
   * Resume intelligence from buildResumeIntelligence().
   * Required for LLM draft enhancement — ignored when proKey is absent.
   */
  resumeIntel?: ResumeIntelligence;
  /**
   * CareerClaw Pro license key (CAREERCLAW_PRO_KEY).
   * Validated against Gumroad before enabling LLM-enhanced drafts.
   * Falls back to deterministic draft if validation fails.
   */
  proKey?: string;
  /**
   * Injectable fetch for the LLM API calls — passed through to enhanceDraft().
   * Defaults to global fetch. Pass a stub in tests.
   */
  enhanceFetchFn?: EnhanceOptions["fetchFn"];
  /**
   * Injectable fetch for the Gumroad license API call.
   * Defaults to global fetch. Pass a stub in tests.
   */
  licenseFetchFn?: CheckLicenseOptions["fetchFn"];
  /**
   * Override the license cache file path — for tests using a tmpdir.
   */
  licenseCachePath?: string;
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Run a full briefing pipeline for the given user profile.
 *
 * Stages and timings:
 *   1. fetch_ms  — fetch + deduplicate jobs from all sources
 *   2. rank_ms   — score and rank jobs against profile
 *   3. draft_ms  — generate one OutreachDraft per top match
 *   4. persist_ms — upsert tracking entries + append run record
 *
 * @param profile - User profile (passed in by caller, not loaded here)
 * @param options - Injection points and run flags
 */
export async function runBriefing(
  profile: UserProfile,
  options: BriefingOptions = {}
): Promise<BriefingResult> {
  const {
    topK = DEFAULT_TOP_K,
    dryRun = false,
    fetchFn = fetchAllJobs,
    repo = new TrackingRepository({ dryRun }),
    resumeIntel,
    proKey,
    enhanceFetchFn,
    licenseFetchFn,
    licenseCachePath,
  } = options;

  // Validate Pro license before enabling LLM enhancement.
  // Runs only when proKey is present; result degrades gracefully on network
  // failure (cached result used for up to LICENSE_CACHE_TTL_MS = 7 days).
  let isProActive = false;
  if (proKey && proKey.trim().length > 0 && resumeIntel) {
    const licenseOptions: import("./license.js").CheckLicenseOptions = {};
    if (licenseFetchFn !== undefined) licenseOptions.fetchFn = licenseFetchFn;
    if (licenseCachePath !== undefined) licenseOptions.cachePath = licenseCachePath;
    const licenseResult = await checkLicense(proKey, licenseOptions);
    isProActive = licenseResult.valid;
  }

  const runAt = new Date().toISOString();
  const runId = randomUUID();
  const version = readPackageVersion();

  // -------------------------------------------------------------------------
  // Stage 1: Fetch + deduplicate
  // -------------------------------------------------------------------------
  const fetchStart = Date.now();
  let fetchResult: FetchResult;
  try {
    fetchResult = await fetchFn();
  } catch {
    // Catastrophic fetch failure — return an empty result rather than throwing
    fetchResult = { jobs: [], counts: {}, errors: {} };
  }
  const fetchMs = Date.now() - fetchStart;

  const { jobs, counts: sourceCounts } = fetchResult;

  // -------------------------------------------------------------------------
  // Stage 2: Rank
  // -------------------------------------------------------------------------
  const rankStart = Date.now();
  const matches: ScoredJob[] = jobs.length > 0 ? rankJobs(jobs, profile, topK) : [];
  const rankMs = Date.now() - rankStart;

  // -------------------------------------------------------------------------
  // Stage 3: Draft
  // -------------------------------------------------------------------------
  const draftStart = Date.now();
  const drafts: OutreachDraft[] = await Promise.all(
    matches.map(async (scored) => {
      const baseline = draftOutreach(scored.job, profile, scored.matched_keywords);
      if (isProActive) {
        return enhanceDraft(
          scored.job,
          profile,
          resumeIntel!,
          baseline,
          scored.gap_keywords,
          enhanceFetchFn !== undefined ? { fetchFn: enhanceFetchFn } : {}
        );
      }
      return baseline;
    })
  );
  const draftMs = Date.now() - draftStart;

  // -------------------------------------------------------------------------
  // Stage 4: Persist
  // -------------------------------------------------------------------------
  const persistStart = Date.now();
  const trackingResult = repo.upsertEntries(
    matches.map((s) => s.job),
    matches
  );

  const run: BriefingRun = {
    run_id: runId,
    run_at: runAt,
    dry_run: dryRun,
    jobs_fetched: jobs.length,
    jobs_ranked: jobs.length,
    jobs_matched: matches.length,
    sources: sourceCounts,
    timings: {
      fetch_ms: fetchMs,
      rank_ms: rankMs,
      draft_ms: draftMs,
      persist_ms: null, // filled below after appendRun
    },
    version,
  };

  repo.appendRun(run);
  const persistMs = Date.now() - persistStart;

  // Back-fill persist_ms (the field exists for observability; the run
  // record on disk will have null for persist_ms — that is acceptable
  // and consistent with the Python implementation)
  run.timings.persist_ms = persistMs;

  // -------------------------------------------------------------------------
  // Result bundle
  // -------------------------------------------------------------------------
  return {
    run,
    matches,
    drafts,
    tracking: {
      created: trackingResult.created,
      already_present: trackingResult.already_present,
    },
    dry_run: dryRun,
  };
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Read the package version from package.json at runtime. */
function readPackageVersion(): string {
  try {
    const require = createRequire(import.meta.url);
    // Walk up from src/ to find package.json
    const pkg = require("../package.json") as { version: string };
    return pkg.version;
  } catch {
    return "unknown";
  }
}
