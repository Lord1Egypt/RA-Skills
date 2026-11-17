---
name: visual-refresh
version: 1.0.0
description: Change, fix, re-roll or version visuals that Canvora already produced — targeted edits, variations, localization, edit history and revert — without paying to regenerate. Use when the user wants to tweak, fix, restyle, translate or undo an existing visual.
homepage: https://canvora.ai/for-agents
metadata: {"openclaw":{"emoji":"🩹","requires":{"bins":["canvora"],"env":["CANVORA_API_KEY"]}}}
---

# Refining what already exists

The most expensive mistake an agent makes with Canvora is regenerating. A new
generation costs full price, throws away a design the user already liked, and
comes back different in ways they didn't ask for. Almost every "can you change
X" is a 3-credit edit.

Setup and credits: see the `canvora` skill.

## Pick the right operation

| The user says | Operation | Cost |
|---|---|---|
| "make the headline bigger", "change 73% to 78%", "warmer colors" | `edit` one output | **3** |
| "same thing in Spanish" | `localize` the generation | 10 per visual per language |
| "show me some other options" | `variations` | 10 per image (15 per carousel slide) |
| "go back to the previous one" | `revert_edit` (MCP) | **free** |
| "what did we change?" | `get_edit_history` (MCP) | free |
| "completely different message" | a new `generate` | full price — the only honest case |

If you're unsure between `edit` and `variations`: does the user want *this*
design fixed, or a *different* design? Fixed → edit. Different → variations.

## Targeted edits

```bash
# Preview first (prints Canvora's interpretation, spends nothing)
canvora edit $OUTPUT_ID --prompt "make the headline bigger and increase contrast"

# Execute
canvora edit $OUTPUT_ID --prompt "make the headline bigger and increase contrast" --yes --json
```

- Edits act on **one output**, identified by `outputId` (not the generation id).
  Get it from `canvora status <generationId> --json`.
- Without `--yes` you get a preview of what it understood — show that to the
  user when the instruction was ambiguous.
- "needs clarification" means the instruction was too vague. Re-prompt with a
  concrete noun: *which* text, *which* element.
- One change per edit. "Bigger headline and swap the photo and make it blue" is
  three edits, and each one preserves more of the design than a combined
  instruction would.

## Whole-generation operations

```bash
# Every visual in the generation, new language, layout untouched
NEW=$(canvora localize $GENERATION_ID --language es | head -1)
canvora status "$NEW" --json    # repeat every ~30s until completed

# Fresh takes on the same content
NEW=$(canvora variations $GENERATION_ID --count 2 | head -1)
canvora status "$NEW" --json
```

Drop `--json` on the capture and take `| head -1` — the first stdout line is
the bare new generation id (progress notes go to stderr). The same idiom works
for `generate`, `localize` and `variations`, so there is nothing to remember,
and it needs no `jq`.

**Always state the cost in the same message as the run** — announce it, don't
ask permission. `variations --count 2` on a 5-slide carousel is 10 new images
at 15 credits = 150. That surprises people. When you picked `--count` yourself,
confirm that number first.

Both of these fan out over the whole generation, so at 3+ outputs skip `--wait`
and poll `status`: your harness likely kills a shell command at 120s while the
work carries on server-side. Never re-run the command after a timeout — that
starts a second, separate job. See the `canvora` skill's "Long runs" section.
`--wait` is still fine when the source generation is a single visual.

Both need the Visual Editor feature (Starter plan or an active Campaign Pack).
A 403 is a plan gate, not an auth failure — say that, don't retry.

## Versioning (MCP clients)

- `get_edit_history({ output_id })` — every version of one visual
- `revert_edit({ generation_id, output_index, edit_id })` — go back, free

This is the safety net that makes editing worth trying: an edit the user
dislikes costs 3 credits and can be undone. Say that when they hesitate.

## When regeneration IS correct

Be honest about the three cases where refining won't help:

1. The **message** is wrong, not the design.
2. They need a **different format/size** — an edit can't reflow a 1:1 into 9:16.
3. The generation came back `partial` and slides are **missing** — the failed
   ones were refunded; re-run for those specific slides.

## Quality checklist

- [ ] `edit` tried before anything more expensive
- [ ] Correct id used (`outputId` for edits, `generationId` for localize/variations)
- [ ] One change per edit; preview shown when the instruction was ambiguous
- [ ] Cost stated before `variations`/`localize`
- [ ] 403 explained as a plan gate
- [ ] Revert offered (MCP) so the user knows edits are reversible
