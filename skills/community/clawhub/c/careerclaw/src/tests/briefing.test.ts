/**
 * briefing.test.ts — Integration tests for runBriefing().
 *
 * All tests inject:
 *   - A stub fetchFn so no live network calls are made.
 *   - A tmpdir-backed TrackingRepository so no .careerclaw/ files
 *     are written or read during CI.
 *
 * Run: npm test
 */

import { describe, it, expect } from "vitest";
import { mkdtempSync } from "fs";
import { tmpdir } from "os";
import { join } from "path";
import { runBriefing } from "../briefing.js";
import { TrackingRepository } from "../tracking.js";
import { emptyProfile } from "../models.js";
import type { NormalizedJob, UserProfile, FetchResult } from "../models.js";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function makeTmpRepo(dryRun = false): TrackingRepository {
  const dir = mkdtempSync(join(tmpdir(), "cc-briefing-test-"));
  return new TrackingRepository({
    trackingPath: join(dir, "tracking.json"),
    runsPath: join(dir, "runs.jsonl"),
    dryRun,
  });
}

function makeJob(overrides: Partial<NormalizedJob> = {}): NormalizedJob {
  return {
    job_id: `job${Math.random().toString(36).slice(2, 10)}`,
    title: "Senior TypeScript Engineer",
    company: "Acme",
    location: "Remote",
    description: "TypeScript react node aws engineer role.",
    url: `https://example.com/job/${Math.random()}`,
    source: "remoteok",
    salary_min: null,
    salary_max: null,
    work_mode: "remote",
    experience_years: null,
    posted_at: null,
    fetched_at: new Date().toISOString(),
    ...overrides,
  };
}

function makeProfile(overrides: Partial<UserProfile> = {}): UserProfile {
  return {
    ...emptyProfile(),
    skills: ["typescript", "react", "node"],
    experience_years: 5,
    work_mode: "remote",
    ...overrides,
  };
}

function stubFetch(jobs: NormalizedJob[]): () => Promise<FetchResult> {
  return async () => ({
    jobs,
    counts: { remoteok: jobs.filter((j) => j.source === "remoteok").length },
    errors: {},
  });
}

// ---------------------------------------------------------------------------
// Result shape
// ---------------------------------------------------------------------------

describe("runBriefing — result shape", () => {
  it("returns all required BriefingResult fields", async () => {
    const result = await runBriefing(makeProfile(), {
      fetchFn: stubFetch([makeJob()]),
      repo: makeTmpRepo(),
    });
    expect(result).toHaveProperty("run");
    expect(result).toHaveProperty("matches");
    expect(result).toHaveProperty("drafts");
    expect(result).toHaveProperty("tracking");
    expect(result).toHaveProperty("dry_run");
  });

  it("matches and drafts have the same length", async () => {
    const jobs = [makeJob(), makeJob(), makeJob(), makeJob(), makeJob()];
    const result = await runBriefing(makeProfile(), {
      fetchFn: stubFetch(jobs),
      repo: makeTmpRepo(),
      topK: 3,
    });
    expect(result.drafts).toHaveLength(result.matches.length);
  });

  it("matches length is capped at topK", async () => {
    const jobs = [makeJob(), makeJob(), makeJob(), makeJob(), makeJob()];
    const result = await runBriefing(makeProfile(), {
      fetchFn: stubFetch(jobs),
      repo: makeTmpRepo(),
      topK: 2,
    });
    expect(result.matches.length).toBeLessThanOrEqual(2);
  });

  it("each draft job_id matches its corresponding match job_id", async () => {
    const jobs = [makeJob(), makeJob()];
    const result = await runBriefing(makeProfile(), {
      fetchFn: stubFetch(jobs),
      repo: makeTmpRepo(),
    });
    for (let i = 0; i < result.matches.length; i++) {
      expect(result.drafts[i]!.job_id).toBe(result.matches[i]!.job.job_id);
    }
  });
});

// ---------------------------------------------------------------------------
// BriefingRun fields
// ---------------------------------------------------------------------------

