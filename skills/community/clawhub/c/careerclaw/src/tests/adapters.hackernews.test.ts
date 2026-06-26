/**
 * adapters.hackernews.test.ts — Offline contract tests for the HN adapter.
 *
 * Tests call parseComment() directly with fixture JSON — no network calls.
 * Run with: npm test
 */

import { readFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, it, expect } from "vitest";
import { parseComment } from "../adapters/hackernews.js";
import type { HnItem } from "../adapters/hackernews.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

function loadFixture(name: string): HnItem {
  const raw = readFileSync(resolve(__dirname, "fixtures", name), "utf-8");
  return JSON.parse(raw) as HnItem;
}

const jobComment = loadFixture("hn-comment-job.json");
const deletedComment = loadFixture("hn-comment-deleted.json");

describe("parseComment — job comment", () => {
  it("parses company from pipe-separated header", () => {
    const job = parseComment(jobComment);
    expect(job.company).toBe("Starbridge AI");
  });

  it("parses title from second pipe segment", () => {
    const job = parseComment(jobComment);
    expect(job.title).toBe("Senior Backend Engineer");
  });

  it("parses location from third pipe segment", () => {
    const job = parseComment(jobComment);
    expect(job.location).toBe("NYC or Remote");
  });

  it("sets source='hackernews'", () => {
    expect(parseComment(jobComment).source).toBe("hackernews");
  });

  it("builds canonical_url from item id", () => {
    const job = parseComment(jobComment);
    expect(job.url).toBe(
      `https://news.ycombinator.com/item?id=${jobComment.id}`
    );
  });

  it("job_id is 16 hex chars derived from canonical_url", () => {
    const job = parseComment(jobComment);
    expect(job.job_id).toHaveLength(16);
    expect(job.job_id).toMatch(/^[0-9a-f]{16}$/);
  });

  it("job_id is stable (same input → same output)", () => {
    expect(parseComment(jobComment).job_id).toBe(
      parseComment(jobComment).job_id
    );
  });

  it("converts unix timestamp to ISO posted_at", () => {
    const job = parseComment(jobComment);
    expect(job.posted_at).toMatch(/^\d{4}-\d{2}-\d{2}T/);
    // time=1741014000 → 2026-03-03
    expect(job.posted_at).toContain("2026-03-03");
  });

  it("strips HTML tags from description", () => {
    const job = parseComment(jobComment);
    expect(job.description).not.toContain("<p>");
    expect(job.description).not.toContain("&#x27;");
    expect(job.description.toLowerCase()).toContain("we're building");
  });

  it("infers work_mode=remote from location 'NYC or Remote'", () => {
    expect(parseComment(jobComment).work_mode).toBe("remote");
  });

  it("extracts experience_years from description", () => {
    expect(parseComment(jobComment).experience_years).toBe(3);
  });

  it("extracts salary_min from description ($130k)", () => {
    const job = parseComment(jobComment);
    expect(job.salary_min).toBe(130_000);
  });

  it("uses provided fetched_at when supplied", () => {
    const ts = "2026-03-03T10:00:00.000Z";
    expect(parseComment(jobComment, ts).fetched_at).toBe(ts);
  });
});

describe("parseComment — deleted/dead items", () => {
  it("throws for deleted items", () => {
    expect(() => parseComment(deletedComment)).toThrow();
  });

  it("throws for items with no text", () => {
    const noText: HnItem = { id: 99999, type: "comment", by: "user" };
    expect(() => parseComment(noText)).toThrow();
  });

  it("throws for non-comment item types", () => {
    const story: HnItem = {
      id: 88888,
      type: "story",
      text: "Company | Role | Remote",
    };
    expect(() => parseComment(story)).toThrow();
  });
});

describe("parseComment — header format edge cases", () => {
  it("handles dash-separated header when no pipes present", () => {
    const item: HnItem = {
      id: 11111,
      type: "comment",
      time: 1741014000,
      text: "Dash Corp - Staff Engineer - Remote\n<p>We build things.</p>",
    };
    const job = parseComment(item);
    expect(job.company).toBe("Dash Corp");
    expect(job.title).toBe("Staff Engineer");
  });

  it("handles minimal header with only company", () => {
    const item: HnItem = {
      id: 22222,
      type: "comment",
      time: 1741014000,
      text: "Solo Company\n<p>Description here.</p>",
    };
    const job = parseComment(item);
    expect(job.company).toBe("Solo Company");
    expect(job.title).toBe("");
    expect(job.location).toBe("");
  });
});
