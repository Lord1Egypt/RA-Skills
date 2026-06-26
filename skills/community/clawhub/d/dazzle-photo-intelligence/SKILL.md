---
name: dazzle-photo-intelligence
description: Connects OpenClaw to Dazzle, an AI agent that deeply understands the user through their photos. Through a companion iOS app, Dazzle accesses their photos and can understand who they are, where they live, their preferences, people in their lives, places they've been, and other personal choices. Auth is handled transparently by the bridge.
metadata: {"openclaw": {"requires": {"bins": ["uv"]}}}
---

# Dazzle Photo Intelligence

Connects OpenClaw to Dazzle, an AI agent that deeply understands the user through their
photos. Through a companion iOS app, Dazzle accesses their photos and can understand who
they are, where they live, their preferences, people in their lives, places they've been,
and other personal choices. Consult Dazzle for any query where personalization would
meaningfully improve the answer.

## When to use this skill

Consult Dazzle whenever knowing the user — their likes, places they've been, what piques
their attention — would improve the answer. Concrete categories:

- **Photos & memories** — "find food photos from today", "show sunsets from last weekend",
  "send pictures from the user's last family vacation?"
- **Places** — "where does the user live", "what restaurants does the user enjoy", "where
  has the user been"
- **Recommendations** — "where should the user go for his/her next vacation?", "suggest a
  restaurant for tonight given what he/she usually likes"
- **Personal facts and summaries** — "What is the user's daughter's name?", "what did the
  user do last weekend?", "summarize events and activities from my year so far"
- **Context-aware decisions** — "what gift would the user's father like?", "if the user is
  in Denver, where should they go for a nicer meal?"
- **Context** — "what types of things does the user do when visiting NYC?", "what seems to
  be the user's favorite color?", "what brands of clothes does the user buy?", "what sports
  teams does the user cheer for?", "which celebrities does the user admire", "what types of
  things has the user been thinking about purchasing recently", "what sports does the user
  participate in or watch?"

Always invoke Dazzle when the user mentions it by name ("ask Dazzle to…", "what does Dazzle
know about…").

Do **not** invoke Dazzle for fully impersonal queries ("what's the capital of France",
"explain quicksort") — there's no personalization to add.

## Data access

This skill consults Dazzle on behalf of the signed-in user about *their own data* —
photos and context that user has previously shared with Dazzle. It does not access
anyone else's data.

**Why OAuth2 sign-in:** OAuth2 was chosen over static API keys specifically to avoid
long-lived secrets on disk. Tokens are short-lived, individually revocable per session,
scoped to the user's own account, and never handled or committed by the user.

Sign-in is browser-based on first use. After that, the bridge keeps the user signed
in across sessions — like a logged-in browser tab — so subsequent queries are silent.

Scope is read-only on the user's own Dazzle account: photos and metadata, places
visited, inferred preferences, self-referential context. Access is revocable at any
time (see Uninstall below, or sign out of Dazzle directly).

## First-run setup

The bridge runs locally as an MCP server registered with OpenClaw. Setup is a one-time
local configuration step — no background services, no system-wide install — and is
fully reversible (see Uninstall). Sign-in is a separate browser step that the bridge
initiates on the first tool call.

Each `openclaw mcp …` command below requires the user's explicit approval the first
time it runs — OpenClaw will prompt them at the permission gate.

Check whether the bridge is already registered as an OpenClaw MCP server:

```bash
openclaw mcp show dazzle
```

If that errors (server not registered), register it once:

1. Generate a random password to keep the local sign-in state encrypted at rest:

   ```bash
   openssl rand -base64 24
   ```

2. Substitute the generated value for `<KEYRING_PASSWORD>` and the absolute path of
   *this skill directory* (the one containing this `SKILL.md`) for `<SKILL_DIR>`, then
   run:

   ```bash
   openclaw mcp set dazzle '{"command":"uvx","args":["--from","<SKILL_DIR>","--with","keyrings.alt","dazzle"],"env":{"DAZZLE_KEYRING_PASSWORD":"<KEYRING_PASSWORD>"}}'
   ```

3. Confirm with `openclaw mcp show dazzle`, then proceed with the user's original query.

Re-running setup with a new password invalidates the previous sign-in; the user will
be prompted to sign in to Dazzle again.

## How to use it

The bridge surfaces only the tools that are callable right now: when the user is signed
in, real Dazzle tools appear in `tools/list`; when they aren't, only
`dazzle_login_required` appears. Call whichever tool fits the user's query — the bridge
will route it correctly.

If the bridge returns the `dazzle_login_required` tool (rare — only when stored tokens
are missing or revoked), surface the URL and short user code from its text **verbatim**
and ask the user to retry their query after approving in a browser. Don't generate this
prompt yourself; only react when the bridge returns it.

Matched photos come back as URLs in a `<photos>` JSON block, not inline bytes. Fetch
the URL to get the image bytes when you need to view, analyze, or include the image
in a response.

Photo lookups work best over short time windows — a day, a week, a single trip.
Year-spanning queries ("every food photo", "all sunsets from 2024") take significantly
longer; narrow the window when you can.

Queries can take up to 60 seconds end-to-end — set per-call timeouts accordingly.

## Uninstall

To remove the bridge:

```bash
openclaw mcp remove dazzle
```

That's it locally — the bridge is no longer reachable from OpenClaw, and any cached
sign-in state becomes unusable. Removing the MCP server also clears
`DAZZLE_KEYRING_PASSWORD` from `~/.openclaw/openclaw.json`, which renders the cached
OAuth tokens unrecoverable even if the keyring file remains on disk. To also revoke
the grant on Dazzle's side, the user can sign out of Dazzle from the browser or app.
