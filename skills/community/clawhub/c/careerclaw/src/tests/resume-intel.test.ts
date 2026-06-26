/**
 * resume-intel.test.ts — Unit tests for buildResumeIntelligence().
 * Run: npm test
 */

import { describe, it, expect } from "vitest";
import { buildResumeIntelligence } from "../resume-intel.js";

// ---------------------------------------------------------------------------
// source flag
// ---------------------------------------------------------------------------

describe("buildResumeIntelligence — source flag", () => {
  it("sets source='summary_only' when only summary is provided", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "Senior engineer focused on reliability.",
    });
    expect(intel.source).toBe("summary_only");
  });

  it("sets source='resume_text' when resume_text is provided but no skills", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "Senior engineer.",
      resume_text: "Led migration to TypeScript across three services.",
    });
    expect(intel.source).toBe("resume_text");
  });

  it("sets source='skills_injected' when skills are provided", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "Senior engineer.",
      skills: ["typescript", "react"],
    });
    expect(intel.source).toBe("skills_injected");
  });

  it("sets source='skills_injected' when only target_roles are provided", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "",
      target_roles: ["staff engineer"],
    });
    expect(intel.source).toBe("skills_injected");
  });
});

// ---------------------------------------------------------------------------
// skills injection (PR-E fix)
// ---------------------------------------------------------------------------

describe("buildResumeIntelligence — skills injection", () => {
  it("skills appear in extracted_keywords", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "Experienced engineer.",
      skills: ["typescript", "react", "aws"],
    });
    expect(intel.extracted_keywords).toContain("typescript");
    expect(intel.extracted_keywords).toContain("react");
    expect(intel.extracted_keywords).toContain("aws");
  });

  it("skills receive keyword_weight of 1.0", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "Experienced engineer.",
      skills: ["typescript", "react"],
    });
    expect(intel.keyword_weights["typescript"]).toBe(1.0);
    expect(intel.keyword_weights["react"]).toBe(1.0);
  });

  it("skills appear in impact_signals", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "",
      skills: ["python", "typescript"],
    });
    expect(intel.impact_signals).toContain("python");
    expect(intel.impact_signals).toContain("typescript");
  });

  it("target_roles tokens appear in extracted_keywords", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "",
      target_roles: ["senior engineer", "staff engineer"],
    });
    expect(intel.extracted_keywords).toContain("senior");
    expect(intel.extracted_keywords).toContain("engineer");
    expect(intel.extracted_keywords).toContain("staff");
  });

  it("empty skills list does not break output", () => {
    expect(() =>
      buildResumeIntelligence({ resume_summary: "Engineer.", skills: [] })
    ).not.toThrow();
  });
});

// ---------------------------------------------------------------------------
// keyword extraction
// ---------------------------------------------------------------------------

describe("buildResumeIntelligence — keyword extraction", () => {
  it("extracts keywords from resume_summary", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "Senior engineer focused on systems reliability.",
    });
    expect(intel.extracted_keywords).toContain("senior");
    expect(intel.extracted_keywords).toContain("engineer");
    expect(intel.extracted_keywords).toContain("reliability");
  });

  it("extracted_keywords are unique", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "typescript typescript react",
      skills: ["typescript"],
    });
    expect(
      intel.extracted_keywords.filter((k) => k === "typescript")
    ).toHaveLength(1);
  });

  it("stopwords are not in extracted_keywords", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "I am a senior engineer who is looking for a new role.",
    });
    for (const stopword of ["i", "am", "a", "who", "is", "for"]) {
      expect(intel.extracted_keywords).not.toContain(stopword);
    }
  });

  it("returns empty lists for empty input", () => {
    const intel = buildResumeIntelligence({ resume_summary: "" });
    expect(intel.extracted_keywords).toEqual([]);
    expect(intel.extracted_phrases).toEqual([]);
    expect(intel.impact_signals).toEqual([]);
  });
});

// ---------------------------------------------------------------------------
// phrase extraction
// ---------------------------------------------------------------------------

describe("buildResumeIntelligence — phrase extraction", () => {
  it("extracts bigrams from summary", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "Senior TypeScript engineer with React experience.",
    });
    expect(intel.extracted_phrases).toContain("senior typescript");
    expect(intel.extracted_phrases).toContain("typescript engineer");
  });

  it("extracted_phrases are unique", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "senior typescript engineer",
      skills: ["typescript"],
    });
    const set = new Set(intel.extracted_phrases);
    expect(set.size).toBe(intel.extracted_phrases.length);
  });
});

// ---------------------------------------------------------------------------
// impact_signals
// ---------------------------------------------------------------------------

describe("buildResumeIntelligence — impact_signals", () => {
  it("impact_signals only contains keywords with weight >= 0.8", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "Senior engineer.",
      skills: ["typescript"],
      resume_text: "Worked on distributed systems.",
    });
    for (const signal of intel.impact_signals) {
      expect(intel.keyword_weights[signal]).toBeGreaterThanOrEqual(0.8);
    }
  });

  it("resume_text tokens below 0.8 weight are not in impact_signals", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "",
      resume_text: "Kubernetes deployment pipelines.",
    });
    // resume_text is experience weight (0.6) — should not be in impact_signals
    expect(intel.impact_signals).not.toContain("kubernetes");
    expect(intel.impact_signals).not.toContain("deployment");
  });
});

// ---------------------------------------------------------------------------
// keyword_weights order (higher weight section wins)
// ---------------------------------------------------------------------------

describe("buildResumeIntelligence — keyword_weight precedence", () => {
  it("skill section weight (1.0) beats summary weight (0.8) for same token", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "I use typescript daily.",
      skills: ["typescript"],
    });
    expect(intel.keyword_weights["typescript"]).toBe(1.0);
  });

  it("summary weight (0.8) beats resume_text weight (0.6) for same token", () => {
    const intel = buildResumeIntelligence({
      resume_summary: "Experienced with kubernetes.",
      resume_text: "Deployed kubernetes clusters.",
    });
    expect(intel.keyword_weights["kubernetes"]).toBe(0.8);
  });
});
