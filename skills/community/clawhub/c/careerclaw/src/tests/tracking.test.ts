/**
 * tracking.test.ts — Unit tests for TrackingRepository.
 * Run: npm test
 *
 * All tests use a per-test temporary directory so there is no shared
 * state between tests and no pollution of .careerclaw/ during CI.
 */

import { describe, it, expect, beforeEach } from "vitest";
import { mkdtempSync, readFileSync, existsSync } from "fs";
import { tmpdir } from "os";
import { join } from "path";
import { TrackingRepository } from "../tracking.js";
import type { NormalizedJob, BriefingRun } from "../models.js";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function makeTmpRepo(): { repo: TrackingRepository; dir: string; trackingPath: string; runsPath: string } {
  const dir = mkdtempSync(join(tmpdir(), "careerclaw-test-"));
  const trackingPath = join(dir, "tracking.json");
  const runsPath = join(dir, "runs.jsonl");
  const repo = new TrackingRepository({ trackingPath, runsPath });
  return { repo, dir, trackingPath, runsPath };
}

function makeJob(overrides: Partial<NormalizedJob> = {}): NormalizedJob {
  return {
    job_id: "track00000000001",
    title: "Senior TypeScript Engineer",
    company: "Acme",
    location: "Remote",
    description: "A great role.",
    url: "https://example.com/job/1",
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

function makeRun(overrides: Partial<BriefingRun> = {}): BriefingRun {
  return {
    run_id: "00000000-0000-0000-0000-000000000001",
    run_at: new Date().toISOString(),
    dry_run: false,
    jobs_fetched: 10,
    jobs_ranked: 10,
    jobs_matched: 3,
    sources: { remoteok: 7, hackernews: 3 },
    timings: { fetch_ms: 100, rank_ms: 5, draft_ms: 2, persist_ms: 1 },
    version: "0.7.0",
    ...overrides,
  };
}

// ---------------------------------------------------------------------------
// load() — reading
// ---------------------------------------------------------------------------

describe("TrackingRepository.load()", () => {
  it("returns empty object when tracking.json does not exist", () => {
    const { repo } = makeTmpRepo();
    expect(repo.load()).toEqual({});
  });

  it("returns parsed store when tracking.json exists", () => {
    const { repo, trackingPath } = makeTmpRepo();
    const job = makeJob();
    repo.upsertEntries([job]);
    const store = repo.load();
    expect(store[job.job_id]).toBeDefined();
    expect(store[job.job_id]!.company).toBe("Acme");
  });

  it("returns empty object when tracking.json is corrupt", () => {
    const { repo, trackingPath } = makeTmpRepo();
    // Write corrupt JSON
    repo.upsertEntries([makeJob()]);
    const { writeFileSync } = require("fs");
    writeFileSync(trackingPath, "{ not valid json", "utf8");
    expect(repo.load()).toEqual({});
  });
});

// ---------------------------------------------------------------------------
// upsertEntries() — new entries
// ---------------------------------------------------------------------------

describe("TrackingRepository.upsertEntries() — new entries", () => {
  it("creates a new entry for an unseen job", () => {
    const { repo } = makeTmpRepo();
    const result = repo.upsertEntries([makeJob()]);
    expect(result.created).toBe(1);
    expect(result.already_present).toBe(0);
  });

  it("new entry has status='saved'", () => {
    const { repo } = makeTmpRepo();
    const job = makeJob();
    repo.upsertEntries([job]);
    const store = repo.load();
    expect(store[job.job_id]!.status).toBe("saved");
  });

  it("new entry has correct job snapshot fields", () => {
    const { repo } = makeTmpRepo();
    const job = makeJob({ title: "Staff Engineer", company: "Stripe" });
    repo.upsertEntries([job]);
    const entry = repo.load()[job.job_id]!;
    expect(entry.title).toBe("Staff Engineer");
    expect(entry.company).toBe("Stripe");
    expect(entry.url).toBe(job.url);
    expect(entry.source).toBe("remoteok");
  });

  it("new entry has null applied_at and notes", () => {
    const { repo } = makeTmpRepo();
    const job = makeJob();
    repo.upsertEntries([job]);
    const entry = repo.load()[job.job_id]!;
    expect(entry.applied_at).toBeNull();
    expect(entry.notes).toBeNull();
  });

  it("new entry has last_seen_at set", () => {
    const { repo } = makeTmpRepo();
    const job = makeJob();
    repo.upsertEntries([job]);
    const entry = repo.load()[job.job_id]!;
    expect(entry.last_seen_at).not.toBeNull();
  });

  it("creates multiple entries in one call", () => {
    const { repo } = makeTmpRepo();
    const jobs = [
      makeJob({ job_id: "id001" }),
      makeJob({ job_id: "id002" }),
      makeJob({ job_id: "id003" }),
    ];
    const result = repo.upsertEntries(jobs);
    expect(result.created).toBe(3);
    expect(result.already_present).toBe(0);
    const store = repo.load();
    expect(Object.keys(store)).toHaveLength(3);
  });
});

// ---------------------------------------------------------------------------
// upsertEntries() — re-encounter
// ---------------------------------------------------------------------------

describe("TrackingRepository.upsertEntries() — re-encounter", () => {
  it("reports already_present on second upsert", () => {
    const { repo } = makeTmpRepo();
    const job = makeJob();
    repo.upsertEntries([job]);
    const result = repo.upsertEntries([job]);
    expect(result.created).toBe(0);
    expect(result.already_present).toBe(1);
  });

  it("preserves status on re-encounter", () => {
    const { repo, trackingPath } = makeTmpRepo();
    const job = makeJob();
    repo.upsertEntries([job]);

    // Manually advance status to "applied"
    const store = repo.load();
    store[job.job_id]!.status = "applied";
    const { writeFileSync } = require("fs");
    writeFileSync(trackingPath, JSON.stringify(store, null, 2), "utf8");

    // Re-encounter should not reset status
    repo.upsertEntries([job]);
    expect(repo.load()[job.job_id]!.status).toBe("applied");
  });

  it("updates last_seen_at on re-encounter", async () => {
    const { repo } = makeTmpRepo();
    const job = makeJob();
    repo.upsertEntries([job]);
    const first = repo.load()[job.job_id]!.last_seen_at;

    // Small delay to ensure timestamp differs
    await new Promise((r) => setTimeout(r, 10));
    repo.upsertEntries([job]);
    const second = repo.load()[job.job_id]!.last_seen_at;

    expect(second).not.toBe(first);
  });

  it("mixed batch: counts created and already_present correctly", () => {
    const { repo } = makeTmpRepo();
    const jobA = makeJob({ job_id: "aaa" });
    const jobB = makeJob({ job_id: "bbb" });
    repo.upsertEntries([jobA]);

    const result = repo.upsertEntries([jobA, jobB]);
    expect(result.created).toBe(1);
    expect(result.already_present).toBe(1);
  });
});

// ---------------------------------------------------------------------------
// upsertEntries() — disk persistence
// ---------------------------------------------------------------------------

describe("TrackingRepository.upsertEntries() — disk writes", () => {
  it("writes tracking.json to disk", () => {
    const { repo, trackingPath } = makeTmpRepo();
    repo.upsertEntries([makeJob()]);
    expect(existsSync(trackingPath)).toBe(true);
  });

  it("tracking.json is valid JSON", () => {
    const { repo, trackingPath } = makeTmpRepo();
    repo.upsertEntries([makeJob()]);
    expect(() => JSON.parse(readFileSync(trackingPath, "utf8"))).not.toThrow();
  });

  it("creates parent directory if it does not exist", () => {
    const dir = mkdtempSync(join(tmpdir(), "careerclaw-test-"));
    const nestedPath = join(dir, "subdir", "tracking.json");
    const repo = new TrackingRepository({
      trackingPath: nestedPath,
      runsPath: join(dir, "runs.jsonl"),
    });
    repo.upsertEntries([makeJob()]);
    expect(existsSync(nestedPath)).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// appendRun()
// ---------------------------------------------------------------------------

describe("TrackingRepository.appendRun()", () => {
  it("creates runs.jsonl on first append", () => {
    const { repo, runsPath } = makeTmpRepo();
    repo.appendRun(makeRun());
    expect(existsSync(runsPath)).toBe(true);
  });

  it("each run appended as a separate line", () => {
    const { repo, runsPath } = makeTmpRepo();
    repo.appendRun(makeRun({ run_id: "run-1" }));
    repo.appendRun(makeRun({ run_id: "run-2" }));
    const lines = readFileSync(runsPath, "utf8")
      .split("\n")
      .filter((l) => l.trim());
    expect(lines).toHaveLength(2);
  });

  it("each line is valid JSON", () => {
    const { repo, runsPath } = makeTmpRepo();
    repo.appendRun(makeRun());
    repo.appendRun(makeRun());
    const lines = readFileSync(runsPath, "utf8")
      .split("\n")
      .filter((l) => l.trim());
    for (const line of lines) {
      expect(() => JSON.parse(line)).not.toThrow();
    }
  });

  it("persisted run contains expected fields", () => {
    const { repo, runsPath } = makeTmpRepo();
    const run = makeRun({ run_id: "abc-123", jobs_fetched: 42 });
    repo.appendRun(run);
    const parsed = JSON.parse(
      readFileSync(runsPath, "utf8").trim()
    ) as BriefingRun;
    expect(parsed.run_id).toBe("abc-123");
    expect(parsed.jobs_fetched).toBe(42);
    expect(parsed.version).toBe("0.7.0");
  });
});

// ---------------------------------------------------------------------------
// Dry-run mode
// ---------------------------------------------------------------------------

describe("TrackingRepository — dry-run mode", () => {
  it("upsertEntries() returns correct counts in dry-run", () => {
    const dir = mkdtempSync(join(tmpdir(), "careerclaw-test-"));
    const repo = new TrackingRepository({
      trackingPath: join(dir, "tracking.json"),
      runsPath: join(dir, "runs.jsonl"),
      dryRun: true,
    });
    const result = repo.upsertEntries([makeJob()]);
    expect(result.created).toBe(1);
    expect(result.already_present).toBe(0);
  });

  it("upsertEntries() writes nothing in dry-run", () => {
    const dir = mkdtempSync(join(tmpdir(), "careerclaw-test-"));
    const trackingPath = join(dir, "tracking.json");
    const repo = new TrackingRepository({
      trackingPath,
      runsPath: join(dir, "runs.jsonl"),
      dryRun: true,
    });
    repo.upsertEntries([makeJob()]);
    expect(existsSync(trackingPath)).toBe(false);
  });

  it("appendRun() writes nothing in dry-run", () => {
    const dir = mkdtempSync(join(tmpdir(), "careerclaw-test-"));
    const runsPath = join(dir, "runs.jsonl");
    const repo = new TrackingRepository({
      trackingPath: join(dir, "tracking.json"),
      runsPath,
      dryRun: true,
    });
    repo.appendRun(makeRun());
    expect(existsSync(runsPath)).toBe(false);
  });
});
