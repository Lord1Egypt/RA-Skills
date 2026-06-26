#!/usr/bin/env node
/**
 * cli.ts — CareerClaw command-line entry point.
 *
 * Usage:
 *   npx careerclaw-js [options]
 *   node --env-file=.env dist/cli.js [options]
 *
 * Options:
 *   --profile PATH     Path to profile.json (default: ~/.careerclaw/profile.json)
 *   --resume-txt PATH  Plain-text resume file to enhance matching
 *   --top-k INT        Number of top matches to return (default: 3)
 *   --dry-run          Run without writing tracking or run log
 *   --json             Print JSON output only (machine-readable; no colour)
 *   --help             Print this help message and exit
 *
 * Exit codes:
 *   0 — briefing completed (even if 0 matches — not an error)
 *   1 — fatal error (profile not found, unreadable, or invalid JSON)
 */

import { parseArgs } from "node:util";
import { readFileSync, existsSync } from "node:fs";
import { runBriefing } from "./briefing.js";
import {
  PROFILE_PATH,
  RESUME_TXT_PATH,
  DEFAULT_TOP_K,
  PRO_KEY,
} from "./config.js";
import type { UserProfile, BriefingResult, ScoredJob, OutreachDraft } from "./models.js";
import { buildResumeIntelligence } from "./resume-intel.js";

// ---------------------------------------------------------------------------
// Arg parsing
// ---------------------------------------------------------------------------

const { values: args } = parseArgs({
  options: {
    profile:     { type: "string",  short: "p" },
    "resume-txt":{ type: "string" },
    "top-k":     { type: "string",  short: "k" },
    "dry-run":   { type: "boolean", short: "d", default: false },
    json:        { type: "boolean", short: "j", default: false },
    help:        { type: "boolean", short: "h", default: false },
  },
  strict: true,
  allowPositionals: false,
});

if (args.help) {
  printHelp();
  process.exit(0);
}

const profilePath  = args["profile"]     ?? PROFILE_PATH;
const resumeTxtPath = args["resume-txt"] ?? null;
const topK         = parseInt(args["top-k"] ?? String(DEFAULT_TOP_K), 10);
const dryRun       = args["dry-run"] as boolean;
const jsonMode     = args["json"] as boolean;

if (isNaN(topK) || topK < 1) {
  fatal(`--top-k must be a positive integer, got: ${args["top-k"]}`);
}

// ---------------------------------------------------------------------------
// Load profile
// ---------------------------------------------------------------------------

function loadProfile(path: string): UserProfile {
  if (!existsSync(path)) {
    fatal(
      `Profile not found: ${path}\n` +
      `  Create one at ${path} or pass --profile PATH.\n` +
      `  See README for the profile schema.`
    );
  }
  let raw: string;
  try {
    raw = readFileSync(path, "utf8");
  } catch (err) {
    fatal(`Could not read profile: ${path}\n  ${String(err)}`);
  }
  try {
    return JSON.parse(raw!) as UserProfile;
  } catch (err) {
    fatal(`Profile is not valid JSON: ${path}\n  ${String(err)}`);
  }
}

// ---------------------------------------------------------------------------
// Load resume (optional)
// ---------------------------------------------------------------------------

function loadResumeTxt(path: string): string | null {
  if (!existsSync(path)) {
    warn(`Resume file not found: ${path} — running without resume intelligence`);
    return null;
  }
  try {
    return readFileSync(path, "utf8");
  } catch {
    warn(`Could not read resume: ${path} — running without resume intelligence`);
    return null;
  }
}

// ---------------------------------------------------------------------------
// Console formatter — mirrors Python output format
// ---------------------------------------------------------------------------

