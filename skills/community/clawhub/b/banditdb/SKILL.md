---
name: banditdb
description: >
  BanditDB is an in-memory decision database for AI agents — real-time learning from outcomes.
  Use it to auto-tune notification timing, model routing, or prompt selection.
---

# BanditDB Skill

BanditDB is a self-hosted decision database. It learns which choice works best for which context
through contextual multi-armed bandits — no ML pipeline required.

## Setup

Install BanditDB from GitHub releases or run the Docker image (see `references/api.md` for details).
Default port: 8080. Verify by requesting `GET /campaigns`.

## Core Workflow

Three-step loop — create once, then predict and reward repeatedly:

1. **Create a campaign** — define a campaign ID, the arms (choices), and context feature dimension.
2. **Get a prediction** — pass a context vector, receive the recommended arm and an interaction ID.
3. **Record a reward** — report the outcome (0.0–1.0) for the interaction ID.

For full API details, request/response examples, and MCP tool registration, see `references/api.md`.

## Designing Context Vectors

The context vector is the most important design decision. Each float encodes something about the
current situation. Normalize values to roughly 0–1 range.

Examples:
- **Notification timing**: `[hour_of_day/24, day_of_week/7, messages_today/10, last_response_delay_mins/60]`
- **Tool selection**: `[query_length/500, has_code_mention, has_url, specificity_score]`
- **Prompt strategy**: `[task_complexity, domain_familiarity, output_length_needed, structured_output]`

## Use Cases for OpenClaw Agents

- **Smart notifications** — learn when/how to reach the user (arms: morning/afternoon/evening, channel variants)
- **Tool routing** — which tool to use for a query type (arms: web_search/memory/file_lookup/ask)
- **Model selection** — which model for which task (arms: opus/sonnet/haiku)
- **Response style** — learn user preferences (arms: brief/detailed/bullet_points)
- **Heartbeat frequency** — when to check in vs stay quiet

## Key Details

- Algorithms: LinUCB (default, supports causal analysis) or Thompson Sampling
- Cold start: meaningful lift typically after 300–1500 interactions depending on noise
- Parquet export available for offline causal analysis (LinUCB only)
- WAL ensures crash recovery — no data loss on restart
- ~10K predictions/s on a single node
