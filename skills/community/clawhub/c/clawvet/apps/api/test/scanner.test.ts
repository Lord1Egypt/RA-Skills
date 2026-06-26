import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { scanSkill } from "../src/services/scanner.js";

const fixture = (name: string) =>
  readFileSync(join(__dirname, "fixtures", name, "SKILL.md"), "utf-8");

describe("scanner", () => {
  it("gives benign weather skill a low risk score", async () => {
    const result = await scanSkill(fixture("benign-weather"));
    expect(result.riskScore).toBeLessThanOrEqual(25);
    expect(result.riskGrade).toMatch(/^[AB]$/);
  });

  it("detects malicious stealer as critical", async () => {
    const result = await scanSkill(fixture("malicious-stealer"));
    expect(result.riskScore).toBeGreaterThanOrEqual(50);
    expect(result.findingsCount.critical).toBeGreaterThan(0);
    expect(result.recommendation).toBe("block");
  });

  it("detects prompt injection", async () => {
    const result = await scanSkill(fixture("sneaky-injection"));
    const categories = result.findings.map((f) => f.category);
    expect(categories).toContain("prompt_injection");
  });

  it("detects typosquat", async () => {
    const result = await scanSkill(fixture("typosquat-todoistt"));
    const categories = result.findings.map((f) => f.category);
    expect(categories).toContain("typosquatting");
  });

  it("detects credential leaking", async () => {
    const result = await scanSkill(fixture("leaky-creds"));
    const categories = result.findings.map((f) => f.category);
    expect(categories).toContain("credential_theft");
  });

  it("detects obfuscated payloads", async () => {
    const result = await scanSkill(fixture("obfuscated-payload"));
    expect(result.findingsCount.critical).toBeGreaterThan(0);
    expect(result.riskScore).toBeGreaterThanOrEqual(50);
  });
});
