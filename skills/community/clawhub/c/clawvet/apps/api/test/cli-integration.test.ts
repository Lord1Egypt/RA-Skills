import { describe, it, expect } from "vitest";
import { execSync } from "node:child_process";
import { join } from "node:path";

const ROOT = join(__dirname, "..", "..", "..");
const CLI = `npx tsx ${join(ROOT, "packages/cli/src/index.ts")}`;
const FIXTURES = join(__dirname, "fixtures");

function run(args: string): { stdout: string; exitCode: number } {
  try {
    const stdout = execSync(`${CLI} ${args}`, {
      cwd: ROOT,
      encoding: "utf-8",
      env: { ...process.env, NODE_NO_WARNINGS: "1" },
      stdio: ["pipe", "pipe", "pipe"],
    });
    return { stdout, exitCode: 0 };
  } catch (err: any) {
    return { stdout: err.stdout || "", exitCode: err.status || 1 };
  }
}

describe("CLI integration", () => {
  it("clawvet --version prints version", () => {
    const { stdout, exitCode } = run("--version");
    expect(exitCode).toBe(0);
    expect(stdout.trim()).toBe("0.6.0");
  });

  it("clawvet --help shows usage", () => {
    const { stdout, exitCode } = run("--help");
    expect(exitCode).toBe(0);
    expect(stdout).toContain("scan");
    expect(stdout).toContain("audit");
    expect(stdout).toContain("watch");
  });

  it("clawvet scan with nonexistent path exits 1", () => {
    const { exitCode } = run("scan /nonexistent/path/to/skill");
    expect(exitCode).toBe(1);
  });

  it("clawvet scan benign-weather --format json produces valid JSON", () => {
    const { stdout, exitCode } = run(
      `scan ${join(FIXTURES, "benign-weather")} --format json`
    );
    expect(exitCode).toBe(0);
    const result = JSON.parse(stdout);
    expect(result.skillName).toBe("weather-forecast");
    expect(result.riskGrade).toBe("A");
    expect(result.status).toBe("complete");
    expect(Array.isArray(result.findings)).toBe(true);
  });

  it("clawvet scan malicious-stealer --format json --fail-on high exits 1", () => {
    const { stdout, exitCode } = run(
      `scan ${join(FIXTURES, "malicious-stealer")} --format json --fail-on high`
    );
    expect(exitCode).toBe(1);
    const result = JSON.parse(stdout);
    expect(result.riskScore).toBe(100);
  });

  it("clawvet scan benign-weather --fail-on critical exits 0", () => {
    const { stdout, exitCode } = run(
      `scan ${join(FIXTURES, "benign-weather")} --format json --fail-on critical`
    );
    expect(exitCode).toBe(0);
  });

  it("clawvet scan on a direct SKILL.md file path works", () => {
    const { stdout, exitCode } = run(
      `scan ${join(FIXTURES, "benign-weather", "SKILL.md")} --format json`
    );
    expect(exitCode).toBe(0);
    const result = JSON.parse(stdout);
    expect(result.skillName).toBe("weather-forecast");
  });

  it("all 6 fixtures produce consistent results across runs", { timeout: 60000 }, () => {
    const fixtures = [
      "benign-weather",
      "malicious-stealer",
      "sneaky-injection",
      "typosquat-todoistt",
      "leaky-creds",
      "obfuscated-payload",
    ];

    for (const fixture of fixtures) {
      const r1 = run(`scan ${join(FIXTURES, fixture)} --format json`);
      const r2 = run(`scan ${join(FIXTURES, fixture)} --format json`);

      const result1 = JSON.parse(r1.stdout);
      const result2 = JSON.parse(r2.stdout);

      expect(result1.riskScore).toBe(result2.riskScore);
      expect(result1.riskGrade).toBe(result2.riskGrade);
      expect(result1.findings.length).toBe(result2.findings.length);
    }
  });

  it("terminal output contains expected sections", () => {
    const { stdout, exitCode } = run(
      `scan ${join(FIXTURES, "malicious-stealer")}`
    );
    expect(exitCode).toBe(0);
    expect(stdout).toContain("ClawVet Scan Report");
    expect(stdout).toContain("productivity-boost");
    expect(stdout).toContain("Risk Score:");
    expect(stdout).toContain("Findings:");
    expect(stdout).toContain("Recommendation:");
    expect(stdout).toContain("BLOCK");
  });
});
