/**
 * models.ts — Canonical data schemas for CareerClaw.
 *
 * These types are the single source of truth for all data flowing through
 * the pipeline. JSON serialisation formats are intentionally kept identical
 * to the Python careerclaw package so that profile.json, tracking.json, and
 * runs.jsonl files remain compatible between the two implementations.
 */

// ---------------------------------------------------------------------------
// Enums
// ---------------------------------------------------------------------------

/** Application lifecycle states, persisted as lowercase strings in JSON. */
export type ApplicationStatus =
  | "saved"
  | "applied"
  | "interviewing"
  | "rejected"
  | "offer";

/** Work-mode preference. Matches the values accepted in profile.json. */
export type WorkMode = "remote" | "hybrid" | "onsite" | "any";

/** Canonical source identifiers for job listings. */
export type JobSource = "remoteok" | "hackernews" | "unknown";

// ---------------------------------------------------------------------------
// Core domain types
// ---------------------------------------------------------------------------

/**
 * A normalised job record produced by any adapter.
 *
 * `job_id` is a stable SHA-256 hex digest of the canonical URL (or
 * company+title when no URL is available).  It is used as the primary key
 * in tracking.json and for deduplication across sources and runs.
 */
export interface NormalizedJob {
  /** Stable hash-based identifier. */
  job_id: string;
  title: string;
  company: string;
  /** Raw location string from the source ("Remote", "NYC", etc.). */
  location: string;
  description: string;
  /** Canonical URL — empty string when unavailable. */
  url: string;
  source: JobSource;
  /** Minimum salary in annualised USD, or null when not stated. */
  salary_min: number | null;
  /** Maximum salary in annualised USD, or null when not stated. */
  salary_max: number | null;
  /** Normalised work mode inferred from job text, or null when ambiguous. */
  work_mode: WorkMode | null;
  /** Required years of experience inferred from job text, or null. */
  experience_years: number | null;
  /** ISO-8601 UTC timestamp of when the job was posted, or null. */
  posted_at: string | null;
  /** ISO-8601 UTC timestamp of when this record was fetched. */
  fetched_at: string;
}

/**
 * User profile loaded from `.careerclaw/profile.json`.
 *
 * All fields are optional so that partial profiles (e.g. profiles created
 * incrementally via the OpenClaw agent wizard) are still valid at runtime.
 * The briefing pipeline degrades gracefully when fields are missing.
 */
export interface UserProfile {
  skills: string[];
  target_roles: string[];
  /** Total years of professional experience. */
  experience_years: number | null;
  work_mode: WorkMode | null;
  /** Short free-text resume summary used for keyword extraction. */
  resume_summary: string | null;
  /** City / region string used for location scoring. */
  location: string | null;
  /** Minimum acceptable annual salary in USD. */
  salary_min: number | null;
}

/**
 * A single tracked application in `.careerclaw/tracking.json`.
 *
 * Keyed by `job_id` in the JSON file.  All timestamps are ISO-8601 UTC.
 */
export interface TrackingEntry {
  job_id: string;
  status: ApplicationStatus;
  /** Snapshot of the job title at time of saving. */
  title: string;
  /** Snapshot of the company name at time of saving. */
  company: string;
  url: string;
  source: JobSource;
  /** ISO-8601 UTC timestamp when the entry was first saved. */
  saved_at: string;
  /** ISO-8601 UTC timestamp when the application was submitted, or null. */
  applied_at: string | null;
  /** ISO-8601 UTC timestamp when the entry was last updated. */
  updated_at: string;
  /** ISO-8601 UTC timestamp when this job was last seen in a briefing run. */
  last_seen_at: string | null;
  notes: string | null;
}

/**
 * A single run record appended to `.careerclaw/runs.jsonl`.
 *
 * Each line in the JSONL file is one serialised BriefingRun.
 */
