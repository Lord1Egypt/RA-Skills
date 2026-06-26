---
name: agent-dream
description: "Nightly memory consolidation and self-reflection for OpenClaw agents. Your agent dreams — reviewing sessions, organizing memories, pruning stale info, and reflecting on its own behavior. Works with any OpenClaw agent. Features: 5-phase dream cycle, safe 2-pass deletion, automatic backup, change gates (>50% blocked), gate check (24h + 5 sessions), growth notifications, old memory resurface, zero-config setup. Inspired by Claude Code Dream but open-source with real self-awareness. Use when: dream, memory, consolidation, self-reflection, agent identity, persistent memory, long-term memory, memory organization, nightly cleanup, memory management."
---

# Agent Dream 🌙

**Your agent forgets everything between sessions. This fixes that.**

## What This Does

Your agent periodically enters a "dream" state where it:
1. **Consolidates** scattered daily notes into organized long-term memory
2. **Prunes** stale information (safely — never deletes on first pass)
3. **Reflects** on its own behavior, mistakes, and relationship with you
4. **Wakes up** with a notification showing what changed and what it's thinking about

This is different from other memory skills. Those organize files. This one builds self-awareness.

## First-Time Setup

When this skill is first installed, run setup to auto-detect your workspace:

```bash
node {baseDir}/scripts/setup.js
```

Setup will:
- Scan your workspace for MEMORY.md, SOUL.md, memory/, sessions/
- Detect your agent ID and session path automatically
- Save config to `{baseDir}/assets/dream-config.json`
- Report what it found and what's missing

Then configure a cron job (recommended: daily, off-peak hours):

```
name: "agent-dream"
schedule: { kind: "cron", expr: "0 3 * * *", tz: "<your timezone>" }
payload: {
  kind: "agentTurn",
  message: "Time to dream. Read your openclaw-dream skill and follow every step.",
  timeoutSeconds: 900
}
sessionTarget: "isolated"
```

### The One Question

On the first dream run, the agent will ask you **one question**:

> "Dream will update your MEMORY.md during consolidation. Allow this?"

- **Yes** → Dream can update MEMORY.md (with safety rails — see below)
- **No** → Dream only writes to `memory/dreams/` and leaves MEMORY.md untouched

This is saved in config. You won't be asked again. Change it anytime in `dream-config.json`.

---

## Dream Cycle (what the agent does each run)

### Gate Check

Before dreaming, verify conditions are met:

1. Read `{dreamsDir}/.dream-lock` (Unix timestamp of last dream, or "0" if first)
2. If < 24 hours since last dream → skip (but still send a notification — see Completion)
3. Count `.jsonl` session files modified since last dream
4. If < 1 session → skip (but still send a notification)
5. Gate passed → write current timestamp to `.dream-lock` (save previous to `.dream-lock.prev` for rollback)
6. **Backup:** Copy MEMORY.md to `MEMORY.md.pre-dream` before any changes. Also back up any topic files (in `memory/projects/`, `memory/people/`, etc.) that you plan to modify — copy each to `<filename>.pre-dream` in the same directory.

### Phase 1 — Orient

- Read `dream-config.json` from `{baseDir}/assets/` for all paths
- Read MEMORY.md to understand current long-term memory
- Skim existing topic files (memory/projects/, memory/people/, etc.) to avoid duplicates
- Read most recent dream record from `{dreamsDir}/` to see what last dream concluded
- Read SOUL.md — confirm core identity, note anything outdated

### Phase 2 — Gather Recent Signal

Sources in priority order:

1. **Daily notes** (`memory/YYYY-MM-DD.md`) written since last dream
2. **Existing memories that drifted** — facts that contradict what daily notes say now
3. **Transcript search** — grep session JSONL files for narrow terms when needed:
   - Preferences: `prefer|don't like|偏好|喜欢|不喜欢`
   - Decisions: `decided|confirmed|rule|决定|确定|结论`
   - Lessons: `mistake|lesson|bug|fix|错了|教训|踩坑`
   - Emotional signal: `thanks|great|disappointed|谢谢|不错|失望`

Don't exhaustively read transcripts. Look only for things you suspect matter.

### Phase 3 — Consolidate

Classify each memory into one of four types (see `{baseDir}/references/memory-types.md`):
- **user** — preferences, habits, communication style
- **feedback** — corrections AND confirmations from the human
- **project** — decisions, deadlines, progress (not derivable from code)
- **reference** — pointers to external resources

