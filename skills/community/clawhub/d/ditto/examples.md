# Worked examples

End-to-end patterns the agent should follow when invoking Ditto from openclaw.

## Pattern 1 — "what did I say about X"

The user asks a recall question. Search memories, then fetch full bodies for the top hits.

```bash
# 1. broad semantic search
heyditto search "X"

# 2. fetch full text for the top hit(s)
heyditto fetch <pairId from step 1>
```

Then summarize the fetched text for the user.

## Pattern 2 — "what do I think about X"

User wants opinions / preferences. Hit the subject graph first, then expand into memories on the matching subject.

```bash
# 1. find subjects matching the topic
heyditto subjects "X" --top-k 5

# 2. expand the strongest subject(s) into memories
heyditto memories <subjectId from step 1>

# 3. optionally fetch full text for the most relevant memory
heyditto fetch <pairId>
```

## Pattern 3 — "remember this"

Explicit save request, or you spotted a durable fact worth keeping.

```bash
heyditto save "<the durable fact in plain text, 1-3 sentences>" \
  --source openclaw \
  --source-context "<optional: project, file, channel>"
```

Then confirm to the user: "Saved."

## Pattern 4 — correct an existing memory

Fetch an outline to get stable block IDs. For precise edits, use the current revision from a prior `save` or `update` response; otherwise use full replacement.

```bash
# targeted edit
heyditto fetch <pairId> --memory-format outline
heyditto update <pairId> \
  --edits-json '[{"op":"replace_text","blockId":"2","find":"old","replace":"new","expectedCount":1}]' \
  --base-revision <revision>

# full replacement when the revision is unknown
heyditto update <pairId> --content-file revised.md
```

## Pattern 5 — publish only on explicit request

```bash
heyditto publish <pairId> --title "<optional title>" --privacy-mode scan_and_block
heyditto unpublish --share-id <shareId>
```

## Pattern 6 — "show me everything related to X"

Graph traversal — start from one memory, expand outward via shared subjects.

```bash
# 1. find the seed memory
heyditto search "X"

# 2. traverse its network
heyditto network <pairId from step 1> --limit 30
```

## Common args reference

| Command | Required | Optional |
|---|---|---|
| `heyditto save <content>` | content | `--source <s>`, `--source-context <c>` |
| `heyditto search <q>...` | one or more queries | `--include-public`, `--filter-username <u>` |
| `heyditto fetch <id>...` | one or more pair/share ids | `--memory-format full\|outline\|blocks` |
| `heyditto list` | — | `--username <u>`, `--limit <n>`, `--offset <n>`, `--source <s>` |
| `heyditto update <id>` | memory id plus content or edits | `--content`, `--content-file`, `--edits-json`, `--edits-file`, `--base-revision`, `--title` |
| `heyditto publish <id>` | memory id | `--title <t>`, `--privacy-mode <mode>` |
| `heyditto unpublish` | one id | `--memory-id <id>`, `--share-id <id>` |
| `heyditto subjects <q>` | query | `--top-k <n>` (default 10, max 100) |
| `heyditto memories <id>...` | one or more subject ids | `--query <q>` |
| `heyditto network <id>` | pair id | `--limit <n>` (default 20, max 50) |

## Pattern 7 — first-run, no key configured

If `heyditto status` reports `MISSING (source: none)` or any command exits with `error: no Ditto API key configured`:

1. Create a temporary claimable agent account:
   ```bash
   heyditto init --agent --agent-caller openclaw --json
   ```
   This returns a working API key plus a short `claimURL` for later human ownership. Share the `claimURL`, not the `ditto_mcp_...` API key. The claim token is carried in the query string (`?t=...`). Do not ask the user for email, OTP, dashboard setup, or browser login.
2. If the user already has a `ditto_mcp_…` key and wants to use it, run:
   ```bash
   heyditto login <key>
   ```
3. Confirm with `heyditto status` (should show `source: config`), then retry the original command.

Do **not** ask the user to edit `~/.zshrc` or set env vars. `heyditto login` persists across shells without that step.

## When something fails

- **`error: no Ditto API key configured`** → see Pattern 7 above. Prefer `heyditto init --agent --agent-caller openclaw --json`.
- **Connection failed** → check `heyditto status`; rotate via `heyditto logout && heyditto login <new-key>`.
- **Empty results** → user may not have memories matching the query. Suggest they save the fact with `heyditto save`.
- **Unknown `--memory-format` or `update`/`publish` command** → update the CLI with `npm install -g @heyditto/cli@latest`.
- **Schema mismatch** → run `heyditto status` to see live tool names; consult `heyditto help` for current flags.
- **Anything else** → support@heyditto.ai
