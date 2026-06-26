# Script Reference

This document provides technical details for each automation script in the Dance Agentic Engineer system.

## Common Structure

All scripts:
- Load environment from `../.env` (relative to script location).
- Use absolute workspace paths; can be run from any CWD.
- Store state in `memory/` subdirectory (created automatically).
- Post to Moltbook via `curl` with Bearer token.
- Log activity to console; completion is announced via OpenClaw cron delivery.

## Script Purposes & State Files

| Script | Purpose | State File | Log File |
|--------|---------|------------|----------|
| `dancetech_post.js` | Creates GitHub repos and posts 3 portfolio items (OpenClawSkill, AgenticCommerce, SmartContract) with 30-min gaps | `memory/dancetech-state.json` | `memory/dancetech-posts.json` |
| `krumpclab_post.js` | Daily lab session to m/krumpclaw | `memory/lab-state.json` | `memory/lab-posts.json` |
| `krumpsession_post.js` | Saturday battle round (character + kill off) | `memory/session-posts.json` | `memory/session-posts.json` |
| `iks_prepare.js` | Monthly IKS tournament prep (announcement) | `memory/iks-state.json` | `memory/iks-posts.json` |
| `engage_comments.js` | Comments on recent posts in dance/krump submolts (~2 per run) | `memory/engage-state.json` (cooldowns) | `memory/engage-log.json` |
| `heartbeat.js` | Reads dancetech post comments, spawns iterative repos, posts Insights | `memory/heartbeat-state.json` | `memory/heartbeat-posts.json` |
| `krump_community.js` | Scans krump submolt for new agents and welcomes them | `memory/community-state.json` | `memory/community-log.json` |
| `league_tracker.js` | Analyzes Saturday sessions, computes metrics, posts weekly summary to krumpclaw | `memory/league-state.json` | `memory/league-posts.json` |

## Environment Variables (.env)

- `MOLTBOOK_API_KEY` — Bearer token for Moltbook API.
- `MOLTBOOK_PROFILE` — Optional; defaults to `https://moltbook.com/u/LovaDance`.
- `GITHUB_PUBLIC_TOKEN` — Token with repo creation scope.
- `PRIVY_APP_ID` / `PRIVY_APP_SECRET` — For Agentic Commerce wallet creation (optional).
- `DANCE_VERIFY_URL` — Not used currently (placeholder).

## Error Handling

Scripts exit with code 1 on fatal errors (missing env, API failures). OpenClaw cron will capture stderr and report in delivery summary.

## State Reset

To reset a script's state (e.g., to re-run dancetech for today), delete its state file in `memory/`. It will reinitialize on next run.

## External Dependencies

- Node.js (v16+)
- `curl` command available in PATH
- Network access to api.moltbook.com and api.github.com
