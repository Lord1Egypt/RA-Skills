/**
 * matching.engine.test.ts — End-to-end ranking engine tests.
 *
 * Tests use real UserProfile and NormalizedJob types to validate that
 * rankJobs() produces correct ordering, respects topK, applies the
 * signal gate, and populates all ScoredJob fields.
 * Run: npm test
 */

import { describe, it, expect } from "vitest";
import { rankJobs } from "../matching/engine.js";
import { emptyProfile } from "../models.js";
import type { NormalizedJob, UserProfile } from "../models.js";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function makeJob(overrides: Partial<NormalizedJob> & { job_id: string }): NormalizedJob {
  return {
    title: "Engineer",
    company: "Corp",
    location: "Remote",
    description: "engineering role",
    url: `https://example.com/${overrides.job_id}`,
    source: "remoteok",
    salary_min: null,
    salary_max: null,
    work_mode: null,
    experience_years: null,
    posted_at: null,
    fetched_at: "2026-03-04T10:00:00.000Z",
    ...overrides,
  };
}

/** A profile with skills that will overlap with standard makeJob() descriptions. */
function makeProfile(overrides: Partial<UserProfile> = {}): UserProfile {
  return {
    ...emptyProfile(),
    skills: ["typescript", "react"],
    target_roles: ["engineer"],
    experience_years: 5,
    work_mode: "remote",
    ...overrides,
  };
}

// ---------------------------------------------------------------------------
// rankJobs — basic behaviour
// ---------------------------------------------------------------------------

describe("rankJobs — basic", () => {
  it("returns empty array for empty job list", () => {
    expect(rankJobs([], makeProfile())).toEqual([]);
  });

  it("returns at most topK results", () => {
    const jobs = [
      makeJob({ job_id: "a", description: "typescript react engineer" }),
      makeJob({ job_id: "b", description: "typescript react engineer" }),
      makeJob({ job_id: "c", description: "typescript react engineer" }),
      makeJob({ job_id: "d", description: "typescript react engineer" }),
    ];
    expect(rankJobs(jobs, makeProfile(), 2)).toHaveLength(2);
  });

  it("returns all jobs when topK exceeds job count", () => {
    const jobs = [
      makeJob({ job_id: "a", description: "typescript react engineer" }),
      makeJob({ job_id: "b", description: "typescript react engineer" }),
    ];
    expect(rankJobs(jobs, makeProfile(), 10)).toHaveLength(2);
  });

  it("each result is a valid ScoredJob with all required fields", () => {
    const jobs = [makeJob({ job_id: "a", description: "typescript react engineer" })];
    const [result] = rankJobs(jobs, makeProfile(), 1);
    expect(result).toHaveProperty("job");
    expect(result).toHaveProperty("score");
    expect(result).toHaveProperty("breakdown");
    expect(result).toHaveProperty("matched_keywords");
    expect(result).toHaveProperty("gap_keywords");
    expect(result!.breakdown).toHaveProperty("keyword");
    expect(result!.breakdown).toHaveProperty("experience");
    expect(result!.breakdown).toHaveProperty("salary");
    expect(result!.breakdown).toHaveProperty("work_mode");
  });

  it("all composite scores are in [0, 1]", () => {
    const profile = makeProfile({ salary_min: 100_000 });
    const jobs = [
      makeJob({ job_id: "a", description: "typescript react node", work_mode: "remote", salary_min: 120_000, experience_years: 3 }),
      makeJob({ job_id: "b", description: "typescript api backend", work_mode: "onsite", salary_min: 80_000, experience_years: 8 }),
    ];
    for (const result of rankJobs(jobs, profile, 5)) {
      expect(result.score).toBeGreaterThanOrEqual(0);
      expect(result.score).toBeLessThanOrEqual(1);
    }
  });
});

// ---------------------------------------------------------------------------
// rankJobs — signal gate
// ---------------------------------------------------------------------------

