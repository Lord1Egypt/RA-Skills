# Daily to Goal AI Coach

## Required environment variables

- `DATABASE_URL`: PostgreSQL connection string for the shared application database.
- `WEB_ORIGIN`: Browser origin used in onboarding links and follow-up actions.
- `SKILL_GATEWAY_BASE_URL`: Base URL that serves `/api/skill-gateway` for ClawHub callbacks.
- `CLAWHUB_INSTALLATION_SECRET`: Shared secret used to verify installation flow requests.

## First-run flow

1. Install the skill in ClawHub.
2. Start provisioning through `/api/skill-gateway/installations/start`.
3. Complete setup through `/api/skill-gateway/installations/complete` by selecting mode, timezone, and workweek.
4. Create the first goal after provisioning finishes.

## Personal vs team mode

- `personal`: Sets up one user workspace with daily digest automation enabled by default.
- `team`: Sets up a shared workspace for a lead and teammates, with weekly reporting and risk scanning available.

## Automation triggers

- `dailyDigest`: Sends a working-day summary for the current workspace.
- `weeklyReport`: Builds the end-of-week report draft for team review.
- `riskScan`: Checks for execution risks and prepares reminders for the responsible lead.
