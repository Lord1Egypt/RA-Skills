/**
 * sources.test.ts — Unit tests for source aggregation and deduplication.
 *
 * Uses vi.mock() to stub both adapters so no network calls are made.
 * Run: npm test
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import { deduplicate } from "../sources.js";
import type { NormalizedJob } from "../models.js";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function makeJob(overrides: Partial<NormalizedJob> & { job_id: string }): NormalizedJob {
  return {
    title: "Engineer",
    company: "Acme",
    location: "Remote",
    description: "A job.",
    url: `https://example.com/${overrides.job_id}`,
    source: "remoteok",
    salary_min: null,
    salary_max: null,
    work_mode: "remote",
    experience_years: null,
    posted_at: null,
    fetched_at: "2026-03-03T10:00:00.000Z",
    ...overrides,
  };
}

// ---------------------------------------------------------------------------
// deduplicate
// ---------------------------------------------------------------------------

describe("deduplicate", () => {
  it("passes through a list with no duplicates", () => {
    const jobs = [makeJob({ job_id: "aaa" }), makeJob({ job_id: "bbb" })];
    expect(deduplicate(jobs)).toHaveLength(2);
  });

  it("removes duplicate job_ids, first-seen wins", () => {
    const first = makeJob({ job_id: "aaa", title: "First" });
    const dupe = makeJob({ job_id: "aaa", title: "Duplicate" });
    const result = deduplicate([first, dupe]);
    expect(result).toHaveLength(1);
    expect(result[0]!.title).toBe("First");
  });

  it("returns empty array for empty input", () => {
    expect(deduplicate([])).toEqual([]);
  });

  it("preserves original order for unique jobs", () => {
    const jobs = [
      makeJob({ job_id: "c" }),
      makeJob({ job_id: "a" }),
      makeJob({ job_id: "b" }),
    ];
    expect(deduplicate(jobs).map((j) => j.job_id)).toEqual(["c", "a", "b"]);
  });

  it("handles multiple duplicates across sources", () => {
    const jobs = [
      makeJob({ job_id: "x", source: "remoteok" }),
      makeJob({ job_id: "y", source: "hackernews" }),
      makeJob({ job_id: "x", source: "hackernews" }), // duplicate of first
      makeJob({ job_id: "z", source: "remoteok" }),
    ];
    const result = deduplicate(jobs);
    expect(result).toHaveLength(3);
    expect(result.find((j) => j.job_id === "x")!.source).toBe("remoteok");
  });
});

// ---------------------------------------------------------------------------
// fetchAllJobs — stubbed adapter tests
// ---------------------------------------------------------------------------

describe("fetchAllJobs — adapter stubs", () => {
  beforeEach(() => {
    vi.resetModules();
  });

  it("merges results from both sources", async () => {
    vi.doMock("../adapters/remoteok.js", () => ({
      fetchRemoteOkJobs: async () => [makeJob({ job_id: "r1", source: "remoteok" })],
    }));
    vi.doMock("../adapters/hackernews.js", () => ({
      fetchHnJobs: async () => [makeJob({ job_id: "h1", source: "hackernews" })],
    }));

    const { fetchAllJobs } = await import("../sources.js");
    const result = await fetchAllJobs();

    expect(result.jobs).toHaveLength(2);
    expect(result.counts["remoteok"]).toBe(1);
    expect(result.counts["hackernews"]).toBe(1);
    expect(result.errors).toEqual({});
  });

  it("degrades gracefully when RemoteOK fails", async () => {
    vi.doMock("../adapters/remoteok.js", () => ({
      fetchRemoteOkJobs: async () => { throw new Error("network error"); },
    }));
    vi.doMock("../adapters/hackernews.js", () => ({
      fetchHnJobs: async () => [makeJob({ job_id: "h1", source: "hackernews" })],
    }));

    const { fetchAllJobs } = await import("../sources.js");
    const result = await fetchAllJobs();

    expect(result.jobs).toHaveLength(1);
    expect(result.counts["remoteok"]).toBe(0);
    expect(result.errors["remoteok"]).toContain("network error");
  });

  it("degrades gracefully when HN fails", async () => {
    vi.doMock("../adapters/remoteok.js", () => ({
      fetchRemoteOkJobs: async () => [makeJob({ job_id: "r1", source: "remoteok" })],
    }));
    vi.doMock("../adapters/hackernews.js", () => ({
      fetchHnJobs: async () => { throw new Error("timeout"); },
    }));

    const { fetchAllJobs } = await import("../sources.js");
    const result = await fetchAllJobs();

    expect(result.jobs).toHaveLength(1);
    expect(result.counts["hackernews"]).toBe(0);
    expect(result.errors["hackernews"]).toContain("timeout");
  });

  it("returns empty jobs and error entries when both sources fail", async () => {
    vi.doMock("../adapters/remoteok.js", () => ({
      fetchRemoteOkJobs: async () => { throw new Error("rss down"); },
    }));
    vi.doMock("../adapters/hackernews.js", () => ({
      fetchHnJobs: async () => { throw new Error("firebase down"); },
    }));

    const { fetchAllJobs } = await import("../sources.js");
    const result = await fetchAllJobs();

    expect(result.jobs).toEqual([]);
    expect(Object.keys(result.errors)).toHaveLength(2);
  });

  it("deduplicates cross-source duplicates", async () => {
    vi.doMock("../adapters/remoteok.js", () => ({
      fetchRemoteOkJobs: async () => [makeJob({ job_id: "shared", source: "remoteok" })],
    }));
    vi.doMock("../adapters/hackernews.js", () => ({
      fetchHnJobs: async () => [makeJob({ job_id: "shared", source: "hackernews" })],
    }));

    const { fetchAllJobs } = await import("../sources.js");
    const result = await fetchAllJobs();

    expect(result.jobs).toHaveLength(1);
    expect(result.jobs[0]!.source).toBe("remoteok"); // first-seen wins
  });
});
