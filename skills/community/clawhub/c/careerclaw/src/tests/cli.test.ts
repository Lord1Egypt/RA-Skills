/**
 * cli.test.ts — Unit tests for CLI argument parsing and profile loading.
 *
 * Tests use child_process to invoke the compiled CLI so they exercise
 * real arg parsing and exit codes without mocking Node internals.
 * All tests use --dry-run and injected fixtures to avoid live network
 * calls or filesystem side effects.
 *
 * Run: npm test
 */

import { describe, it, expect } from "vitest";
import { spawnSync } from "child_process";
import { mkdtempSync, writeFileSync } from "fs";
import { tmpdir } from "os";
import { join } from "path";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const CLI = join(process.cwd(), "src/cli.ts");

interface RunResult {
  status: number | null;
  stdout: string;
  stderr: string;
}

function runCli(args: string[], env?: Record<string, string>): RunResult {
  // Use npx + shell:true for cross-platform compatibility (Windows needs tsx.cmd).
  const result = spawnSync("npx", ["tsx", CLI, ...args], {
    encoding: "utf8",
    timeout: 30_000,
    shell: true,
    env: {
      ...process.env,
      // Isolate from real ~/.careerclaw during tests
      CAREERCLAW_DIR: mkdtempSync(join(tmpdir(), "cc-cli-test-")),
      ...env,
    },
  });
  return {
    status: result.status,
    stdout: result.stdout ?? "",
    stderr: result.stderr ?? "",
  };
}

function makeProfileFile(overrides: Record<string, unknown> = {}): string {
  const dir = mkdtempSync(join(tmpdir(), "cc-cli-profile-"));
  const profile = {
    skills: ["typescript", "react", "node"],
    target_roles: ["software engineer"],
    experience_years: 5,
    work_mode: "remote",
    resume_summary: "Senior engineer with 5 years experience.",
    location: "Remote",
    salary_min: 100000,
    ...overrides,
  };
  const path = join(dir, "profile.json");
  writeFileSync(path, JSON.stringify(profile));
  return path;
}

// ---------------------------------------------------------------------------
// --help
// ---------------------------------------------------------------------------

describe("cli --help", () => {
  it("exits 0 and prints usage", () => {
    const { status, stdout } = runCli(["--help"]);
    expect(status).toBe(0);
    expect(stdout).toContain("careerclaw-js");
    expect(stdout).toContain("--profile");
    expect(stdout).toContain("--dry-run");
    expect(stdout).toContain("--json");
    expect(stdout).toContain("--top-k");
    expect(stdout).toContain("--resume-txt");
  });
});

// ---------------------------------------------------------------------------
// Profile loading errors
// ---------------------------------------------------------------------------

describe("cli — profile loading", () => {
  it("exits 1 with clear error when profile file does not exist", () => {
    const { status, stderr } = runCli([
      "--profile", "/nonexistent/profile.json",
      "--dry-run",
    ]);
    expect(status).toBe(1);
    expect(stderr).toMatch(/Profile not found/i);
  });

  it("exits 1 with clear error when profile is not valid JSON", () => {
    const dir = mkdtempSync(join(tmpdir(), "cc-cli-bad-"));
    const badPath = join(dir, "profile.json");
    writeFileSync(badPath, "{ this is not json }");
    const { status, stderr } = runCli(["--profile", badPath, "--dry-run"]);
    expect(status).toBe(1);
    expect(stderr).toMatch(/not valid JSON/i);
  });
});

// ---------------------------------------------------------------------------
// --top-k validation
// ---------------------------------------------------------------------------

describe("cli --top-k", () => {
  it("exits 1 when --top-k is not a positive integer", () => {
    const profilePath = makeProfileFile();
    const { status, stderr } = runCli([
      "--profile", profilePath,
      "--top-k", "0",
      "--dry-run",
    ]);
    expect(status).toBe(1);
    expect(stderr).toMatch(/top-k/i);
  });

  it("exits 1 when --top-k is not a number", () => {
    const profilePath = makeProfileFile();
    const { status, stderr } = runCli([
      "--profile", profilePath,
      "--top-k", "banana",
      "--dry-run",
    ]);
    expect(status).toBe(1);
    expect(stderr).toMatch(/top-k/i);
  });
});

// ---------------------------------------------------------------------------
// --json output
// ---------------------------------------------------------------------------

describe("cli --json", () => {
  it("outputs valid JSON with expected top-level fields", () => {
    const profilePath = makeProfileFile();
    const { status, stdout } = runCli([
      "--profile", profilePath,
      "--json",
      "--dry-run",
    ]);
    expect(status).toBe(0);
    let parsed: Record<string, unknown>;
    expect(() => {
      parsed = JSON.parse(stdout) as Record<string, unknown>;
    }).not.toThrow();
    expect(parsed!).toHaveProperty("run");
    expect(parsed!).toHaveProperty("matches");
    expect(parsed!).toHaveProperty("drafts");
    expect(parsed!).toHaveProperty("tracking");
    expect(parsed!).toHaveProperty("dry_run", true);
  });

  it("--json output contains no ANSI colour codes", () => {
    const profilePath = makeProfileFile();
    const { stdout } = runCli([
      "--profile", profilePath,
      "--json",
      "--dry-run",
    ]);
    // eslint-disable-next-line no-control-regex
    expect(stdout).not.toMatch(/\x1b\[/);
  });
});

// ---------------------------------------------------------------------------
// --dry-run
// ---------------------------------------------------------------------------

describe("cli --dry-run", () => {
  it("exits 0 and prints dry-run notice in console output", () => {
    const profilePath = makeProfileFile();
    const { status, stdout } = runCli([
      "--profile", profilePath,
      "--dry-run",
    ]);
    expect(status).toBe(0);
    expect(stdout).toContain("dry-run");
  });

  it("dry_run flag is true in --json output when --dry-run is passed", () => {
    const profilePath = makeProfileFile();
    const { stdout } = runCli([
      "--profile", profilePath,
      "--json",
      "--dry-run",
    ]);
    const parsed = JSON.parse(stdout) as { dry_run: boolean };
    expect(parsed.dry_run).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// Console output format
// ---------------------------------------------------------------------------

describe("cli — console output format", () => {
  it("prints the briefing header", () => {
    const profilePath = makeProfileFile();
    const { status, stdout } = runCli(["--profile", profilePath, "--dry-run"]);
    expect(status).toBe(0);
    expect(stdout).toContain("=== CareerClaw Daily Briefing ===");
  });

  it("prints Fetched jobs line", () => {
    const profilePath = makeProfileFile();
    const { stdout } = runCli(["--profile", profilePath, "--dry-run"]);
    expect(stdout).toMatch(/Fetched jobs:/);
  });

  it("prints Tracking section", () => {
    const profilePath = makeProfileFile();
    const { stdout } = runCli(["--profile", profilePath, "--dry-run"]);
    expect(stdout).toContain("Tracking:");
  });
});