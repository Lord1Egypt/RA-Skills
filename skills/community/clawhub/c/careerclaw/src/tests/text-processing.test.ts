/**
 * text-processing.test.ts — Unit tests for core text processing utilities.
 * Run: npm test
 */

import { describe, it, expect } from "vitest";
import {
  STOPWORDS,
  SECTION_WEIGHTS,
  tokenize,
  tokenizeUnique,
  extractPhrases,
  extractPhrasesFromText,
  tokenOverlap,
  matchedTokens,
  gapTokens,
} from "../core/text-processing.js";

// ---------------------------------------------------------------------------
// STOPWORDS
// ---------------------------------------------------------------------------

describe("STOPWORDS", () => {
  it("filters common English function words", () => {
    for (const word of ["the", "a", "an", "and", "or", "is", "in", "of"]) {
      expect(STOPWORDS.has(word)).toBe(true);
    }
  });

  it("filters recruitment boilerplate terms", () => {
    for (const word of [
      "apply", "applicant", "candidate", "candidates", "interview",
      "hiring", "submit", "competitive", "opportunity", "benefits",
    ]) {
      expect(STOPWORDS.has(word)).toBe(true);
    }
  });

  it("does NOT filter technical skill tokens", () => {
    for (const word of [
      "typescript", "python", "react", "node", "kubernetes",
      "postgres", "graphql", "redis", "docker", "aws",
    ]) {
      expect(STOPWORDS.has(word)).toBe(false);
    }
  });

  it("does NOT filter professional role tokens", () => {
    for (const word of ["engineer", "senior", "staff", "principal", "architect"]) {
      expect(STOPWORDS.has(word)).toBe(false);
    }
  });
});

// ---------------------------------------------------------------------------
// SECTION_WEIGHTS
// ---------------------------------------------------------------------------

describe("SECTION_WEIGHTS", () => {
  it("skills has the highest weight (1.0)", () => {
    expect(SECTION_WEIGHTS["skills"]).toBe(1.0);
  });

  it("all weights are in (0, 1]", () => {
    for (const w of Object.values(SECTION_WEIGHTS)) {
      expect(w).toBeGreaterThan(0);
      expect(w).toBeLessThanOrEqual(1.0);
    }
  });

  it("skills > summary > experience > education", () => {
    expect(SECTION_WEIGHTS["skills"]!).toBeGreaterThan(SECTION_WEIGHTS["summary"]!);
    expect(SECTION_WEIGHTS["summary"]!).toBeGreaterThan(SECTION_WEIGHTS["experience"]!);
    expect(SECTION_WEIGHTS["experience"]!).toBeGreaterThan(SECTION_WEIGHTS["education"]!);
  });
});

// ---------------------------------------------------------------------------
// tokenize
// ---------------------------------------------------------------------------

describe("tokenize", () => {
  it("lowercases all tokens", () => {
    const tokens = tokenize("TypeScript Python REACT");
    expect(tokens).toEqual(["typescript", "python", "react"]);
  });

  it("splits on whitespace and punctuation", () => {
    expect(tokenize("node.js, react; sql")).toContain("node.js");
    expect(tokenize("node.js, react; sql")).toContain("react");
    expect(tokenize("node.js, react; sql")).toContain("sql");
  });

  it("filters stopwords", () => {
    const tokens = tokenize("we are looking for a senior engineer");
    expect(tokens).not.toContain("we");
    expect(tokens).not.toContain("are");
    expect(tokens).not.toContain("looking");
    expect(tokens).not.toContain("for");
    expect(tokens).not.toContain("a");
    expect(tokens).toContain("senior");
    expect(tokens).toContain("engineer");
  });

  it("filters recruitment boilerplate", () => {
    const tokens = tokenize("candidates must apply and submit their application");
    expect(tokens).not.toContain("candidates");
    expect(tokens).not.toContain("apply");
    expect(tokens).not.toContain("submit");
    expect(tokens).not.toContain("application");
  });

  it("drops tokens shorter than 2 characters", () => {
    const tokens = tokenize("a b go do it");
    expect(tokens.some((t) => t.length < 2)).toBe(false);
  });

  it("preserves hyphenated tokens", () => {
    expect(tokenize("full-stack developer")).toContain("full-stack");
  });

  it("returns empty array for empty input", () => {
    expect(tokenize("")).toEqual([]);
  });

  it("returns empty array for all-stopword input", () => {
    expect(tokenize("the a an and or")).toEqual([]);
  });
});

