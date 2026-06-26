/**
 * scripts/smoke_sources.ts — Live smoke test for job source adapters.
 *
 * Hits real network endpoints. Run MANUALLY before releases, not in CI.
 *
 *   npm run smoke
 *
 * Exit codes:
 *   0 — both sources returned ≥1 valid job
 *   1 — one or both sources failed or returned 0 jobs
 */

import { fetchRemoteOkJobs } from "../src/adapters/remoteok.js";
import { fetchHnJobs } from "../src/adapters/hackernews.js";
import { HN_WHO_IS_HIRING_ID } from "../src/config.js";

const PASS = "\x1b[32m✓\x1b[0m";
const FAIL = "\x1b[31m✗\x1b[0m";

async function run(): Promise<void> {
  console.log("=== CareerClaw Source Smoke Test ===\n");
  let allPassed = true;

  // ---- RemoteOK ----
  console.log("RemoteOK RSS …");
  try {
    const jobs = await fetchRemoteOkJobs();
    if (jobs.length === 0) {
      console.log(`  ${FAIL} Returned 0 jobs`);
      allPassed = false;
    } else {
      const first = jobs[0]!;
      console.log(`  ${PASS} Fetched ${jobs.length} jobs`);
      console.log(`  ${PASS} First job_id: ${first.job_id}`);
      console.log(`  ${PASS} First title:  "${first.title}" @ ${first.company}`);
      console.log(`  ${PASS} work_mode:    ${first.work_mode ?? "(null)"}`);
      console.log(`  ${PASS} salary_min:   ${first.salary_min ?? "(null)"}`);
    }
  } catch (err) {
    console.log(`  ${FAIL} Fetch error: ${String(err)}`);
    allPassed = false;
  }

  console.log();

  // ---- Hacker News ----
  console.log(`Hacker News "Who is Hiring?" (thread ${HN_WHO_IS_HIRING_ID}) …`);
  try {
    const jobs = await fetchHnJobs(HN_WHO_IS_HIRING_ID);
    if (jobs.length === 0) {
      console.log(`  ${FAIL} Returned 0 jobs — check HN_WHO_IS_HIRING_ID is current`);
      allPassed = false;
    } else {
      const first = jobs[0]!;
      console.log(`  ${PASS} Fetched ${jobs.length} jobs`);
      console.log(`  ${PASS} First job_id: ${first.job_id}`);
      console.log(`  ${PASS} First title:  "${first.title}" @ ${first.company}`);
      console.log(`  ${PASS} location:     "${first.location}"`);
      console.log(`  ${PASS} work_mode:    ${first.work_mode ?? "(null)"}`);
    }
  } catch (err) {
    console.log(`  ${FAIL} Fetch error: ${String(err)}`);
    allPassed = false;
  }

  console.log();

  if (allPassed) {
    console.log(`${PASS} All sources healthy\n`);
    process.exit(0);
  } else {
    console.log(`${FAIL} One or more sources failed — see above\n`);
    process.exit(1);
  }
}

run();
