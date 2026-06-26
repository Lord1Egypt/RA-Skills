---
name: auth-preflight-checklist
version: 1.0.0
description: "Preflight checklist for auth-dependent work: verify the active credential lane, runtime environment, scopes, and smallest safe live probe before writing, deploying, or debugging provider integrations."
author: nissan
tags:
  - auth
  - operations
  - preflight
  - security
metadata:
  openclaw:
    emoji: "🔐"
    network:
      outbound: false
---

# Auth Preflight Checklist

Use before auth-dependent docs, troubleshooting, cron jobs, deploys, API integrations, or any task where the result depends on a token, service account, OAuth session, 1Password item, gateway model route, deploy key, or approval flag.

## Rule

Do not infer auth from configuration alone. Prove the same runtime that will do the work can access the credential and complete the smallest safe live action.

## Checklist

1. Identify the active auth lane.
   - Human OAuth, Codex subscription, OpenClaw gateway, raw API key, 1Password service account, deploy key, GitHub App, or provider token.
   - Runtime: interactive shell, LaunchAgent, cron, OpenClaw gateway, subagent, CI, VPS, container, or browser session.

2. Verify secret source and runtime agree.
   - Confirm the expected vault/item/field or env var name.
   - Check presence only; never print secret values.
   - If the job runs under launchd/cron/container, verify inside that environment or with an equivalent env capture.

3. Run the smallest live probe.
   - Notion: retrieve bot/user or target database.
   - GitHub: read repo metadata or list app installation access.
   - Vercel/Coolify: read project/app metadata before deploy.
   - OpenClaw/Codex: run a tiny gateway model smoke test.
   - 1Password: read the exact item field with bounded retry.

4. Check scopes and target access.
   - Token exists is not enough.
   - Confirm the token can access the specific database, repo, branch, app, project, model route, or webhook target.

5. Fail with a useful blocker.
   - Include missing auth lane, expected secret reference, runtime, probe command, response class, and next owner/action.
   - Do not continue into writes/deploys after 401/403/missing scope unless the task explicitly asks for forensic collection only.

## Completion Evidence

Auth work is not complete until one is true:

- Preflight command passed in the same runtime lane.
- Live action succeeded and produced the expected artifact.
- Blocker is recorded with exact missing credential/scope/approval and next action.

For OpenClaw model calls in scheduled scripts, prefer gateway/Codex routing. A missing raw OPENAI_API_KEY is not a failure if the OpenClaw gateway smoke test proves the Codex-backed route works.
