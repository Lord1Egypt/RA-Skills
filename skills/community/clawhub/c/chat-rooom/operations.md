# Operations - Chat Rooom

## Open a Room

Create the minimal structure first:

```bash
mkdir -p .chat-rooom/rooms/main/{channels,inbox}
```

Then add `room.md`, `summary.md`, `jobs.md`, and `claims.md` from `memory-template.md`. Use `main` unless a better name is already obvious.

## Join a Room

Before posting:
1. Read `summary.md`
2. Read the relevant channel file
3. Check `claims.md`
4. Post one short update about what you are taking

Do not reread the entire room unless the summary is stale or contradictory.

## Write Safely

Append-only files can be written directly. For files you rewrite, use a temp file and rename it into place:

```bash
tmp="$(mktemp)"
cp .chat-rooom/rooms/main/summary.md "$tmp"
# edit $tmp
mv "$tmp" .chat-rooom/rooms/main/summary.md
```

Prefer archive copies over destructive cleanup. If a room is noisy, open a new channel or rotate the room into `archive/`.

## Run a Handoff

Every handoff should contain:
- Current status
- Claimed surfaces being released or renewed
- Evidence already collected
- Exact next owner
- One open question, if any

If the next owner is unclear, the handoff is incomplete.

## Close a Room

When work finishes:
1. Mark jobs `done`
2. Clear or expire claims
3. Update `summary.md` with final outcome
4. Move the room under `.chat-rooom/archive/` if the user wants historical retention

Keep the final summary short enough that a future agent can decide in seconds whether to reopen the room.
