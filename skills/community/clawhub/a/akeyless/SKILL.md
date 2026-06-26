---
name: akeyless
description: Akeyless Secrets Management via the official akeyless CLI — install, configure profiles, gateway routing, and safe read/list operations. Use when the user mentions Akeyless, akeyless CLI, vault, static/dynamic secrets, list-items, profiles, AKEYLESS_GATEWAY_URL, or fetching secrets without putting credentials in chat.
homepage: https://docs.akeyless.io/docs/cli
metadata:
  {
    "openclaw":
      {
        "emoji": "🔑",
        "requires": { "bins": ["akeyless"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "akeylesslabs/tap/akeyless",
              "bins": ["akeyless"],
              "label": "Install Akeyless CLI (brew tap)",
            },
          ],
      },
  }
---

# Akeyless CLI

Teach the agent to use the **official** [Akeyless CLI](https://docs.akeyless.io/docs/cli) on the **same machine as the OpenClaw gateway**. Do not invent URLs, regions, or auth flows—defer to docs and `akeyless <cmd> -h`.

## References

Load when details are needed:

- `references/cli-notes.md` — install (macOS/Linux), profiles, gateway env, `list-items`, precedence, safety

## Prerequisites

1. **`akeyless`** on PATH (`akeyless --version`).
2. A **configured profile** (`akeyless configure` or `~/.akeyless/profiles/`). Auth is **not** done through chat—user runs configure locally.
3. For **private gateways**: `AKEYLESS_GATEWAY_URL` (and TLS trust PEM if required)—see references.

## Workflow

1. Confirm CLI: `akeyless --version` / `which akeyless`.
2. If commands fail with auth errors: user must fix **profile** or **gateway URL** outside the agent; suggest `akeyless configure` or env vars from references—**never** ask them to paste Access Keys into chat.
3. Prefer **read-only** checks first: `akeyless list-items --minimal-view` or `akeyless list-items --path '<folder>' --minimal-view` (paths are org-specific).
4. For JSON: `akeyless list-items --json` — **summarize**; do not dump large payloads or possible secret fields into chat.
5. **Region / tenant**: do not assume only `vault.akeyless.io`; follow account and org docs.

## OpenClaw-specific

- Skills live under the agent workspace, e.g. `~/.openclaw/workspace/skills/akeyless/`. User enables **akeyless** in **Skills** and restarts the **gateway** after changes.
- Shell commands run as the **gateway host user**; that user must have working `akeyless` credentials.

## Guardrails

- **Never** paste or request Access Keys, API keys, or secret **values** in chat, logs, or repos.
- Least-privilege: only commands the user’s **role** allows; if access denied, point to Akeyless **role** and **folder path**, not “retry with more secret text.”
- Do not commit `~/.akeyless/` or paste profile TOML into threads.

## Contrast with 1Password (`op`)

Akeyless uses **`akeyless`** + **profiles** + optional **`AKEYLESS_GATEWAY_URL`**. There is no 1Password-style desktop app unlock in this workflow.