function printBriefing(result: BriefingResult, profile: UserProfile): void {
  const { run, matches, drafts, tracking, dry_run } = result;
  const sources = Object.entries(run.sources)
    .map(([s, n]) => `${s}: ${n}`)
    .join(" | ");

  console.log(`\n=== CareerClaw Daily Briefing ===`);
  console.log(`Fetched jobs: ${run.jobs_fetched} | Sources: ${sources}`);
  console.log(`Duration: ${run.timings.fetch_ms ?? 0}ms fetch + ${run.timings.rank_ms ?? 0}ms rank`);
  if (dry_run) console.log(`(dry-run — no files written)`);
  console.log();

  // ---- Top matches ----
  if (matches.length === 0) {
    console.log(`No matches found for your profile.`);
    console.log(`Try broadening your skills list or checking source health with:`);
    console.log(`  npm run smoke\n`);
  } else {
    console.log(`Top Matches:\n`);
  }
  for (let i = 0; i < matches.length; i++) {
    const m: ScoredJob = matches[i]!;
    const fitPct = Math.round(m.breakdown.keyword * 100);
    const matchStr = m.matched_keywords.slice(0, 5).join(", ") || "(none)";
    const gapStr   = m.gap_keywords.slice(0, 5).join(", ")     || "(none)";

    console.log(`${i + 1}) ${m.job.title} @ ${m.job.company}  [${m.job.source}]`);
    console.log(`   score: ${m.score.toFixed(4)} | fit: ${fitPct}%`);
    console.log(`   matches: ${matchStr}`);
    console.log(`   gaps:    ${gapStr}`);
    console.log(`   location: ${m.job.location || "(not specified)"}`);
    console.log(`   url: ${m.job.url}`);
    console.log();
  }

  // ---- Drafts ----
  console.log(`Drafts:\n`);
  for (let i = 0; i < drafts.length; i++) {
    const d: OutreachDraft = drafts[i]!;
    console.log(`--- Draft #${i + 1} ---`);
    console.log(`Subject: ${d.subject}`);
    console.log();
    console.log(d.body);
    console.log();
  }

  // ---- Tracking summary ----
  console.log(`Tracking:`);
  console.log(`  ${tracking.created} new job(s) saved`);
  if (tracking.already_present > 0) {
    console.log(`  ${tracking.already_present} already in your tracker (last_seen_at updated)`);
  }
  console.log();
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  const profile = loadProfile(profilePath);

  // Resume text is loaded for future LLM enhancement (Phase 10).
  // It is NOT merged into profile.skills — that would inflate the token
  // corpus with generic words and collapse Jaccard scores.
  // profile.skills + profile.resume_summary already provide the correct
  // matching corpus. Resume intelligence will be wired as a weighted
  // signal layer when the LLM enhancement module ships.
  // Resume text is loaded and converted to keyword signals for LLM enhancement.
  // Raw text is NEVER forwarded to the LLM — only extracted impact_signals.
  const resumePath = resumeTxtPath ?? (existsSync(RESUME_TXT_PATH) ? RESUME_TXT_PATH : null);
  let resumeText: string | null = null;
  if (resumePath) {
    resumeText = loadResumeTxt(resumePath);
    if (resumeText && !jsonMode) {
      console.log(`Resume loaded: ${resumePath} (ready for Pro enhancement)`);
    }
  }

  const intelParams: Parameters<typeof buildResumeIntelligence>[0] = {
    resume_summary: profile.resume_summary ?? "",
    skills: profile.skills,
    target_roles: profile.target_roles,
  };
  if (resumeText) intelParams.resume_text = resumeText;
  const resumeIntel = buildResumeIntelligence(intelParams);

  const briefingOptions: Parameters<typeof runBriefing>[1] = { topK, dryRun, resumeIntel };
  if (PRO_KEY) briefingOptions.proKey = PRO_KEY;
  const result = await runBriefing(profile, briefingOptions);

  if (jsonMode) {
    process.stdout.write(JSON.stringify(result, null, 2) + "\n");
    process.exit(0);
  }

  printBriefing(result, profile);
  process.exit(0);
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function fatal(message: string): never {
  console.error(`\nError: ${message}\n`);
  process.exit(1);
}

function warn(message: string): void {
  console.warn(`Warning: ${message}`);
}

function printHelp(): void {
  console.log(`
careerclaw-js — AI-powered job search briefing

Usage:
  careerclaw-js [options]
  node --env-file=.env dist/cli.js [options]

Options:
  -p, --profile PATH     Path to profile.json
                         (default: ~/.careerclaw/profile.json)
      --resume-txt PATH  Plain-text resume to enhance keyword matching
                         (default: ~/.careerclaw/resume.txt if present)
  -k, --top-k INT        Number of top matches to return (default: 3)
  -d, --dry-run          Run without writing tracking or run log
  -j, --json             Machine-readable JSON output (no colour, no headers)
  -h, --help             Show this help message

Examples:
  # First run — dry-run to preview without writing files
  careerclaw-js --dry-run

  # With your resume for better match quality
  careerclaw-js --resume-txt ~/.careerclaw/resume.txt --dry-run

  # JSON output for agent/script consumption
  careerclaw-js --json --dry-run

  # Custom profile and top 5 results
  careerclaw-js --profile ./my-profile.json --top-k 5

Environment:
  node --env-file=.env dist/cli.js   Load credentials from .env (Node 20+)
  Copy .env.example to .env and fill in CAREERCLAW_PRO_KEY and LLM keys.
`);
}

main().catch((err: unknown) => {
  fatal(String(err));
});
