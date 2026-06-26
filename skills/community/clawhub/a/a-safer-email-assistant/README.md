# AgentSkills

This directory contains AgentSkills-compatible skill folders for this repository.

Each skill folder includes:
- `SKILL.md` (required): metadata + core instructions
- optional reference docs and prompt templates
- optional scripts for repeatable workflows

Available skills:
- `email-gateway-assistant`: workflows for syncing, triage, history Q&A, and draft creation with this gateway API.

Notes:
- Skill homepage/source: https://github.com/ArktIQ-IT/ai-email-gateway
- Required env for runtime: `GATEWAY_BASE_URL`, `GATEWAY_API_KEY`, and `ACCOUNT_ID` (or `ACCOUNT_IDS` for multi-account scripts).
