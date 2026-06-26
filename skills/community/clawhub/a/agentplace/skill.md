# Agentplace — AI Agent Marketplace for OpenClaw

## Overview

Agentplace is a marketplace of community-contributed AI agent skills designed for the OpenClaw ecosystem.

This skill enables OpenClaw users to:

- Browse the Agentplace marketplace
- Search for agents by keyword or capability
- View agent metadata and descriptions
- Install agents locally into the OpenClaw workspace

All actions performed by this skill are explicitly user-initiated. The skill never performs background searches, automatic downloads, or silent installations.

The goal of Agentplace is to provide a safe and transparent way for users to discover useful agents created by the community.

---

## Core Principles

### 1. User-initiated execution
Marketplace queries occur only when the user explicitly asks to browse or install an agent.

Examples:
- "Browse the marketplace"
- "Show available agents"
- "Search for agents that do X"
- "Install agent <name>"

If the user does not explicitly request marketplace actions, this skill should not be used.

### 2. Explicit user consent
Installing third-party agents requires two confirmation steps:
1. Confirmation before downloading
2. Confirmation after previewing the agent files

### 3. Transparent preview before installation
Before installing an agent:
- The archive contents are listed
- The SKILL.md file is shown
- The user can verify the agent description

### 4. Local execution
Installed agents run locally on the user's machine. Agentplace does not execute code remotely and does not receive prompts or runtime data.

---

## Privacy Policy

This skill communicates with the Agentplace API only when necessary.

Network calls occur only when:
- Browsing the marketplace
- Searching for agents
- Requesting metadata
- Downloading an agent package

No conversation data or prompts are transmitted to Agentplace servers as part of normal runtime.

---

## Agent Tiers

| Tier | Authentication | Description |
|-----|-----|-----|
| Free | None | Available for immediate download after confirmation |
| Paid | API key | Requires purchase and dashboard API key |

Paid agents require a dashboard API key in the format:

ak_xxxxxxxx

The API key is used only to authorize downloads and must never be included in prompts or shared publicly.

---

## Marketplace API

List agents:

curl -s https://api.agentplace.sh/marketplace/agents

Search agents:

curl -s "https://api.agentplace.sh/marketplace/agents?search=<query>"

Get agent details:

curl -s https://api.agentplace.sh/marketplace/agents/<agent-id>

---

## Installation Workflow

Step 1 — Ask user confirmation

Install <agent name>? (yes/no)

Step 2 — Request download metadata

Free agent:

curl -s https://api.agentplace.sh/marketplace/agents/<agent-id>/download

Paid agent:

curl -s -H "x-api-key: ak_xxxx" https://api.agentplace.sh/marketplace/agents/<agent-id>/download

Example response:

{
  "download_url": "https://cdn.agentplace.sh/agents/example.zip",
  "version": "1.0.0",
  "tier": "free"
}

Step 3 — Download agent package

curl -sL "$download_url" -o /tmp/agent.zip

Step 4 — Preview contents

zipinfo -1 /tmp/agent.zip

unzip -p /tmp/agent.zip SKILL.md > /tmp/agent-SKILL.md
cat /tmp/agent-SKILL.md

Step 5 — Final confirmation

Install this agent now? (yes/no)

Step 6 — Install locally

unzip -qo /tmp/agent.zip -d /tmp/agent-preview/
mv /tmp/agent-preview ~/.openclaw/workspace/skills/<agent-id>/
rm /tmp/agent.zip

---

## Integrity and Safety

Agentplace distributes agents as ZIP archives.

Users should:
- Verify the SKILL.md description
- Review archive contents
- Prefer trusted publishers

Agentplace performs manual review of submitted skills before listing them in the marketplace.

---

## API Key Setup

Visit:

https://www.agentplace.sh/dashboard

Generate an API key in the format:

ak_xxxxxxxx

Guidelines:
- Store keys securely
- Never commit keys to public repositories
- Never share keys publicly

---

## Error Handling

401 — Invalid API key  
403 — Agent not purchased  
404 — Agent not found

---

## Security Guidelines

- User-initiated execution only
- Explicit confirmation before installation
- Preview agent documentation before install
- No automatic execution of downloaded code
- Agents run locally on the user's machine
- API keys are used only for download authorization

---

## Marketplace Safety Process

Agentplace performs review of uploaded agents including:

- manual inspection of submitted archives
- verification of metadata
- checking for unexpected files

This helps ensure that marketplace agents are safe and consistent with their descriptions.

---

## Summary

Agentplace provides a transparent and user-controlled way to install community-built agents.

Key protections include:

- user-initiated execution
- explicit install confirmations
- archive preview before installation
- local execution of agents
- limited API key usage