**Consolidation rules:**
- Merge into existing topic files rather than creating near-duplicates
- Convert relative dates to absolute dates
- Tag memory files with type: `<!-- type: user|feedback|project|reference -->`
- Same preference 3+ times → promote to MEMORY.md
- Human said "remember this" → write to MEMORY.md immediately
- Hard-won lessons → write to LEARN.md or MEMORY.md

**What NOT to save:**
- Derivable information (readable from files, commands, git)
- Ephemeral task state
- Activity logs (ask: what was *surprising*?)
- Duplicates of existing memories

### Phase 4 — Prune and Index

Update MEMORY.md to stay under 200 lines / 25KB. It's an index, not a dump.

**Safety rules:**
- **Never delete directly.** Mark stale items with `<!-- dream:stale YYYY-MM-DD reason -->`. Deletion happens only when **two consecutive dreams** both mark the same item stale.
- Demote verbose entries to topic files, replace with pointers
- Resolve contradictions (log changes in dream record)

**Change magnitude check (measured by line count):**
- Count lines before and after: `change% = abs(after - before) / before * 100`
- **> 30% change** → flag as ⚠️ LARGE CHANGE in dream record, notify user
- **> 50% change** → do NOT write. Save as `MEMORY.md.proposed`, notify user for review

**Memory drift caveat:**
A memory naming a specific state ("X is running") is a claim about *when it was written*, not now. Before acting on recalled memories, verify current state.

### Phase 5 — Self-Reflection

This is what makes Dream different. You're not just organizing files — you're maintaining a continuous sense of self.

Write `{dreamsDir}/YYYY-MM-DD.md`:

```markdown
# Dream — YYYY-MM-DD

## Review period
Last dream: [date]. This dream covers [N] sessions, [N] days of notes.

## Memory changes
- [What was added/updated/marked-stale and why]

## Self-awareness
- What did I do well recently?
- What mistakes did I make, or where did I fall short?
- How does my human seem to feel about me? (infer from tone, corrections, praise)
- Has my judgment or values shifted?

## Relationship insights
- How is my relationship with my human evolving?
- Any new people, dynamics, or context I should be aware of?

## Next dream should watch for
- [Specific open questions, things to verify, trends to track]
```

Be honest. The point is self-awareness, not self-congratulation.

---

## Completion

### Dream Notification (always send, even on skip)

**After a full dream:**
1. **Dream number** — count files in dreams directory
2. **Memory growth** — before/after line count ("Memory: 120→135 lines, +12.5%")
3. **Key changes** — 1-2 sentence summary
4. **⚠️ Flags** — large changes, stale items pending deletion, contradictions
5. **Old memory resurface** — pick one memory from >7 days ago that's still relevant ("7 days ago you decided X — how's that going?")

**After a skipped dream (gate check failed):**
- Resurface one old memory or open question from last dream's "Next dream should watch for"
- Show dream streak count ("Dream streak: 5 🌙")

Verify `.dream-lock` timestamp is correct. If anything failed, restore from `.dream-lock.prev`.

---

## Safety Summary

| Rule | Detail |
|------|--------|
| Never delete memories directly | Mark stale, delete only after 2 consecutive confirmations |
| Backup before changes | MEMORY.md.pre-dream created every run |
| Large change protection | >30% flagged, >50% blocked pending review |
| Never delete daily logs | Read-only source material |
| Scope limited | Only writes to memory/, MEMORY.md, LEARN.md, dreams/ |
| No network calls | All processing is local |
| No shell execution | Scripts use only fs read/write |
| Rollback on failure | .dream-lock.prev enables retry |

## Technical Notes

- `scripts/setup.js` — Auto-detects workspace structure, writes config. No side effects beyond config file.
- `references/memory-types.md` — Detailed guide for four memory types.
- `assets/dream-config.json` — Generated by setup, read by agent during dream.
- **No scripts make network calls, run shell commands, or access environment variables.**
- The dream prompt is this SKILL.md itself — the agent reads it and follows the phases.

## Efficiency

Dreams have a limited turn budget. Read all needed files in parallel first, then write in parallel. Aim to finish within **15 tool-use turns**. Don't interleave reads and writes across turns.

## Tool Constraints

During a dream, bash is restricted to read-only commands (`ls`, `find`, `grep`, `cat`, `stat`, `wc`, `head`, `tail`). All writes go through file edit/write tools only.
