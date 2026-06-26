---
name: bear-share-sync
description: Detect new Bear notes tagged #share, extract core content into JSON Canvas knowledge nodes on agent_capabilities.canvas, then distribute a preview via BlueBubbles iMessage. Use when syncing Bear notes to a shared knowledge graph and work group, or when asked to "sync share notes", "distribute Bear notes", "publish from Bear", or "update capabilities canvas from Bear".
---

# Bear Share Sync

Three-step pipeline: **Bear #share → Canvas node → iMessage preview**.

## Prerequisites

- Bear running with `grizzly` CLI installed and token configured (`~/.config/grizzly/token`)
- BlueBubbles channel configured in OpenClaw gateway (`channels.bluebubbles`)
- Canvas file at `canvases/agent_capabilities.canvas` (created on first run if missing)

## Configuration

Set environment variables (or defaults apply):

| Variable | Default | Purpose |
|----------|---------|---------|
| `BEAR_SHARE_TAG` | `share` | Bear tag to watch |
| `BEAR_SHARE_CANVAS` | `canvases/agent_capabilities.canvas` | Path to canvas file |
| `BEAR_SHARE_TARGET` | _(required)_ | iMessage target: E.164 phone, email, or `chat_guid:...` |
| `BEAR_SHARE_STATE` | `~/.bear-share-sync/state.json` | Tracks processed note IDs |

## Workflow

### 1. Poll for new #share notes

```bash
bash scripts/poll-share-notes.sh
```

Outputs JSON array of unprocessed notes (id, title, content, tags). Updates state file to mark notes as seen.

### 2. Update canvas

For each new note, append a knowledge node to the canvas. Run:

```bash
python3 scripts/update-canvas.py --canvas "$BEAR_SHARE_CANVAS" --notes /dev/stdin
```

Node layout: new nodes placed at Y = max(existing Y) + 200, X = 0. Node color = `"4"` (green). Edge from a central "Shared Notes" group node if present.

See [references/canvas-schema.md](references/canvas-schema.md) for the JSON Canvas structure.

### 3. Send preview via BlueBubbles

```bash
bash scripts/send-preview.sh "<target>" "<title>" "<summary>"
```

Uses the `message` tool with `channel: "bluebubbles"`. Sends a compact preview:

```
📝 New shared note: <title>

<first 280 chars of content>…

🔗 See canvas for full node.
```

## Full Pipeline (one-shot)

```bash
NOTES=$(bash scripts/poll-share-notes.sh)
if [ "$NOTES" != "[]" ]; then
  echo "$NOTES" | python3 scripts/update-canvas.py --canvas "$BEAR_SHARE_CANVAS" --notes /dev/stdin
  echo "$NOTES" | python3 -c "
import json, sys, subprocess
for n in json.load(sys.stdin):
    subprocess.run(['bash','scripts/send-preview.sh',
        '$BEAR_SHARE_TARGET', n['title'], n['content'][:280]])
"
fi
```

## Scheduling

Set up a cron job to poll every 15 minutes:

```
*/15 * * * * cd /path/to/skill && ./scripts/poll-share-notes.sh | ...
```

Or use OpenClaw cron with `payload.kind = "agentTurn"` and the pipeline command.

## Notes

- The state file prevents re-processing; delete it to re-sync all notes.
- Canvas uses Obsidian-compatible JSON Canvas spec (see [references/canvas-schema.md](references/canvas-schema.md)).
- If BlueBubbles send fails, the canvas is still updated; check gateway logs for delivery errors.
