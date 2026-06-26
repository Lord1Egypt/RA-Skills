/**
 * gap.test.ts — Unit tests for gapAnalysis().
 * Run: npm test
 */

import { describe, it, expect } from "vitest";
import { gapAnalysis } from "../gap.js";
import { buildResumeIntelligence } from "../resume-intel.js";
import type { NormalizedJob } from "../models.js";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function makeJob(overrides: Partial<NormalizedJob> = {}): NormalizedJob {
  return {
    job_id: "gap0000000000001",
    title: "Senior TypeScript Engineer",
    company: "Acme",
    location: "Remote",
    description:
      "We need a senior typescript engineer with react, node, and aws experience. 5+ years required.",
    url: "https://example.com/job/1",
    source: "remoteok",
    salary_min: null,
    salary_max: null,
    work_mode: "remote",
    experience_years: 5,
    posted_at: null,
    fetched_at: "2026-03-04T10:00:00.000Z",
    ...overrides,
  };
}

// ---------------------------------------------------------------------------
// fit_score — skills injection improves score (PR-E acceptance criterion)
// ---------------------------------------------------------------------------

describe("gapAnalysis — fit_score", () => {
  it("fit_score is higher when resume includes job tech stack", () => {
    const intelWithSkills = buildResumeIntelligence({
      resume_summary: "Experienced engineer.",
      skills: ["typescript", "react", "node", "aws"],
    });
    const intelWithoutSkills = buildResumeIntelligence({
      resume_summary: "Experienced engineer.",
    });

    const resultWith = gapAnalysis(intelWithSkills, makeJob());
    const resultWithout = gapAnalysis(intelWithoutSkills, makeJob());

    expect(resultWith.fit_score).toBeGreaterThan(resultWithout.fit_score);
  });

  it("fit_score is in [0, 1]", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "Senior TypeScript engineer with react and aws.",
      skills: ["typescript", "react", "aws"],
    });
    const result = gapAnalysis(intel, makeJob());
    expect(result.fit_score).toBeGreaterThanOrEqual(0);
    expect(result.fit_score).toBeLessThanOrEqual(1);
  });

  it("fit_score_unweighted is in [0, 1]", () => {
    const intel = buildResumeIntelligence({ resume_summary: "Engineer." });
    const result = gapAnalysis(intel, makeJob());
    expect(result.fit_score_unweighted).toBeGreaterThanOrEqual(0);
    expect(result.fit_score_unweighted).toBeLessThanOrEqual(1);
  });

  it("fit_score is 0 for empty resume intel vs real job", () => {
    const intel = buildResumeIntelligence({ resume_summary: "" });
    const result = gapAnalysis(intel, makeJob());
    expect(result.fit_score).toBe(0);
  });

  it("fit_score_unweighted is 0 for empty resume intel", () => {
    const intel = buildResumeIntelligence({ resume_summary: "" });
    const result = gapAnalysis(intel, makeJob());
    expect(result.fit_score_unweighted).toBe(0);
  });
});

// ---------------------------------------------------------------------------
// signals (resume ∩ job)
// ---------------------------------------------------------------------------

describe("gapAnalysis — signals", () => {
  it("signals.keywords contains skills present in the job", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "",
      skills: ["typescript", "react", "python"],
    });
    const result = gapAnalysis(intel, makeJob());
    expect(result.signals.keywords).toContain("typescript");
    expect(result.signals.keywords).toContain("react");
  });

  it("signals.keywords does not contain skills absent from the job", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "",
      skills: ["python", "django"],
    });
    const result = gapAnalysis(intel, makeJob());
    expect(result.signals.keywords).not.toContain("python");
    expect(result.signals.keywords).not.toContain("django");
  });

  it("signals are empty for empty resume intel", () => {
    const intel = buildResumeIntelligence({ resume_summary: "" });
    const result = gapAnalysis(intel, makeJob());
    expect(result.signals.keywords).toEqual([]);
    expect(result.signals.phrases).toEqual([]);
  });
});

// ---------------------------------------------------------------------------
// gaps (job − resume)
// ---------------------------------------------------------------------------

describe("gapAnalysis — gaps", () => {
  it("gaps.keywords contains job keywords absent from resume", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "Python developer.",
    });
    const result = gapAnalysis(intel, makeJob());
    // Job has typescript, react, node, aws — none in resume
    expect(result.gaps.keywords).toContain("typescript");
    expect(result.gaps.keywords).toContain("react");
  });

  it("gaps.keywords does not include skills already in resume", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "",
      skills: ["typescript", "react", "node", "aws"],
    });
    const result = gapAnalysis(intel, makeJob());
    expect(result.gaps.keywords).not.toContain("typescript");
    expect(result.gaps.keywords).not.toContain("react");
    expect(result.gaps.keywords).not.toContain("aws");
  });
});

// ---------------------------------------------------------------------------
// summary shape
// ---------------------------------------------------------------------------

describe("gapAnalysis — summary", () => {
  it("top_signals.keywords has at most 5 entries", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "TypeScript react node aws python java kotlin rust go ruby engineer senior staff",
    });
    const result = gapAnalysis(intel, makeJob());
    expect(result.summary.top_signals.keywords.length).toBeLessThanOrEqual(5);
  });

  it("top_gaps.keywords has at most 5 entries", () => {
    const intel = buildResumeIntelligence({ resume_summary: "" });
    const result = gapAnalysis(intel, makeJob());
    expect(result.summary.top_gaps.keywords.length).toBeLessThanOrEqual(5);
  });

  it("top_signals are a subset of signals.keywords", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "",
      skills: ["typescript", "react", "node", "aws"],
    });
    const result = gapAnalysis(intel, makeJob());
    const signalSet = new Set(result.signals.keywords);
    for (const k of result.summary.top_signals.keywords) {
      expect(signalSet.has(k)).toBe(true);
    }
  });

  it("top_gaps are a subset of gaps.keywords", () => {
    const intel = buildResumeIntelligence({ resume_summary: "" });
    const result = gapAnalysis(intel, makeJob());
    const gapSet = new Set(result.gaps.keywords);
    for (const k of result.summary.top_gaps.keywords) {
      expect(gapSet.has(k)).toBe(true);
    }
  });
});

// ---------------------------------------------------------------------------
// edge cases
// ---------------------------------------------------------------------------

describe("gapAnalysis — edge cases", () => {
  it("handles job with empty title and description", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "Senior engineer.",
      skills: ["typescript"],
    });
    const emptyJob = makeJob({ title: "", description: "" });
    const result = gapAnalysis(intel, emptyJob);
    expect(result.fit_score).toBe(0);
    expect(result.gaps.keywords).toEqual([]);
  });

  it("handles both empty resume and empty job gracefully", () => {
    const intel = buildResumeIntelligence({ resume_summary: "" });
    const emptyJob = makeJob({ title: "", description: "" });
    expect(() => gapAnalysis(intel, emptyJob)).not.toThrow();
  });
});