export interface BriefingRun {
  /** Random UUID v4 identifying this run. */
  run_id: string;
  /** ISO-8601 UTC timestamp when the run started. */
  run_at: string;
  /** Whether this was a dry-run (no writes to disk). */
  dry_run: boolean;
  /** Total jobs fetched across all sources. */
  jobs_fetched: number;
  /** Jobs that passed deduplication and were considered for ranking. */
  jobs_ranked: number;
  /** Top-k jobs returned by the engine. */
  jobs_matched: number;
  /** Source breakdown, e.g. { remoteok: 12, hackernews: 7 }. */
  sources: Partial<Record<JobSource, number>>;
  /** Wall-clock duration in milliseconds for each pipeline stage. */
  timings: {
    fetch_ms: number | null;
    rank_ms: number | null;
    draft_ms: number | null;
    persist_ms: number | null;
  };
  /** careerclaw-js package version that produced this run. */
  version: string;
}

// ---------------------------------------------------------------------------
// Matching / scoring types
// ---------------------------------------------------------------------------

/**
 * Per-dimension score breakdown produced by the matching engine.
 * All values are in [0, 1].
 */
export interface MatchBreakdown {
  /** Raw Jaccard-like keyword overlap score in [0, 1]. */
  keyword: number;
  experience: number;
  salary: number;
  work_mode: number;
}

/**
 * A ranked job with its composite score and explanation.
 */
export interface ScoredJob {
  job: NormalizedJob;
  /** Weighted composite score in [0, 1]. */
  score: number;
  breakdown: MatchBreakdown;
  /** Human-readable explanation tokens (matched keywords etc.). */
  matched_keywords: string[];
  /** Skills/requirements in the job not present in the user profile. */
  gap_keywords: string[];
}

// ---------------------------------------------------------------------------
// Phase 5 — Pro tier analysis types
// ---------------------------------------------------------------------------

/**
 * Structured requirements extracted from a job description.
 * Used as the job corpus for gap analysis.
 */
export interface JobRequirements {
  keywords: string[];
  phrases: string[];
}

/**
 * Section-aware keyword extraction from a resume / profile.
 * Schema is JSON-compatible with the Python careerclaw output.
 */
export interface ResumeIntelligence {
  extracted_keywords: string[];
  extracted_phrases: string[];
  keyword_stream: string[];
  phrase_stream: string[];
  impact_signals: string[];
  keyword_weights: Record<string, number>;
  phrase_weights: Record<string, number>;
  source: 'summary_only' | 'resume_text' | 'skills_injected';
}

/**
 * Result of gapAnalysis() — fit score and matched/gap keyword lists.
 */
export interface GapAnalysisResult {
  fit_score: number;
  fit_score_unweighted: number;
  signals: { keywords: string[]; phrases: string[] };
  gaps: { keywords: string[]; phrases: string[] };
  summary: {
    top_signals: { keywords: string[]; phrases: string[] };
    top_gaps: { keywords: string[]; phrases: string[] };
  };
}

// ---------------------------------------------------------------------------
// Drafting types
// ---------------------------------------------------------------------------

export interface OutreachDraft {
  job_id: string;
  subject: string;
  body: string;
  /** True when the draft was produced by LLM enhancement (Pro tier). */
  llm_enhanced: boolean;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Returns an ISO-8601 UTC timestamp string for the current moment. */
export function utcNow(): string {
  return new Date().toISOString();
}

/** Returns a default empty UserProfile. */
export function emptyProfile(): UserProfile {
  return {
    skills: [],
    target_roles: [],
    experience_years: null,
    work_mode: null,
    resume_summary: null,
    location: null,
    salary_min: null,
  };
}

// ---------------------------------------------------------------------------
// Briefing output bundle
// ---------------------------------------------------------------------------

/**
 * The complete output of a single briefing run.
 * This is the stable JSON schema consumed by OpenClaw/ClawHub agents.
 */
export interface BriefingResult {
  /** The BriefingRun record that was (or would be) appended to runs.jsonl. */
  run: BriefingRun;
  /** Top-K scored jobs produced by the ranking engine. */
  matches: ScoredJob[];
  /** One OutreachDraft per match, in the same order as matches[]. */
  drafts: OutreachDraft[];
  /** Counts from upsertEntries() — always accurate even in dry-run. */
  tracking: {
    created: number;
    already_present: number;
  };
  /** Whether this was a dry run (no files written). */
  dry_run: boolean;
}

