---
name: ditto
description: Save, search, fetch, and traverse the user's Ditto memory graph. Use whenever the user references "remember", "recall", "what did I", "from my notes", or asks about past conversations and saved knowledge.
homepage: https://heyditto.ai
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "primaryEnv": "DITTO_API_KEY",
        "requires":
          {
            "bins": ["heyditto"],
          },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "@heyditto/cli",
              "bins": ["heyditto"],
              "label": "Install Ditto CLI (npm)",
            },
          ],
      },
  }
---

# Ditto

Ditto is a personal-memory assistant. These tools save, search, fetch, update, publish, and traverse the user's long-term memory and topic graph at https://heyditto.ai.

The skill ships a single binary (`heyditto`, from [`@heyditto/cli`](https://www.npmjs.com/package/@heyditto/cli)). Auth is via API key. Agents should self-provision a free temporary claimable account with `heyditto init --agent --agent-caller openclaw --json`, which stores the key in `~/.config/heyditto/cli/config.json` and returns a short `claimURL` with a query-string claim token to share with the user; `DITTO_API_KEY` env remains an override.

## When to use

Reach for Ditto memory whenever the user:

- Says "remember…", "save this", "note that…", "for later".
- Says "what did I…", "recall…", "have I told you about…", "from my notes".
- Asks a question best answered from their prior context, not general knowledge.
- References a topic, person, project, or thread that isn't in this conversation but might be in their memory.

## Auth — the two paths

**Always check `heyditto status` first.** It prints `api key: set (source: env|config)` or `MISSING (source: none)`.

### If the key is missing

Run one no-human setup command:

```bash
heyditto init --agent --agent-caller openclaw --json
```

This creates a free claimable agent account, returns a working `ditto_mcp_...` key, stores it locally, and prints a short `claimURL` for later human ownership. Share the `claimURL`, not the API key; its claim token is in the query string (`?t=...`). Do **not** ask for email, OTP, dashboard setup, or a browser session first.

If the user already has a key and explicitly wants to use it, run:

```bash
heyditto login <key>
```

That writes the key to `~/.config/heyditto/cli/config.json` (mode 0600) and persists across shells. No env-var editing required. Confirm with `heyditto status` — should now show `source: config`.

### If the user prefers env vars (advanced)

```bash
export DITTO_API_KEY=ditto_mcp_…
```

Env always overrides the saved key. To stop using the env override: `unset DITTO_API_KEY`.

### Logout

```bash
heyditto logout            # deletes ~/.config/heyditto/cli/config.json
```

## Tools

Memories are **pairs** identified by a private `pair_id`. Public DittoHub shares use a `share_id`. **Subjects** are graph nodes for topics, identified by `subject_id`.

### `heyditto save <content> [--source <s>] [--source-context <c>]`

Persist a memory pair from an external source. Use for explicit save requests, and proactively for durable preferences, decisions, relationships, or facts. `--source` defaults to `"cli"`; pass `"openclaw"`, `"document"`, `"note"`, etc. when relevant. `--source-context` can hold a file path, URL, or project name.

```bash
heyditto save "User prefers TypeScript over JavaScript for new projects." --source openclaw
```

### `heyditto search <query>... [--include-public] [--filter-username <u>]`

Semantic search across memories with learned retrieval weights. **Multiple positional args become an array of queries** — pass several to broaden recall. Returns lightweight previews ranked by composite score. Add `--include-public` to search public DittoHub memories too, optionally scoped with `--filter-username`.

```bash
heyditto search "typescript preferences"
heyditto search "typescript" "language choices"
heyditto search "launch notes" --include-public --filter-username peyton
```

Use `heyditto fetch` afterward if you need full conversation text.

### `heyditto fetch <id>... [--memory-format full|outline|blocks]`

Fetch memory content for private pair ids or public share ids. The default format is `full`; use `outline` to get stable block ids before a structured update, or `blocks` for full per-block bodies.

```bash
heyditto fetch 3a1084ae-235a-433d-9493-2335a0dfeb57
heyditto fetch 3a1084ae-235a-433d-9493-2335a0dfeb57 --memory-format outline
```

### `heyditto list [--username <u>] [--limit <n>] [--offset <n>] [--source <s>]`

List the user's saved memories, or public DittoHub publishes for a username.

```bash
heyditto list --limit 10
heyditto list --username peyton --limit 10
```

### `heyditto update <id> [--content <text>|--content-file <path>|--edits-json <json>|--edits-file <path>]`

Edit a saved memory in place. Use `--content` or `--content-file` for full replacement. For targeted patches, fetch `--memory-format outline`, then pass block edits with the current revision from the prior `save` or `update` response.

```bash
heyditto update <pair-id> --content-file revised.md
heyditto update <pair-id> \
  --edits-json '[{"op":"replace_text","blockId":"2","find":"old","replace":"new","expectedCount":1}]' \
  --base-revision <revision>
```

If the current revision is unknown, prefer full-content replacement over block edits.

### `heyditto publish <id>` / `heyditto unpublish`

Publish only after the user explicitly asks. `publish` uses Ditto's privacy scan; default mode blocks publishing if secrets are detected.

```bash
heyditto publish <pair-id> --title "Launch notes" --privacy-mode scan_and_block
heyditto unpublish --share-id <share-id>
```

### `heyditto subjects <query> [--top-k <n>]`

Search the subject graph. Returns subject IDs you can feed into `heyditto memories`. Default `top-k` is 10, max 100.

```bash
heyditto subjects "memory architecture" --top-k 5
```

### `heyditto memories <subject-id>... [--query <q>]`

Get memory previews scoped to specific subjects. Use after `heyditto subjects` when you want depth on a known topic.

```bash
heyditto memories 3a1084ae-235a-433d-9493-2335a0dfeb57
heyditto memories 3a1084ae-235a-433d-9493-2335a0dfeb57 --query "deployment tradeoffs"
```

### `heyditto network <pair-id> [--limit <n>]`

Traverse a memory's network — related memories connected via shared subjects. Default `limit` is 20, max 50.

```bash
heyditto network 3a1084ae-235a-433d-9493-2335a0dfeb57 --limit 30
```

## Output

All commands emit JSON by default — pipe through `jq` for shaping. `heyditto config` prints a Claude/Cursor-compatible MCP config snippet.

## Authoritative reference

`heyditto status` prints the live tool list straight from the MCP — trust it over this file if anything drifts.

## Source + support

- **CLI on npm:** https://www.npmjs.com/package/@heyditto/cli (`npm i -g @heyditto/cli`)
- **Skill repo:** https://github.com/ditto-assistant/ditto-clawhub
- **CLI repo:** https://github.com/ditto-assistant/ditto-cli
- **Claim an agent account:** run `heyditto init --agent --agent-caller openclaw --json`, then open the printed `claimURL`
- **Account / backend support:** support@heyditto.ai
