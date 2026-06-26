/**
 * drafting.test.ts — Unit tests for draftOutreach().
 * Run: npm test
 */

import { describe, it, expect } from "vitest";
import { draftOutreach } from "../drafting.js";
import { emptyProfile } from "../models.js";
import type { NormalizedJob, UserProfile } from "../models.js";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function makeJob(overrides: Partial<NormalizedJob> = {}): NormalizedJob {
  return {
    job_id: "draft000000000001",
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
    fetched_at: "2026-03-04T10:00:00.000Z",
    ...overrides,
  };
}

function makeProfile(overrides: Partial<UserProfile> = {}): UserProfile {
  return { ...emptyProfile(), experience_years: 6, ...overrides };
}

// ---------------------------------------------------------------------------
// OutreachDraft shape
// ---------------------------------------------------------------------------

describe("draftOutreach — shape", () => {
  it("returns all required OutreachDraft fields", () => {
    const draft = draftOutreach(makeJob(), makeProfile());
    expect(draft).toHaveProperty("job_id");
    expect(draft).toHaveProperty("subject");
    expect(draft).toHaveProperty("body");
    expect(draft).toHaveProperty("llm_enhanced");
  });

  it("job_id matches the input job", () => {
    const job = makeJob({ job_id: "abc123" });
    expect(draftOutreach(job, makeProfile()).job_id).toBe("abc123");
  });

  it("llm_enhanced is always false", () => {
    expect(draftOutreach(makeJob(), makeProfile()).llm_enhanced).toBe(false);
    expect(
      draftOutreach(makeJob(), makeProfile(), ["typescript", "react"]).llm_enhanced
    ).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// Subject line
// ---------------------------------------------------------------------------

describe("draftOutreach — subject", () => {
  it("subject contains the job title", () => {
    const draft = draftOutreach(makeJob({ title: "Staff Engineer" }), makeProfile());
    expect(draft.subject).toContain("Staff Engineer");
  });

  it("subject contains the company name", () => {
    const draft = draftOutreach(makeJob({ company: "Stripe" }), makeProfile());
    expect(draft.subject).toContain("Stripe");
  });

  it("subject follows the expected format", () => {
    const draft = draftOutreach(
      makeJob({ title: "Senior TypeScript Engineer", company: "Acme" }),
      makeProfile()
    );
    expect(draft.subject).toBe("Interest in Senior TypeScript Engineer at Acme");
  });
});

// ---------------------------------------------------------------------------
// Body — structure
// ---------------------------------------------------------------------------

describe("draftOutreach — body structure", () => {
  it("body opens with company greeting", () => {
    const draft = draftOutreach(makeJob({ company: "Stripe" }), makeProfile());
    expect(draft.body).toMatch(/^Hi Stripe team,/);
  });

  it("body mentions the job title", () => {
    const draft = draftOutreach(makeJob({ title: "Staff Engineer" }), makeProfile());
    expect(draft.body).toContain("Staff Engineer");
  });

  it("body mentions the company name", () => {
    const draft = draftOutreach(makeJob({ company: "Stripe" }), makeProfile());
    expect(draft.body).toContain("Stripe");
  });

  it("body ends with sign-off", () => {
    const draft = draftOutreach(makeJob(), makeProfile());
    expect(draft.body).toContain("Best regards,");
    expect(draft.body).toContain("[Your Name]");
  });

  it("body word count is in [150, 250]", () => {
    const draft = draftOutreach(
      makeJob(),
      makeProfile(),
      ["typescript", "react", "node"]
    );
    const wordCount = draft.body.split(/\s+/).filter(Boolean).length;
    expect(wordCount).toBeGreaterThanOrEqual(150);
    expect(wordCount).toBeLessThanOrEqual(250);
  });
});

// ---------------------------------------------------------------------------
// Body — experience clause
// ---------------------------------------------------------------------------

describe("draftOutreach — experience clause", () => {
  it("inserts experience_years when set", () => {
    const draft = draftOutreach(makeJob(), makeProfile({ experience_years: 8 }));
    expect(draft.body).toContain("8+ years of experience");
  });

  it("falls back to 'extensive experience' when experience_years is null", () => {
    const draft = draftOutreach(makeJob(), makeProfile({ experience_years: null }));
    expect(draft.body).toContain("extensive experience");
    expect(draft.body).not.toContain("null");
  });
});

// ---------------------------------------------------------------------------
// Body — matched keyword highlights
// ---------------------------------------------------------------------------

describe("draftOutreach — matched keywords", () => {
  it("includes matched keywords in the body when provided", () => {
    const draft = draftOutreach(makeJob(), makeProfile(), ["typescript", "react"]);
    expect(draft.body.toLowerCase()).toContain("typescript");
    expect(draft.body.toLowerCase()).toContain("react");
  });

  it("uses at most 3 matched keywords", () => {
    const keywords = ["typescript", "react", "node", "aws", "postgres"];
    const draft = draftOutreach(makeJob(), makeProfile(), keywords);
    // "aws" and "postgres" are 4th and 5th — should not appear
    expect(draft.body.toLowerCase()).not.toContain("aws");
    expect(draft.body.toLowerCase()).not.toContain("postgres");
  });

  it("falls back gracefully when matched_keywords is empty", () => {
    expect(() => draftOutreach(makeJob(), makeProfile(), [])).not.toThrow();
    const draft = draftOutreach(makeJob(), makeProfile(), []);
    expect(draft.body).toBeTruthy();
  });

  it("falls back gracefully when matched_keywords is not provided", () => {
    expect(() => draftOutreach(makeJob(), makeProfile())).not.toThrow();
  });

  it("fallback clause mentions job title when no keywords", () => {
    const draft = draftOutreach(
      makeJob({ title: "Staff Engineer" }),
      makeProfile(),
      []
    );
    expect(draft.body).toContain("Staff Engineer");
  });
});

// ---------------------------------------------------------------------------
// Determinism
// ---------------------------------------------------------------------------

describe("draftOutreach — determinism", () => {
  it("produces identical output for identical inputs", () => {
    const job = makeJob();
    const profile = makeProfile();
    const keywords = ["typescript", "react"];

    const draft1 = draftOutreach(job, profile, keywords);
    const draft2 = draftOutreach(job, profile, keywords);

    expect(draft1.subject).toBe(draft2.subject);
    expect(draft1.body).toBe(draft2.body);
  });

  it("produces different bodies for different matched keywords", () => {
    const job = makeJob();
    const profile = makeProfile();

    const draft1 = draftOutreach(job, profile, ["typescript"]);
    const draft2 = draftOutreach(job, profile, ["python"]);

    expect(draft1.body).not.toBe(draft2.body);
  });
});
