---
name: gemini-ops
description: Operate Gemini WebAPI MCP authentication lifecycle on Linux host. Use for Gemini MCP (`gemini-webapi-mcp` via `mcporter`) when cookies expire frequently and auth must be refreshed often. Handles on/off, auth refresh, status, and smoke test. Triggers: "Включи Gemini", "Выключи Gemini", "обнови куки Gemini", "проверь Gemini".
---

# Gemini Ops

Automate operations for **Gemini MCP** in environments where Google session cookies become invalid quickly.

Target MCP project: https://github.com/AndyShaman/gemini-webapi-mcp

This skill solves repeated manual auth refresh by automating:
- GUI stack startup,
- navigation to Gemini,
- cookie extraction from Gemini tab,
- MCP sanity checks,
- full cleanup on shutdown.

Run these commands from `/home/moltuser/clawd`.

## Requirements / dependencies

- Linux host with Chromium and CDP (`--remote-debugging-port=9222`).
- Virtual display stack: **Xvfb + openbox + x11vnc**.
- Working scripts used by this skill:
  - `/home/moltuser/clawd/scripts/notebooklm-remote-gui.sh`
  - `/home/moltuser/clawd/scripts/gemini-on.sh`
  - `/home/moltuser/clawd/scripts/gemini-off.sh`
- Gemini MCP configured in `mcporter` (`gemini-webapi-mcp`).

## One-time login

A one-time manual login in Chromium to Google/Gemini is required.
After that, this skill keeps refresh automated by reusing the same browser profile/session.

## Turn Gemini ON

Execute:

```bash
/home/moltuser/clawd/skills/gemini-ops/scripts/gemini-on.sh
```

This sequence must:
1. Start GUI/CDP stack (Xvfb + openbox + x11vnc + Chromium).
2. Navigate the **current tab** to `https://gemini.google.com/`.
3. Wait for load.
4. Extract `__Secure-1PSID` and `__Secure-1PSIDTS` from the Gemini tab via CDP `Network.getCookies`.
5. Write cookies to `~/.mcporter/mcporter.json` (`mcpServers.gemini.env`).
6. Run sanity check with `gemini.gemini_chat`.

## Turn Gemini OFF

Execute:

```bash
/home/moltuser/clawd/skills/gemini-ops/scripts/gemini-off.sh
```

Stop Chromium and related GUI processes (x11vnc/Xvfb/openbox), then clean leftovers.

## Check status

Execute:

```bash
/home/moltuser/clawd/skills/gemini-ops/scripts/gemini-status.sh
```

## Smoke test

Execute:

```bash
/home/moltuser/clawd/skills/gemini-ops/scripts/gemini-smoke.sh
```

Expected response: `smoke-ok`.

## Failure handling

If `__Secure-1PSID` / `__Secure-1PSIDTS` are missing:
1. Re-run Gemini ON once.
2. If still missing, ask user to log in at `https://gemini.google.com/` in the same Chromium profile via VNC.
3. Re-run Gemini ON and smoke test.