// ---------------------------------------------------------------------------
// tokenizeUnique
// ---------------------------------------------------------------------------

describe("tokenizeUnique", () => {
  it("deduplicates repeated tokens", () => {
    const tokens = tokenizeUnique("senior engineer senior typescript engineer");
    expect(tokens.filter((t) => t === "senior")).toHaveLength(1);
    expect(tokens.filter((t) => t === "engineer")).toHaveLength(1);
  });

  it("preserves insertion order", () => {
    const tokens = tokenizeUnique("python react typescript");
    expect(tokens).toEqual(["python", "react", "typescript"]);
  });
});

// ---------------------------------------------------------------------------
// extractPhrases
// ---------------------------------------------------------------------------

describe("extractPhrases", () => {
  it("produces bigrams from a token stream", () => {
    const phrases = extractPhrases(["senior", "software", "engineer"]);
    expect(phrases).toContain("senior software");
    expect(phrases).toContain("software engineer");
  });

  it("produces trigrams from a token stream", () => {
    const phrases = extractPhrases(["senior", "software", "engineer"]);
    expect(phrases).toContain("senior software engineer");
  });

  it("returns empty array for single token", () => {
    expect(extractPhrases(["engineer"])).toEqual([]);
  });

  it("returns empty array for empty input", () => {
    expect(extractPhrases([])).toEqual([]);
  });

  it("produces n-1 bigrams for n tokens", () => {
    const tokens = ["a", "b", "c", "d"];
    const bigrams = extractPhrases(tokens).filter((p) => p.split(" ").length === 2);
    expect(bigrams).toHaveLength(3);
  });
});

// ---------------------------------------------------------------------------
// extractPhrasesFromText
// ---------------------------------------------------------------------------

describe("extractPhrasesFromText", () => {
  it("tokenizes then extracts phrases end-to-end", () => {
    const phrases = extractPhrasesFromText(
      "We need a Senior TypeScript Engineer for our team"
    );
    expect(phrases).toContain("senior typescript");
    expect(phrases).toContain("typescript engineer");
    expect(phrases).toContain("senior typescript engineer");
  });

  it("returns unique phrases only", () => {
    const phrases = extractPhrasesFromText("python python python");
    // After tokenizing: ["python", "python", "python"] → dedupe not done at token level
    // Phrase dedup should still work
    const set = new Set(phrases);
    expect(set.size).toBe(phrases.length);
  });
});

// ---------------------------------------------------------------------------
// tokenOverlap
// ---------------------------------------------------------------------------

describe("tokenOverlap", () => {
  it("returns 1.0 for identical sets", () => {
    expect(tokenOverlap(["a", "b"], ["a", "b"])).toBe(1.0);
  });

  it("returns 0.0 for disjoint sets", () => {
    expect(tokenOverlap(["a", "b"], ["c", "d"])).toBe(0.0);
  });

  it("returns 0.0 for two empty arrays", () => {
    expect(tokenOverlap([], [])).toBe(0.0);
  });

  it("returns partial overlap correctly", () => {
    // intersection={b}, union={a,b,c} → 1/3
    expect(tokenOverlap(["a", "b"], ["b", "c"])).toBeCloseTo(1 / 3, 5);
  });
});

// ---------------------------------------------------------------------------
// matchedTokens / gapTokens
// ---------------------------------------------------------------------------

describe("matchedTokens", () => {
  it("returns tokens in query that are present in corpus", () => {
    expect(matchedTokens(["python", "react", "rust"], ["python", "typescript", "react"])).toEqual(
      ["python", "react"]
    );
  });

  it("returns empty array when no overlap", () => {
    expect(matchedTokens(["rust"], ["python"])).toEqual([]);
  });

  it("deduplicates matches", () => {
    expect(matchedTokens(["python", "python"], ["python"])).toEqual(["python"]);
  });
});

describe("gapTokens", () => {
  it("returns tokens in query absent from corpus", () => {
    expect(gapTokens(["python", "react", "rust"], ["python", "react"])).toEqual(["rust"]);
  });

  it("returns all tokens when corpus is empty", () => {
    expect(gapTokens(["python", "react"], [])).toEqual(["python", "react"]);
  });

  it("returns empty array when all tokens are covered", () => {
    expect(gapTokens(["python"], ["python", "react"])).toEqual([]);
  });
});