describe("rankJobs — signal gate", () => {
  it("filters out jobs with zero keyword overlap (default minKeywordScore=0.01)", () => {
    const profile = makeProfile({ skills: ["typescript"], target_roles: [] });
    const dentist = makeJob({
      job_id: "dentist",
      title: "Dentist",
      description: "Looking for a qualified dentist.",
      work_mode: "remote",   // perfect metadata match
      salary_min: 200_000,
      experience_years: 5,
    });
    const results = rankJobs([dentist], profile);
    expect(results).toHaveLength(0);
  });

  it("bypassing the gate with minKeywordScore=0 returns all jobs", () => {
    const jobs = [
      makeJob({ job_id: "a" }),
      makeJob({ job_id: "b" }),
    ];
    expect(rankJobs(jobs, emptyProfile(), 10, 0)).toHaveLength(2);
  });

  it("emptyProfile() does not throw even when gate filters all jobs", () => {
    const jobs = [makeJob({ job_id: "x", description: "typescript engineer" })];
    expect(() => rankJobs(jobs, emptyProfile())).not.toThrow();
  });
});

// ---------------------------------------------------------------------------
// rankJobs — ranking order
// ---------------------------------------------------------------------------

describe("rankJobs — ranking order", () => {
  it("ranks a highly matching job above a poorly matching job", () => {
    const profile = makeProfile({
      skills: ["typescript", "react", "node"],
      target_roles: ["senior engineer"],
      experience_years: 6,
      salary_min: 100_000,
    });

    const strongMatch = makeJob({
      job_id: "strong",
      title: "Senior TypeScript Engineer",
      description: "Looking for a senior engineer with typescript react and node skills.",
      work_mode: "remote",
      salary_min: 130_000,
      experience_years: 5,
    });

    const weakMatch = makeJob({
      job_id: "weak",
      title: "TypeScript Developer",
      description: "Entry level typescript role.",
      work_mode: "onsite",
      salary_min: 70_000,
      experience_years: 10,
    });

    const results = rankJobs([weakMatch, strongMatch], profile, 2);
    expect(results[0]!.job.job_id).toBe("strong");
    expect(results[1]!.job.job_id).toBe("weak");
  });

  it("results are sorted descending by score", () => {
    const profile = makeProfile();
    const jobs = [
      makeJob({ job_id: "a", description: "react typescript frontend", work_mode: "onsite" }),
      makeJob({ job_id: "b", description: "react typescript frontend", work_mode: "remote" }),
      makeJob({ job_id: "c", description: "react typescript frontend", work_mode: "remote" }),
    ];
    const results = rankJobs(jobs, profile, 3);
    const scores = results.map((r) => r.score);
    for (let i = 0; i < scores.length - 1; i++) {
      expect(scores[i]!).toBeGreaterThanOrEqual(scores[i + 1]!);
    }
  });

  it("preserves original job data in ScoredJob.job", () => {
    const job = makeJob({ job_id: "preserve", title: "Staff Engineer", company: "TestCo", description: "typescript react staff engineer" });
    const [result] = rankJobs([job], makeProfile(), 1);
    expect(result!.job.title).toBe("Staff Engineer");
    expect(result!.job.company).toBe("TestCo");
    expect(result!.job.job_id).toBe("preserve");
  });

  it("matched_keywords contains tokens found in both profile and job", () => {
    const profile = makeProfile({ skills: ["typescript", "react"] });
    const job = makeJob({ job_id: "m", description: "typescript react node aws" });
    const [result] = rankJobs([job], profile, 1);
    expect(result!.matched_keywords).toContain("typescript");
    expect(result!.matched_keywords).toContain("react");
  });

  it("gap_keywords contains job tokens absent from profile", () => {
    const profile = makeProfile({ skills: ["typescript"] });
    const job = makeJob({ job_id: "g", description: "typescript golang kubernetes" });
    const [result] = rankJobs([job], profile, 1);
    expect(result!.gap_keywords).toContain("golang");
    expect(result!.gap_keywords).not.toContain("typescript");
  });
});
