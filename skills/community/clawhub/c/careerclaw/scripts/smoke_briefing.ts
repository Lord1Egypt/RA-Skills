/**
 * scripts/smoke_briefing.ts — Live end-to-end smoke test for the full pipeline.
 *
 * Hits real network endpoints and runs the complete briefing pipeline
 * in dry-run mode (no files written). Use this to validate the full
 * stack before building the CLI.
 *
 *   npm run smoke:briefing # Uses profile 0 (Senior Software Engineer)
 *   PowerShell
 *   $env:PROFILE=1 npm run smoke:briefing # Uses profile 1 (Marketing Specialist)
 *   $env:PROFILE=2 npm run smoke:briefing # Uses profile 2 (Registered Nurse)
 *
 *   bash
 *   PROFILE=1 npm run smoke:briefing # Uses profile 1 (Marketing Specialist)
 *   PROFILE=2 npm run smoke:briefing # Uses profile 2 (Registered Nurse)
 *
 * The profile below mirrors the sample profile from the README.
 * Edit skills / summary to match your own before running.
 *
 * Exit codes:
 *   0 — pipeline completed, ≥1 match returned
 *   1 — pipeline error or 0 matches
 */

import { runBriefing } from "../src/briefing.js";
import type { UserProfile } from "../src/models.js";

const PASS = "\x1b[32m✓\x1b[0m";
const FAIL = "\x1b[31m✗\x1b[0m";
const DIM  = "\x1b[2m";
const RESET = "\x1b[0m";

// ---------------------------------------------------------------------------
// Test profiles
// ---------------------------------------------------------------------------

const PROFILES: Array<{ label: string; profile: UserProfile }> = [
	{
		label: "Senior Software Engineer",
		profile: {
			skills: ["typescript", "react", "node", "python", "aws"],
			target_roles: ["senior engineer", "staff engineer", "software engineer"],
			experience_years: 6,
			work_mode: "remote",
			resume_summary:
				"Senior software engineer with 6 years building production systems. " +
				"Strong focus on TypeScript, React, distributed systems, and reliability.",
			location: "Remote",
			salary_min: 120000,
		},
	},
	{
		label: "Marketing Specialist",
		profile: {
			skills: ["content marketing", "seo", "copywriting", "social media", "email campaigns", "analytics", "hubspot"],
			target_roles: ["marketing manager", "content strategist", "growth marketer", "digital marketing specialist"],
			experience_years: 4,
			work_mode: "remote",
			resume_summary:
				"Digital marketing specialist with 4 years driving growth through content, SEO, " +
				"and performance campaigns. Experienced with HubSpot, Google Analytics, and paid social.",
			location: "Remote",
			salary_min: 70000,
		},
	},
	{
		label: "Registered Nurse",
		profile: {
			skills: ["patient care", "clinical assessment", "medication administration", "ehr", "triage", "wound care", "telehealth"],
			target_roles: ["registered nurse", "rn", "nurse practitioner", "clinical nurse", "telehealth nurse"],
			experience_years: 5,
			work_mode: "remote",
			resume_summary:
				"Registered nurse with 5 years of acute care and telehealth experience. " +
				"Skilled in clinical assessment, EHR documentation, and remote patient monitoring.",
			location: "Remote",
			salary_min: 75000,
		},
	},
];

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function run(): Promise<void> {
	console.log("=== CareerClaw Pipeline Smoke Test (dry-run) ===\n");

	// Select profile by env var (default to first profile)
	const profileIndex = parseInt(process.env.PROFILE ?? "0", 10);
	const selected = PROFILES[profileIndex];

	if (!selected) {
		console.error(`${FAIL} Invalid PROFILE index: ${profileIndex} (available: 0-${PROFILES.length - 1})\n`);
		process.exit(1);
	}

	const PROFILE = selected.profile;
	console.log(`Profile: ${selected.label}\n`);

	const start = Date.now();

	let result;
	try {
		result = await runBriefing(PROFILE, { dryRun: true, topK: 3 });
	} catch (err) {
		console.log(`${FAIL} runBriefing() threw: ${String(err)}\n`);
		process.exit(1);
	}

	const elapsed = Date.now() - start;

	// ---- Run summary ----
	console.log("Run");
	console.log(`  ${PASS} run_id:       ${result.run.run_id}`);
	console.log(`  ${PASS} version:      ${result.run.version}`);
	console.log(`  ${PASS} dry_run:      ${result.dry_run}`);
	console.log(`  ${PASS} jobs_fetched: ${result.run.jobs_fetched}`);
	console.log(`  ${PASS} jobs_matched: ${result.run.jobs_matched}`);
	console.log();

	// ---- Timings ----
	console.log("Timings");
	console.log(`  fetch_ms:   ${result.run.timings.fetch_ms ?? "—"}`);
	console.log(`  rank_ms:    ${result.run.timings.rank_ms ?? "—"}`);
	console.log(`  draft_ms:   ${result.run.timings.draft_ms ?? "—"}`);
	console.log(`  persist_ms: ${result.run.timings.persist_ms ?? "—"}`);
	console.log(`  total_ms:   ${elapsed}`);
	console.log();

	// ---- Sources ----
	const sources = result.run.sources;
	console.log("Sources");
	for (const [src, count] of Object.entries(sources)) {
		console.log(`  ${PASS} ${src}: ${count} jobs`);
	}
	console.log();

	// ---- Tracking (dry-run — nothing written) ----
	console.log("Tracking (dry-run — no files written)");
	console.log(`  ${PASS} created:        ${result.tracking.created}`);
	console.log(`  ${PASS} already_present: ${result.tracking.already_present}`);
	console.log();

	// ---- Top matches ----
	if (result.matches.length === 0) {
		console.log(`${FAIL} No matches returned — check profile or source health\n`);
		process.exit(1);
	}

	console.log(`Top ${result.matches.length} Match${result.matches.length === 1 ? "" : "es"}`);
	for (let i = 0; i < result.matches.length; i++) {
		const m = result.matches[i]!;
		const d = result.drafts[i]!;
		console.log();
		console.log(`  ${i + 1}) ${m.job.title} @ ${m.job.company}  [${m.job.source}]`);
		console.log(`     score:    ${m.score.toFixed(4)}`);
		console.log(`     matches:  ${m.matched_keywords.slice(0, 5).join(", ") || "(none)"}`);
		console.log(`     gaps:     ${m.gap_keywords.slice(0, 5).join(", ") || "(none)"}`);
		console.log(`     location: ${m.job.location}`);
		console.log(`     url:      ${DIM}${m.job.url}${RESET}`);
		console.log();
		console.log(`     Draft subject: ${d.subject}`);
		console.log(`     Draft preview: ${d.body.split("\n").slice(0, 3).join(" ").slice(0, 120)}…`);
	}

	console.log();
	console.log(`${PASS} Pipeline healthy — ${result.matches.length} match${result.matches.length === 1 ? "" : "es"} returned in ${elapsed}ms\n`);
	process.exit(0);
}

run();
