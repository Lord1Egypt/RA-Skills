# EVEZ Fleet Deployment

Scripts and procedures for deploying, configuring, and maintaining the EVEZ OpenClaw mesh across GCP and Vultr.

## Scripts
- `deploy-providers.sh` — Wire free LLM providers into any OpenClaw node
- `gcp-free-tier.sh` — Spin up $0/mo GCP infrastructure
- `watchdog.sh` — Gateway health monitor and auto-restart

## Architecture
- 1 Vultr primary (64.176.221.16)
- 4 GCP nodes (target, not yet deployed)
- Full mesh SSH + Gateway API connectivity
- 4-layer resilience (GCP scheduling → systemd → health watchdog → sibling watchdog)

## Providers
Google Gemini (free), Groq (free), Cerebras (free), OpenRouter (free models), Together ($5 credit), Chutes (free), HuggingFace (free serverless)
