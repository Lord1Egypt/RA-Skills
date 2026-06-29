# Onboarding Guide

## Fresh Installation

### Detection
On first load, check:
- Does `ORCHESTRATOR_DATA_DIR` exist or is the env var set?
- Does `models.json` exist with catalogue data?
- If neither → fresh install detected.

### Welcome
```
Welcome to Genor's Project Orchestration!

This skill helps you:
• Manage all your AI models in one inventory
• Route tasks to the right model automatically
• Log sessions, decisions, and project state
• Check cloud pricing and avoid bill surprises
• Bootstrap projects with docs, ADRs, and plans
• Track QA status per session

Let's get you set up. This takes about 5-10 minutes.
```

### Provider Discovery
Probe every provider you can reach:

| Check | What to do |
|-------|-----------|
| **OpenRouter** | Check for API key |
| **LM Studio** | `curl -s --max-time 3 http://localhost:1234/v1/models` |
| **OpenCode** | Check `opencode` CLI |
| **Cursor** | Check `cursor` CLI |
| **Local GPU** | Probe GPU, VRAM, CUDA version |
| **Other** | Ask: any other endpoints? |

For each provider found, ask about typical spend and preferred/avoided models.

### Model Cataloguing
For each discovered model, collect: id, name, provider, host, context_window, speed_rating, agent_ready, user_notes.

Use the helper script: `bash scripts/discover-models.sh`

### Routing Rules
After cataloguing, generate initial routing rules for each task type (coding, research, creative, vision, quick). Write to `orchestrator-data/MODEL_CATALOG.md`.

### Project Discovery
Check common project locations (`~/projects/`, `~/code/`, `~/src/`). For each found, ask if the user wants to onboard it.

### Price Check Cron
Ask if they want nightly price checks at 2 AM. If yes, install cron job.

### Dashboard Test
Offer to start the dashboard: `bash dashboard/serve.sh`

### Summary
After all steps, write a summary of: data directory, providers, models count, projects, price check status, dashboard port.

Log the session: `bash scripts/log-session.sh orchestrator "Fresh install onboarding" "-" complete "X models, Y providers"`

### Re-Onboarding
```
bash scripts/onboard.sh           # re-runs discovery + interview
bash scripts/onboard.sh --force   # force full re-onboarding
```
