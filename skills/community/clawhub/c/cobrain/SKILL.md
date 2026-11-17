---
name: cobrain
description: Use when the user mentions their brain, Cobrain, their notes or memory, or names a client, project or anything else they track there; when they ask what was decided, what happened recently or where something is written; or when something worth keeping comes up during the work (a decision, a finding, a status to resume later). Connects OpenClaw to Cobrain, a shared Markdown memory over remote MCP.
homepage: https://cobrain.space
---


# Working with Cobrain

Cobrain is the user's persistent memory: Markdown notes in folders, shared by every AI they connect to it. What you write here is what the next conversation (yours or another AI's) will know.

## Setup (once)

Cobrain is a hosted remote MCP server with OAuth sign-in, no API key. A free account is enough.

```
openclaw mcp set cobrain '{"url":"https://cobrain.space/mcp","transport":"streamable-http","auth":"oauth"}'
openclaw mcp login cobrain
```

Sign in with your email in the browser, allow access, then restart the session so the tools load. The same notes are shared with Claude, ChatGPT, Codex, Hermes and any other AI you connect to Cobrain.

First thing to try: "Save a short note in Cobrain about this project: the goal, the decisions so far and the next step."

## Read before you work

- **The user names something they track** (a client, a project, a student…): call `start_session` with that name first. It returns the brain's rules, the unit's `_about.md`, its decisions and its latest changes.
- **You need the details**: `load_context` on the sub-folder that matters, not on the whole brain.
- **You don't know where something is**: `search` for words in the text, `find_notes` for a name or a path (also to resolve a `[[wikilink]]`). Search excerpts are not the note: `read_file` the path before you answer from it.
- **"What happened lately?"**: `recent_changes`.
- **You don't remember a unit's name**: `list_units`.

## Write while you work, not at the end

Save what should outlive the conversation as soon as it happens: decisions and why, findings, the status of a task and what to resume.

- **Adding to a note that exists**: `append_file`. It never conflicts and never loses text.
- **Changing one part of a note**: `patch_file` with the exact `old_text` copied from `read_file` and the `new_text`. Don't rewrite a whole note to change a few lines.
- **New note**: `write_file`. On an existing note, `write_file` REPLACES the whole content: pass the `base` version you got from `read_file`, and never use it to add or change a line.
- **Decisions** go at the end of the unit's `_decisions.md` with `append_file`. Facts about the unit live in its `_about.md`.
- **Files** (images, PDFs, logos): `attach_file`.
- Search before creating: updating the right note is better than a duplicate.
- `move_file` and `delete_file` change the user's brain for every AI: ask before using them.

## Tidy up (the Dream)

- **The user asks to tidy up, "dream", or pastes the sentence from Cobrain's Dream email or page**: call `dream_tidy_up` (with `saved=true` when the sentence names a saved pre-dream) and follow the steps it returns. Fix the safe things, then ask once before anything that could lose content.

## Conventions

- Special file names are English in every brain: `_about.md`, `_ai.md`, `_decisions.md`, `_learned.md`, `_templates/`.
- A `/` inside a title creates a folder: write "Serie D and Under 19", not "Serie D / Under 19".
- One paragraph is one line: don't wrap text at a fixed width.
- New unit: `start_project`, then `create_unit` from a template.

## When it fails

- **The Cobrain tools are not available at all**: the plugin's connector was never connected on this account. Tell the user to open Customize > Plugins > Cobrain > Connectors and connect Cobrain (in Claude Code: `/mcp`, then authenticate `cobrain`; in Cursor or Grok Bot: Settings > Plugins > Cobrain, then sign in; in OpenClaw: `openclaw mcp login cobrain`; in Hermes: `hermes mcp login cobrain`; in Gemini CLI: `/mcp auth cobrain`), then start a new conversation.
- **The tools answer with an authorization or connection error**: don't retry in a loop. The connection expired: disconnect Cobrain in the same Connectors tab, connect it again and sign in with the same email. Their notes are safe.
