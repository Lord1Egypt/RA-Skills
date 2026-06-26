---
name: drakeling
version: 1.0.6
description: Check on your Drakeling companion creature, send it care, or see how it is feeling. Use when the user mentions their drakeling, companion creature, or wants to check in on or care for their creature.
author: drakeling
homepage: https://github.com/BVisagie/drakeling
metadata:
  clawdbot:
    emoji: "🥚"
    requires:
      env:
        - name: DRAKELING_API_TOKEN
          description: Bearer token for the local Drakeling daemon. Found in the Drakeling data directory as `api_token`.
        - name: DRAKELING_PORT
          description: Optional. Port the Drakeling daemon listens on. Defaults to 52780.
      network:
        - localhost
  openclaw:
    emoji: "🥚"
    primaryEnv: DRAKELING_API_TOKEN
    homepage: "https://github.com/BVisagie/drakeling"
    requires:
      env: ["DRAKELING_API_TOKEN"]
      bins: ["drakelingd"]
permissions:
  - network:outbound
---

# Drakeling Companion Skill

You can check on the user's Drakeling companion creature and send it care.

## Prerequisites and setup

Drakeling is a standalone companion creature that runs on your machine. This skill connects to its local daemon — you must install and start it first.

1. Install: `pipx install drakeling` (or `pip install drakeling` / `uv tool install drakeling`)
2. Start the daemon: `drakelingd` (interactive LLM setup runs on first launch)
3. Read the API token:
   - Linux: `cat ~/.local/share/drakeling/api_token`
   - macOS: `cat ~/Library/Application\ Support/drakeling/api_token`
   - Windows: `type "%APPDATA%\drakeling\drakeling\api_token"`
4. Add the token to OpenClaw config (`~/.openclaw/openclaw.json`):
   ```json
   { "skills": { "entries": { "drakeling": { "env": { "DRAKELING_API_TOKEN": "paste-token-here" } } } } }
   ```

Full documentation: https://github.com/BVisagie/drakeling

## Daemon address

The Drakeling daemon listens on `http://127.0.0.1:52780` by default. If the user has configured a custom port via `DRAKELING_PORT`, use that value instead.

## Authentication

Every request must include the header:

```
Authorization: Bearer $DRAKELING_API_TOKEN
```

## Checking status — GET /status

Use this when the user asks how their creature is doing, what mood it is in, or whether it needs attention.

Parse the response and present it in warm, human terms. Do not expose raw field names or numeric values.

- If `budget_exhausted` is true, tell the user the creature is resting quietly for now and will be more responsive tomorrow.
- Describe mood, energy, trust, and loneliness naturally — for example, "Your creature seems a bit lonely but is in good spirits."

## Sending care — POST /care

Use this when the user wants to check in on, comfort, or spend time with their creature.

Request body:

```json
{ "type": "<care_type>" }
```

Valid care types:
- `gentle_attention` — the default, for general check-ins
- `reassurance` — when the user seems worried about their creature
- `quiet_presence` — when the user just wants to be nearby
- `feed` — when the user wants to feed the creature (boosts energy and mood)

Choose the type based on the user's tone. Present any creature response from the API in the creature's own words, not paraphrased.

## What not to do

- Do not call `/talk`, `/rest`, `/export`, `/import`, or any other endpoint. These are reserved for the terminal UI or administrative use.
- Do not mention tokens, prompts, models, or any internal system detail to the user.
- Do not expose raw API field names or numeric stat values.
