# Collector + Cron

## One-shot upload

```bash
cd <PROJECTS_ROOT>/agent-fleet-dashboard
REPORT_MODE=cloudflare \
REPORT_ENDPOINT=https://<worker>.workers.dev \
REPORT_TOKEN=<INGEST_TOKEN> \
AGENT_ID=<agent_id> \
npm run -w collectors/openclaw-state-collector collect
```

## Install cron (every 2 minutes)

Use `collectors/openclaw-state-collector/scripts/install-cron.sh` and set env vars inside script/system profile.

Example entry:

```cron
*/2 * * * * cd <PROJECTS_ROOT>/agent-fleet-dashboard && REPORT_MODE=cloudflare REPORT_ENDPOINT=https://<worker>.workers.dev REPORT_TOKEN=<INGEST_TOKEN> AGENT_ID=<agent_id> npm run -w collectors/openclaw-state-collector collect >> <LOG_ROOT>/collector.log 2>&1
```

## Operational notes

- Keep `AGENT_ID` stable.
- Do not run collector through LLM calls.
- Treat non-zero exit in cron as warn-level alert.
