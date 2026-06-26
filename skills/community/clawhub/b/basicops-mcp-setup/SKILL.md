---
name: basicops-mcp-setup
description: Install, configure, authenticate, or verify a BasicOps MCP connection in an MCP-capable environment. Use when the user wants to add BasicOps MCP, when a BasicOps operator skill reports that BasicOps MCP is missing or unauthorized, or when the user asks to connect BasicOps to OpenClaw, Codex, Claude, Cursor, or another MCP client. Prefer MCP-native configuration over raw API setup, verify the connection after configuration, and hand off to the BasicOps operator skill once the MCP surface is ready.
---

# BasicOps MCP Setup

Connect BasicOps to OpenClaw and other MCP-capable agent environments.

This skill is the setup half of the BasicOps MCP pair. It focuses on connection, authentication, verification, and clean handoff to `basicops-mcp-operator` once the MCP surface is ready.

## Best for

- first-time BasicOps MCP setup
- fixing missing or unauthorized BasicOps MCP connections
- verifying that BasicOps tools are actually visible before real work starts

## Pairs with

- `basicops-mcp-operator` for day-to-day task, project, note, and review work after setup

## Overview

Use this skill to help an agent get BasicOps MCP working in the current environment.

Its job is to make the BasicOps MCP connection exist, authenticate cleanly, and prove it works. Once the MCP surface is ready, stop doing setup work and hand off to the operator skill for real BasicOps actions.

Assume the preferred BasicOps MCP pattern is an MCP server reachable at `https://app.basicops.com/mcp` using a BasicOps API key in bearer-token form, typically over streamable HTTP transport. Do not assume an OAuth flow unless the environment explicitly requires one.

## Main workflow

1. Detect whether BasicOps MCP is already present.
2. If present, verify that it is authenticated and exposes usable BasicOps tools.
3. If missing, configure the BasicOps MCP server in the current MCP-capable client.
4. If authentication is missing, request or place the BasicOps API key, typically sent as a bearer token, in the right config location.
5. Verify the connection by checking that BasicOps tools are visible and usable.
6. Hand off to `basicops-mcp-operator` or continue with the user’s original BasicOps task.

## Core rules

- Prefer configuring a real MCP connection over inventing raw REST workarounds.
- Use the client’s native MCP configuration flow when available.
- If the environment already has an MCP management tool or helper, prefer that instead of manual config edits.
- Keep secrets out of chat replies when possible.
- When possible, offer a safer path like environment variables, secret storage, or direct config placement before asking the user to paste an API key into chat.
- Do not print or echo bearer tokens back to the user unless they explicitly ask and the environment requires it.
- If the user already pasted a live API key into chat, acknowledge the exposure risk briefly and recommend rotating it after setup if appropriate.
- Verify after setup. A config change without a successful visibility check is incomplete.
- If a restart or reload is required, say so clearly.

## What success looks like

A successful setup means:

- the BasicOps MCP server is registered in the current environment
- authentication is in place
- BasicOps tools are visible
- at least one low-risk verification step succeeds
- the environment is ready for `basicops-mcp-operator`

## Example requests

- "Set up BasicOps MCP here."
- "Connect BasicOps to OpenClaw."
- "Add BasicOps MCP to this agent environment."
- "BasicOps MCP is missing, can you configure it?"
- "Help me authenticate the BasicOps MCP server."
- "Verify whether this environment can talk to BasicOps through MCP."

## Read these references only when needed

- Read `references/setup-flow.md` for the main end-to-end setup sequence.
- Read `references/client-patterns.md` when you need to fit the BasicOps MCP connection into a specific MCP client or config style.
- Read `references/verification.md` when checking whether the connection is working, authenticated, and visible to the agent.
- Read `references/troubleshooting.md` when the server is missing, unauthorized, or present but not exposing usable BasicOps tools.

## Boundaries

This skill is for setup, connection, and verification.

Do not turn it into:
- a general BasicOps operator skill
- a raw REST API fallback skill
- a webhook deployment framework
- a broad infrastructure skill unrelated to BasicOps MCP

Keep the promise narrow: get BasicOps MCP connected, authenticated, verified, and ready.
