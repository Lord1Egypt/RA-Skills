---
name: bdjobs-job-apply
description: BDJobs job search, matching, applying, undoing, and salary-update automation for OpenClaw. Use when the user wants to set up BDJobs credentials/preferences, search fresh non-applied jobs, inspect job details, auto-apply to matched jobs, cancel an application, or update expected salary.
---

# BDJobs Job Apply

Use this skill to help a user manage BDJobs job searching and applying without needing to know APIs or code.

## What this skill does

- Save resume text/LaTeX into `data/resume.md`
- Save credentials and preferences into `data/userDetails.json`
- Log in and save auth data into `data/loggedInData.json`
- Refresh applied jobs into `data/appliedJobIds.json`
- Keep a not-liked list in `data/notLikedJobIds.json`
- Search jobs and return raw job details for AI matching
- Auto-apply to matched jobs when asked
- Undo/cancel an applied job when asked
- Update expected salary for an already applied job

## Onboarding flow

When the user first sets up this skill, ask for these values in plain language:

1. BDJobs username
2. BDJobs password
3. Resume text or LaTeX
4. `everyDayApplyCount` (default: 2)
5. `everyDayCronTime` (default: `12:00 PM`)
6. `isFresher` (yes/no)
7. `Experience` in years
8. Preferred `jobLocation` (optional, leave blank for all)

Save them in:
- `data/userDetails.json`
- `data/resume.md`

If the user has extra search filters or matching rules, store them in `data/preferences.json`.

## Login flow

Before search/apply work, always ensure `data/loggedInData.json` exists.

If missing:
1. run `ChecKUsername`
2. take `guidId`
3. run `Login`
4. save `token`, `refreshToken`, `encryptId`, `decodeId`, and `guidId` to `data/loggedInData.json`

If login returns 401 at any point:
1. run `ChecKUsername` again
2. run `Login` again
3. overwrite `data/loggedInData.json`

## Search flow

When the user asks for fresh jobs:

1. Clear `data/suggestedJobs.json`
2. Run `scripts/bdjobs-refresh-applied.js` to update `data/appliedJobIds.json` from `GetApplyPositionInfoV1`
3. Run `scripts/bdjobs-fetch-jobs.js` with `--keyword`, `--isFresher`, `--postedWithin`, `--pg`, and `--jobLocation` to fetch raw job lists from `GetJobSearch`
4. Run `scripts/bdjobs-filter-jobs.js` to exclude already-applied and not-liked job IDs before `Job-Details`
5. For selected job IDs, run `scripts/bdjobs-job-details.js` to fetch full job details
6. Let AI compare the raw job details with `data/resume.md` and `data/preferences.json`
7. Run `scripts/bdjobs-rank-jobs.js` to save the top 5 matched jobs into `data/suggestedJobs.json`
8. Show the contents of `data/suggestedJobs.json` to the user

Recommended match threshold:
- show apply suggestions only if match is above 40%
- if the user asks for a looser list, show 30%+

AI matching details:
- Compare the raw job details with `data/resume.md` and `data/preferences.json`
- Judge fit from skills, education, age, experience, responsibilities, location, and preferences
- Output a suggested job list with match percentages

## Auto-apply flow

When the user asks to auto-apply:

1. Ensure login exists
2. Refresh applied jobs first
3. Search fresh jobs
4. Let AI score the raw job details against the resume and preferences
5. For each approved job:
   - call `JobApply`
   - read `MinimumSalary`
   - use it as `expectedSalary` in `JobApplyPost`
   - call `JobApplyPost`
   - if successful, always show `matchingScore`
   - if successful, add the job ID to `data/appliedJobIds.json`
   - save result in `data/lastApplyResult.json`
6. Send Telegram notification only after success

## Undo/cancel flow

When the user asks to undo an application:

1. Ensure login exists
2. Call `UndoJobApply` with job ID and `FormValue`
3. If successful, remove the job ID from `data/appliedJobIds.json`
4. Save result in `data/lastUndoResult.json`

## Expected salary update flow

When the user asks to update salary for an applied job:

1. Ensure login exists
2. Call `UpdateExpectedSalary`
3. Save result in `data/lastSalaryUpdateResult.json`

## Files used by this skill

Important files live inside this skill folder:
- `data/resume.md`
- `data/userDetails.json`
- `data/loggedInData.json`
- `data/appliedJobIds.json`
- `data/notLikedJobIds.json`
- `data/preferences.json`
- `data/suggestedJobs.json`
- `data/lastApplyResult.json`
- `data/lastUndoResult.json`
- `data/lastSalaryUpdateResult.json`

## Script entry points

Run scripts from the skill folder, not the workspace root:
- `scripts/init-job-profile.js`
- `scripts/bdjobs-login.js`
- `scripts/bdjobs-refresh-applied.js`
- `scripts/bdjobs-fetch-jobs.js`

`bdjobs-fetch-jobs.js` accepts:
- `--keyword=...`
- `--isFresher=true|false`
- `--postedWithin=...` (optional day count, any number)
- `--pg=...`
- `--jobLocation=...`
- `scripts/bdjobs-filter-jobs.js`
- `scripts/bdjobs-job-details.js` accepts `--jobId=...` or a positional job id
- `scripts/bdjobs-rank-jobs.js`
- `scripts/bdjobs-apply.js`
- `scripts/bdjobs-undo.js`
- `scripts/bdjobs-update-salary.js`

## Matching rules

Use the resume and these signals:
- Job title
- Company name
- Job description
- Education requirements
- Age requirement
- Experience requirement
- Additional job requirements
- Suggested skills
- Job location
- Job nature
- User preferences from `data/preferences.json`

## Helpful behavior

When presenting jobs to the user:
- keep language simple
- explain only what matters
- include the direct job link
- mention whether it looks worth applying

When the user wants automation, do the work directly with the scripts.
