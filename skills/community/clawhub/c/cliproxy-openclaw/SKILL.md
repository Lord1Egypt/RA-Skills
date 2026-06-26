---
name: cliproxy-openclaw
description: Deploy and configure CLIProxyAPI, expose its dashboard safely, connect OAuth providers like Claude Code, Gemini, Codex, Qwen, and iFlow, generate a reusable API endpoint and API key, and integrate it with OpenClaw or other OpenAI-compatible tools. Use when the user wants one API layer from subscription-based CLI or OAuth accounts, multi-account routing, or CLIProxy setup on a VPS or local machine.
metadata:
  openclaw:
    os: [linux, darwin]
---

# CLIProxy + OpenClaw

Use this skill when the user wants to:
- install or deploy CLIProxyAPI
- expose the CLIProxy dashboard or management UI
- connect OAuth-based CLI subscriptions like Claude Code, Gemini, Codex, Qwen, or iFlow
- generate a reusable API endpoint and API key
- use CLIProxy with OpenClaw or another OpenAI-compatible client

## Outcome

The job is complete only when all of these are true:
1. CLIProxyAPI is installed and running
2. the intended dashboard or management URL is reachable
3. the user has added one or more OAuth-backed providers or accounts
4. a reusable API endpoint and API key are available
5. OpenClaw or the target client is configured to use CLIProxy
6. a smoke test succeeds against a real model

## Default workflow

1. Determine the target mode:
   - local only
   - VPS or private LAN
   - public remote dashboard access

2. Inspect the environment before changing anything:
   - OS and package/runtime availability
   - whether Docker, systemd, nginx, Caddy, or another reverse proxy already exists
   - whether OpenClaw is already installed and how it is configured
   - firewall state and whether public exposure is actually desired

3. Install and start CLIProxyAPI.
   - Prefer a stable service deployment over an ad-hoc shell session.
   - Prefer systemd when available.
   - After install, verify the process is actually listening.

4. Expose access only as needed.
   - If the user wants remote access, prefer reverse proxy plus minimal port exposure.
   - Do not open management surfaces wider than necessary.
   - State clearly what URL and what ports will become reachable.

5. Guide provider onboarding.
   - Tell the user how to open the dashboard.
   - Have them add OAuth providers or accounts.
   - Confirm that models become visible and usable.

6. Capture integration details.
   - base URL
   - API key or token
   - model names
   - any special headers if the deployment requires them

7. Connect the result to OpenClaw.
   - Use the most direct compatible provider path available in OpenClaw.
   - If exact manual values are needed, provide them explicitly.

8. Run a smoke test.
   - list models if available
   - send a minimal request
   - verify the selected model returns a real response

## Read references only when needed

- For install and service layout: `references/install.md`
- For dashboard exposure, reverse proxy, or ports: `references/dashboard.md`
- For adding OAuth providers and accounts: `references/providers.md`
- For connecting CLIProxy to OpenClaw: `references/openclaw-integration.md`
- For failures like 401, 403, 404, 429, 502, model-not-found, or streaming mismatches: `references/troubleshooting.md`

## Operating rules

- Prefer fewer checkpointed steps over long blind command chains.
- Verify actual state after each major step before moving on.
- Treat API keys, OAuth tokens, session cookies, and dashboard credentials as sensitive.
- Do not assume public exposure is desired. If unclear, ask.
- The goal is not to "install the repo"; the goal is to produce one working API layer that OpenClaw or another client can really use.
- If the user wants this published on ClawHub, keep the operational guidance concise in `SKILL.md` and move detail into references.
