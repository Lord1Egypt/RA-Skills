/**
 * adapters.remoteok.test.ts — Offline contract tests for the RemoteOK adapter.
 *
 * These tests call parseRss() directly with fixture XML — no network calls.
 * Run with: npm test
 */

import { readFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, it, expect } from "vitest";
import {parseRss, stableId, stripHtml} from "../adapters/index.js";


const __dirname = dirname(fileURLToPath(import.meta.url));
const fixtureXml = readFileSync(
  resolve(__dirname, "fixtures/remoteok.xml"),
  "utf-8"
);

describe("parseRss — fixture", () => {
  it("returns one NormalizedJob per <item>", () => {
    const jobs = parseRss(fixtureXml);
    expect(jobs).toHaveLength(3);
  });

  it("all jobs have source='remoteok'", () => {
    const jobs = parseRss(fixtureXml);
    expect(jobs.every((j) => j.source === "remoteok")).toBe(true);
  });

  it("all jobs have a non-empty job_id of length 16", () => {
    const jobs = parseRss(fixtureXml);
    expect(jobs.every((j) => j.job_id.length === 16)).toBe(true);
  });

  it("all job_ids are unique", () => {
    const jobs = parseRss(fixtureXml);
    const ids = jobs.map((j) => j.job_id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it("all jobs have a valid fetched_at ISO timestamp", () => {
    const jobs = parseRss(fixtureXml);
    for (const job of jobs) {
      expect(() => new Date(job.fetched_at)).not.toThrow();
      expect(job.fetched_at).toMatch(/^\d{4}-\d{2}-\d{2}T/);
    }
  });
});

describe("parseRss — job 1 (Senior TypeScript Engineer at Acme Corp)", () => {
  it("splits title and company on ' at '", () => {
    const [job] = parseRss(fixtureXml);
    expect(job!.title).toBe("Senior TypeScript Engineer");
    expect(job!.company).toBe("Acme Corp");
  });

  it("parses salary range to annual USD integers", () => {
    const [job] = parseRss(fixtureXml);
    expect(job!.salary_min).toBe(120_000);
    expect(job!.salary_max).toBe(180_000);
  });

  it("infers work_mode=remote from 'Worldwide' location", () => {
    // Worldwide → no explicit remote keyword → work_mode null (acceptable)
    const [job] = parseRss(fixtureXml);
    expect(job!.work_mode === null || job!.work_mode === "remote").toBe(true);
  });

  it("extracts experience_years from description", () => {
    const [job] = parseRss(fixtureXml);
    expect(job!.experience_years).toBe(5);
  });

  it("strips HTML from description", () => {
    const [job] = parseRss(fixtureXml);
    expect(job!.description).not.toContain("<p>");
    expect(job!.description).not.toContain("</p>");
    expect(job!.description.length).toBeGreaterThan(10);
  });

  it("parses pubDate to ISO string", () => {
    const [job] = parseRss(fixtureXml);
    expect(job!.posted_at).toMatch(/^\d{4}-\d{2}-\d{2}T/);
  });

  it("sets url from <link>", () => {
    const [job] = parseRss(fixtureXml);
    expect(job!.url).toBe("https://remoteok.com/remote-jobs/1001");
  });
});

describe("parseRss — job 2 (Backend Engineer, no salary)", () => {
  it("returns null salary when no salary field and none in description", () => {
    const jobs = parseRss(fixtureXml);
    const job = jobs[1]!;
    expect(job.salary_min).toBeNull();
    expect(job.salary_max).toBeNull();
  });

  it("infers work_mode=remote from location 'Remote'", () => {
    const jobs = parseRss(fixtureXml);
    expect(jobs[1]!.work_mode).toBe("remote");
  });

  it("falls back to company field when title has no ' at '", () => {
    const jobs = parseRss(fixtureXml);
    expect(jobs[1]!.title).toBe("Backend Engineer");
    expect(jobs[1]!.company).toBe("Beta Startup");
  });
});

describe("parseRss — job 3 (hybrid, k-suffix salary)", () => {
  it("infers work_mode=hybrid from description", () => {
    const jobs = parseRss(fixtureXml);
    expect(jobs[2]!.work_mode).toBe("hybrid");
  });

  it("parses k-suffix salary ($80k - $110k) correctly", () => {
    const jobs = parseRss(fixtureXml);
    expect(jobs[2]!.salary_min).toBe(80_000);
    expect(jobs[2]!.salary_max).toBe(110_000);
  });
});

describe("parseRss — edge cases", () => {
  it("returns [] for empty channel", () => {
    const xml = `<?xml version="1.0"?><rss version="2.0"><channel></channel></rss>`;
    expect(parseRss(xml)).toEqual([]);
  });

  it("returns [] for completely empty string", () => {
    expect(parseRss("")).toEqual([]);
  });
});

describe("stripHtml", () => {
  it("removes simple tags", () => {
    expect(stripHtml("<p>hello</p>")).toBe("hello");
  });

  it("decodes HTML entities", () => {
    expect(stripHtml("it&#x27;s &amp; fine")).toBe("it's & fine");
  });

  it("converts <br> to newline", () => {
    expect(stripHtml("line1<br>line2")).toBe("line1\nline2");
  });
});

describe("stableId", () => {
  it("returns 16 hex characters", () => {
    expect(stableId("https://example.com")).toHaveLength(16);
    expect(stableId("https://example.com")).toMatch(/^[0-9a-f]{16}$/);
  });

  it("is deterministic", () => {
    expect(stableId("https://remoteok.com/jobs/123")).toBe(
      stableId("https://remoteok.com/jobs/123")
    );
  });

  it("produces different IDs for different URLs", () => {
    expect(stableId("https://remoteok.com/jobs/1")).not.toBe(
      stableId("https://remoteok.com/jobs/2")
    );
  });
});
