/**
 * tests/models.test.ts — Unit tests for canonical data schemas.
 *
 * Run: npm test
 */

import { describe, it, expect } from "vitest";
import {
	utcNow,
	emptyProfile,
	type NormalizedJob,
	type UserProfile,
	type TrackingEntry,
	type BriefingRun,
	type ScoredJob,
} from "../models.js";

describe("utcNow", () => {
	it("returns an ISO-8601 UTC string", () => {
		const ts = utcNow();
		expect(ts).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$/);
	});

	it("is close to Date.now()", () => {
		const before = Date.now();
		const ts = utcNow();
		const after = Date.now();
		const parsed = new Date(ts).getTime();
		expect(parsed).toBeGreaterThanOrEqual(before);
		expect(parsed).toBeLessThanOrEqual(after);
	});
});

describe("emptyProfile", () => {
	it("returns a valid UserProfile with empty/null fields", () => {
		const p = emptyProfile();
		expect(p.skills).toEqual([]);
		expect(p.target_roles).toEqual([]);
		expect(p.experience_years).toBeNull();
		expect(p.work_mode).toBeNull();
		expect(p.resume_summary).toBeNull();
		expect(p.location).toBeNull();
		expect(p.salary_min).toBeNull();
	});

	it("each call returns a new object (not shared state)", () => {
		const a = emptyProfile();
		const b = emptyProfile();
		a.skills.push("python");
		expect(b.skills).toEqual([]);
	});
});

describe("NormalizedJob shape", () => {
	it("accepts a fully populated job record", () => {
		const job: NormalizedJob = {
			job_id: "abc123",
			title: "Senior Engineer",
			company: "Acme",
			location: "Remote",
			description: "Build things.",
			url: "https://example.com/jobs/1",
			source: "remoteok",
			salary_min: 120_000,
			salary_max: 180_000,
			work_mode: "remote",
			experience_years: 5,
			posted_at: "2026-03-01T00:00:00.000Z",
			fetched_at: "2026-03-03T10:00:00.000Z",
		};
		expect(job.job_id).toBe("abc123");
		expect(job.source).toBe("remoteok");
	});

	it("accepts nullable optional fields as null", () => {
		const job: NormalizedJob = {
			job_id: "def456",
			title: "Engineer",
			company: "Startup",
			location: "",
			description: "",
			url: "",
			source: "hackernews",
			salary_min: null,
			salary_max: null,
			work_mode: null,
			experience_years: null,
			posted_at: null,
			fetched_at: utcNow(),
		};
		expect(job.salary_min).toBeNull();
		expect(job.work_mode).toBeNull();
	});
});

describe("TrackingEntry shape", () => {
	it("accepts a saved entry", () => {
		const entry: TrackingEntry = {
			job_id: "abc123",
			status: "saved",
			title: "Senior Engineer",
			company: "Acme",
			url: "https://example.com/jobs/1",
			source: "remoteok",
			saved_at: utcNow(),
			applied_at: null,
			updated_at: utcNow(),
			last_seen_at: null,
			notes: null,
		};
		expect(entry.status).toBe("saved");
		expect(entry.applied_at).toBeNull();
	});
});

describe("BriefingRun shape", () => {
	it("accepts a complete run record", () => {
		const run: BriefingRun = {
			run_id: "run-uuid-1234",
			run_at: utcNow(),
			dry_run: false,
			jobs_fetched: 50,
			jobs_ranked: 45,
			jobs_matched: 3,
			sources: { remoteok: 30, hackernews: 20 },
			timings: {
				fetch_ms: 1200,
				rank_ms: 50,
				draft_ms: 80,
				persist_ms: 20,
			},
			version: "1.0.3",
		};
		expect(run.jobs_matched).toBe(3);
		expect(run.dry_run).toBe(false);
	});
});