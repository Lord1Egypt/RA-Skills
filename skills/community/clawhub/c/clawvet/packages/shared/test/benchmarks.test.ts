import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { scanSkill } from "../src/index.js";

const BENCHMARKS_DIR = resolve(__dirname, "../../../benchmarks");

function loadSkill(category: string, name: string): string {
  return readFileSync(resolve(BENCHMARKS_DIR, category, name, "SKILL.md"), "utf-8");
}

describe("Benchmark suite", () => {
  describe("Malicious skills should score >= 50", () => {
    const malicious = [
      "rce-base64",
      "credential-theft",
      "prompt-injection",
      "obfuscated-shell",
      "typosquat",
    ];

    for (const name of malicious) {
      it(`${name} should be flagged as risky`, async () => {
        const content = loadSkill("malicious", name);
        const result = await scanSkill(content);
        expect(result.riskScore).toBeGreaterThanOrEqual(50);
        expect(result.findings.length).toBeGreaterThan(0);
      });
    }
  });

  describe("Benign skills should score <= 25", () => {
    const benign = [
      "todo-app",
      "git-helper",
      "markdown-formatter",
      "api-client",
      "file-organizer",
    ];

    for (const name of benign) {
      it(`${name} should be considered safe`, async () => {
        const content = loadSkill("benign", name);
        const result = await scanSkill(content);
        expect(result.riskScore).toBeLessThanOrEqual(25);
      });
    }
  });
});
