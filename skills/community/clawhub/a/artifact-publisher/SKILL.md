---
name: artifact-publisher
description: Publish self-contained HTML to a stable share link and read page feedback via Artifact Publisher MCP. Use when the user wants a review/share URL for agent-made HTML, to update the same link, change access, pull comments, or style with built-in themes. Do not use for unrelated hosting, SPA/multi-file deploys, or package registries.
version: 0.1.0
author: Angle Labs GmbH
license: MIT-0
platforms: [macos, linux, windows]
required_environment_variables:
  - name: ARTIFACT_PUBLISHER_KEY
    optional: true
    prompt: "Publisher key for headless/always-on agents (Hermes, OpenClaw operators). Mint once at https://artifactpublisher.com/account/ — shown once; never paste into chat. Prefer OAuth browser consent when the client supports it."
metadata:
  tags: [html, publishing, sharing, share-link, mcp, feedback, review]
  hermes:
    tags: [html, publishing, sharing, mcp, feedback]
    homepage: https://artifactpublisher.com
  openclaw:
    emoji: 📎
    homepage: https://artifactpublisher.com
    primaryEnv: ARTIFACT_PUBLISHER_KEY
    requires:
      env:
        - ARTIFACT_PUBLISHER_KEY
    envVars:
      - name: ARTIFACT_PUBLISHER_KEY
        required: true
        description: Scoped publisher key (Bearer). Prefer OAuth when the client supports browser consent; for headless/always-on agents this env var is the practical path. Mint at https://artifactpublisher.com/account/ — never commit or paste into chat.
---

# Artifact Publisher

Hosted MCP server that turns one self-contained HTML document into a stable,
unlisted share link. Reviewers open it without an AI-vendor account; optional
page comments come back to the agent with `get_feedback`. MCP-first and
provider-agnostic. Free plan available.

**Server:** `artifact-publisher` · version `0.1.0`
**Endpoint:** `https://app.artifactpublisher.com/mcp` (streamable HTTP)
**Docs:** https://artifactpublisher.com/docs/mcp/

> ClawHub pack mirror of the canonical skill at
> `skills/artifact-publisher/`. **Do not publish** to ClawHub until Simon
> rewrite + Bobby go (`docs/internal/skill-clawhub-checklist.md`). No `scripts/`.

## Hard rules

1. After `publish_artifact` / `update_artifact`, report **`artifact.url`**
   (control-origin share/viewer) **first**. Use `artifact.viewer_url` when a
   version pin helps. **Never** make the raw artifact-origin URL the primary
   share link.
2. **Never** print, paste, commit, or write into artifacts: `ar_pk_…`,
   `ar_oat_…`, `ar_ort_…`, `ar_oac_…`, refresh tokens, cookies, or
   `Authorization` headers. Prefer OAuth or env `ARTIFACT_PUBLISHER_KEY`.
3. Do **not** invent HTML when a real file exists — read the file and pass its
   contents to `publish_artifact` / `update_artifact`.
4. Call `get_authoring_guide` before large styling; prefer
   `<meta name="ap-theme" content="firn">`.
5. Feedback is optional/secondary. `get_feedback` is **pull-only** — do not
   frame the product as an approval loop.
6. **Thin MCP wiring only** — no shell scripts, no curl wrappers, no reckless
   `exec`, no downloading or running arbitrary binaries.

## Route the request

| Route | When | Load |
| --- | --- | --- |
| Setup / connect | First wire, OAuth vs key, Hermes/OpenClaw/Cursor snippets | [setup](references/setup.md) |
| Tool honesty | Exact live tool names, deprecated board aliases | [tools](references/tools.md) |

## Quick loop

1. Read existing HTML if a file exists; else author self-contained HTML (inline
   assets; sandbox has no network).
2. Optional: `get_authoring_guide` + `ap-theme` firn before large CSS.
3. `publish_artifact` → report **`artifact.url` first**.
4. Later: `update_artifact` (same link), optional `get_feedback` /
   `reply_to_feedback`, `set_artifact_access`, or `revoke_artifact`.

## Live tools (summary)

`publish_artifact`, `update_artifact`, `set_artifact_access`, `get_feedback`,
`reply_to_feedback`, `list_artifacts`, `revoke_artifact`, `configure_workspace`,
`get_artifact_board`, `reset_artifact_board`, `get_artifact_state`,
`set_artifact_state`, `reset_artifact_state`, `get_authoring_guide`.

Full table: [tools](references/tools.md). Setup ladder: [setup](references/setup.md).
