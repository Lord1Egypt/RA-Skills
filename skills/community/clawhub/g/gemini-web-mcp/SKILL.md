---
name: gemini-web-mcp
description: "Use this skill when an agent should extend itself with Gemini Web: get a second opinion, search current web sources, understand images/files/URLs, run Deep Research, generate or edit image/video/music artifacts, or explicitly work with Gemini account data. Route by user intent instead of loading every tool. This skill is the compatibility router; prefer the focused gemini-assist skill when only assistance and understanding are needed. Do not use for repository implementation, tests, CI, packaging, or releases—use gemini-web-mcp-development instead."
license: MIT-0
compatibility: "Requires Python 3.11+ and an installed Gemini Web MCP server. The low-token server covers common chat, image, generation, and account workflows; the primary core profile is currently required for local files, URLs, and Deep Research. Live calls require Gemini Web account Cookies."
metadata:
  version: "0.2.1"
  openclaw:
    emoji: "♊️"
    homepage: https://github.com/Luckycat133/gemini-web-mcp
    requires:
      bins:
        - uvx
    primaryEnv: GEMINI_PSID
    envVars:
      - name: GEMINI_PSID
        required: false
        description: Optional __Secure-1PSID Cookie for authenticated Gemini Web calls.
      - name: GEMINI_PSIDTS
        required: false
        description: Optional matching __Secure-1PSIDTS Cookie recommended for session stability.
      - name: GEMINI_PSIDCC
        required: false
        description: Optional __Secure-1PSIDCC Cookie forwarded when configured.
      - name: GEMINI_PROXY
        required: false
        description: Optional HTTP or HTTPS proxy used by the MCP server.
      - name: GEMINI_BROWSER_COOKIE_TIMEOUT_SECONDS
        required: false
        description: Optional bounded macOS browser-credential authorization wait for Cookie discovery.
      - name: GEMINI_TOOLS
        required: false
        description: Optional primary-server tool profile such as model, core, history, or account-read.
---

# Gemini Web MCP

Use this Skill to complete the user's task with Gemini, not to tour the Gemini tool surface.

The product priority is:

```text
1. Agent assistance and multimodal understanding
2. Generated artifacts
3. Explicit Gemini account management
```

Choose one lane for the current task. Do not expose or load account-management tools merely because they exist.

## Choose the Capability Lane

| User intent | Preferred current route | What success means |
| --- | --- | --- |
| Second opinion, critique, code/design review | low-token `chat`; primary `gemini_chat` when exact controls are needed | useful Gemini result incorporated into the agent's work |
| Quick current-web lookup | `chat` or `gemini_chat` with an explicit request for current sources | answer plus observed source URLs; otherwise label it ungrounded or escalate to Research |
| Understand one image or screenshot | low-token `chat(image_path=...)`; primary `gemini_chat(image_paths=[...])` | analysis returned to the agent and used in the surrounding task |
| Understand files, URLs, or mixed evidence | primary `gemini_upload_file`, `gemini_analyze_url`, and image chat as needed | source identity preserved and conclusions synthesized |
| Deep, multi-source research | primary `gemini_deep_research(wait_for_completion=false, retain_chat=true)` | an opaque operation/chat handle is preserved immediately; a later result yields a report |
| Generate or edit images | low-token `create(type="image")` / `edit`; primary media tools when exact controls are needed | a usable image Artifact, preferably a verified local file |
| Generate video or music | low-token `create(type="video"|"music")` or primary media tools | queued/completed state plus recoverable IDs and a usable media Artifact |
| History, Notebook, Scheduled, Gem, Prompt, usage, or cleanup | low-token account facades or narrow primary profiles | only the explicitly requested account operation is performed |

Load [workflows.md](references/workflows.md) for detailed task routes.

## Default Server Choice

Use `gemini-mcp-skill-server` for the smallest current tool surface when it can complete the task.

Use the primary server only for a narrow profile:

- `GEMINI_TOOLS=model` for text/session work;
- `GEMINI_TOOLS=core` for files, URLs, media, and Deep Research;
- `GEMINI_TOOLS=history` or `history-organize` for explicit history work;
- `GEMINI_TOOLS=account-read` for explicit account inventory;
- `GEMINI_TOOLS=scheduled-admin` only for requested scheduled mutations.

Do not use `GEMINI_TOOLS=all` as a general-agent default.

The repository is migrating toward three dedicated products. `gemini-assist` is now implemented as the dedicated `gemini-mcp-assist` server (`gemini_ask`, `gemini_search`, `gemini_understand_image`, `gemini_understand`, `gemini_research`) with its own `gemini-assist` Skill; `gemini-create` and `gemini-account` are not implemented yet. This Skill remains the compatibility router until they land.

## Standard Workflow

1. Identify the user's intended outcome.
2. Choose exactly one capability lane.
3. Call the narrowest current tool that can complete it.
4. Read the structured result before trusting compatibility prose.
5. Continue the user's actual task with the result or Artifact.
6. Use manifest or diagnostics only when discovery or recovery is needed.

Do **not** call the manifest before every known workflow. Use `gemini_get_tool_manifest` or `account(action="manifest")` when:

- the expected tool is unavailable;
- a schema or profile appears different;
- the user asks what is supported;
- upstream drift is suspected.

## Information Versus Artifacts

Search and understanding normally return information to the calling agent. The agent should synthesize it and continue working rather than dumping raw Gemini output.

Generation normally returns an Artifact. The agent should pass that file or URI to the next relevant tool:

- add the image to the document, website, slide, or app;
- use the edited image instead of merely reporting its path;
- attach the video or audio to the requested project;
- read and cite the research report.

A path, URI, or success sentence alone is not completion. Load [artifacts.md](references/artifacts.md) for acceptance and handoff rules.

## Long Operations

Deep Research, video, and music are long operations. Start them asynchronously by default.

Preserve every returned `operation_id`, `upstream_operation_id`, `upstream_chat_id`, and Artifact identity. Do not start a duplicate operation merely because one MCP call timed out.

Until the shared local operation registry lands, use start-only/current typed states and retain the upstream IDs. The target contract is an opaque, restart-safe handle stored in local SQLite with no prompt, chat, Cookie, or raw-response content.

Load [operations.md](references/operations.md) before running or recovering a long operation.

## Account Workflows

Only load or use account operations when the user explicitly asks to work with Gemini account data.

Start with list/search/read actions, identify the exact object, then mutate or delete it. A remote request being accepted is not proof that the target state changed; require positive read-back before claiming success.

For browser Cookie export, obtain explicit user approval because it can create sensitive account-authentication material in a local cache. Session reset changes only MCP/Gemini conversation state; it never changes agent memory or agent instructions.

Load [tool_surface.md](references/tool_surface.md) only when detailed account, privacy, destructive, or profile information is needed.

## Recovery

Load [recovery.md](references/recovery.md) when a tool is missing, authentication fails, an entitlement is unavailable, a long operation times out, an Artifact is incomplete, or Gemini Web behavior appears to have drifted.

Do not convert an unavailable entitlement, an ungrounded answer, a queued operation, or an accepted-but-unverified mutation into a success claim.