describe("runBriefing — BriefingRun fields", () => {
  it("run.run_id is a non-empty UUID-format string", async () => {
    const result = await runBriefing(makeProfile(), {
      fetchFn: stubFetch([makeJob()]),
      repo: makeTmpRepo(),
    });
    expect(result.run.run_id).toMatch(
      /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/
    );
  });

  it("run.run_at is an ISO-8601 timestamp", async () => {
    const result = await runBriefing(makeProfile(), {
      fetchFn: stubFetch([makeJob()]),
      repo: makeTmpRepo(),
    });
    expect(() => new Date(result.run.run_at)).not.toThrow();
    expect(result.run.run_at).toMatch(/^\d{4}-\d{2}-\d{2}T/);
  });

  it("run.jobs_fetched matches the number of jobs returned by fetchFn", async () => {
    const jobs = [makeJob(), makeJob(), makeJob()];
    const result = await runBriefing(makeProfile(), {
      fetchFn: stubFetch(jobs),
      repo: makeTmpRepo(),
    });
    expect(result.run.jobs_fetched).toBe(3);
  });

  it("run.jobs_matched matches the matches array length", async () => {
    const jobs = [makeJob(), makeJob(), makeJob(), makeJob()];
    const result = await runBriefing(makeProfile(), {
      fetchFn: stubFetch(jobs),
      repo: makeTmpRepo(),
      topK: 2,
    });
    expect(result.run.jobs_matched).toBe(result.matches.length);
  });

  it("run.version is a non-empty string", async () => {
    const result = await runBriefing(makeProfile(), {
      fetchFn: stubFetch([makeJob()]),
      repo: makeTmpRepo(),
    });
    expect(typeof result.run.version).toBe("string");
    expect(result.run.version.length).toBeGreaterThan(0);
  });

  it("run.timings has fetch_ms and rank_ms as numbers", async () => {
    const result = await runBriefing(makeProfile(), {
      fetchFn: stubFetch([makeJob()]),
      repo: makeTmpRepo(),
    });
    expect(typeof result.run.timings.fetch_ms).toBe("number");
    expect(typeof result.run.timings.rank_ms).toBe("number");
    expect(typeof result.run.timings.draft_ms).toBe("number");
  });
});

// ---------------------------------------------------------------------------
// Tracking counts
// ---------------------------------------------------------------------------

describe("runBriefing — tracking counts", () => {
  it("tracking.created equals matches count on first run", async () => {
    const jobs = [makeJob(), makeJob(), makeJob()];
    const result = await runBriefing(makeProfile(), {
      fetchFn: stubFetch(jobs),
      repo: makeTmpRepo(),
      topK: 3,
    });
    expect(result.tracking.created).toBe(result.matches.length);
    expect(result.tracking.already_present).toBe(0);
  });

  it("tracking.already_present is non-zero on second run with same jobs", async () => {
    const jobs = [makeJob({ job_id: "fixed-id-aaa" }), makeJob({ job_id: "fixed-id-bbb" })];
    const repo = makeTmpRepo();

    await runBriefing(makeProfile(), { fetchFn: stubFetch(jobs), repo, topK: 2 });
    const second = await runBriefing(makeProfile(), {
      fetchFn: stubFetch(jobs),
      repo,
      topK: 2,
    });

    expect(second.tracking.already_present).toBeGreaterThan(0);
  });
});

// ---------------------------------------------------------------------------
// Dry-run mode
// ---------------------------------------------------------------------------

describe("runBriefing — dry-run", () => {
  it("dry_run flag is true when dryRun option is set", async () => {
    const result = await runBriefing(makeProfile(), {
      fetchFn: stubFetch([makeJob()]),
      repo: makeTmpRepo(true),
      dryRun: true,
    });
    expect(result.dry_run).toBe(true);
    expect(result.run.dry_run).toBe(true);
  });

  it("dry_run tracking counts are still accurate", async () => {
    const jobs = [makeJob(), makeJob()];
    const result = await runBriefing(makeProfile(), {
      fetchFn: stubFetch(jobs),
      repo: makeTmpRepo(true),
      dryRun: true,
      topK: 2,
    });
    expect(result.tracking.created).toBe(result.matches.length);
  });
});

// ---------------------------------------------------------------------------
// Edge cases
// ---------------------------------------------------------------------------

describe("runBriefing — edge cases", () => {
  it("returns empty matches and drafts when no jobs are fetched", async () => {
    const result = await runBriefing(makeProfile(), {
      fetchFn: stubFetch([]),
      repo: makeTmpRepo(),
    });
    expect(result.matches).toHaveLength(0);
    expect(result.drafts).toHaveLength(0);
    expect(result.tracking.created).toBe(0);
  });

  it("does not throw when fetchFn throws — returns empty result", async () => {
    const failingFetch = async (): Promise<FetchResult> => {
      throw new Error("Network error");
    };
    const result = await runBriefing(makeProfile(), {
      fetchFn: failingFetch,
      repo: makeTmpRepo(),
    });
    expect(result.matches).toHaveLength(0);
    expect(result.run.jobs_fetched).toBe(0);
  });

  it("works with an empty profile (emptyProfile())", async () => {
    await expect(
      runBriefing(emptyProfile(), {
        fetchFn: stubFetch([makeJob()]),
        repo: makeTmpRepo(),
      })
    ).resolves.not.toThrow();
  });
});
