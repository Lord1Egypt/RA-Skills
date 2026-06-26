# Usage

This skill is intended for OpenClaw users who want to add **Alice** as a continuity layer for stronger memory, cleaner resumption, open-loop tracking, and provenance-backed recall.

Alice can be used with OpenClaw in two main ways:

1. **Import mode** — bring existing OpenClaw memory into Alice
2. **Augmentation mode** — keep using OpenClaw, but let Alice improve recall, resumption, and continuity workflows

---

## What Alice is doing

Alice is not meant to replace OpenClaw’s core workflow.

Instead, it adds:

- stronger long-term memory
- resumption briefs for interrupted work
- correction-aware memory
- open-loop tracking
- provenance-backed explanations
- trust-aware promotion of durable memory

That means you can continue using OpenClaw while upgrading how memory and context are handled over time.

---

## Integration mode 1: Import existing OpenClaw memory

Use this mode when you want Alice to ingest existing OpenClaw memory and normalize it into structured continuity objects.

Typical outcomes:

- old memory becomes queryable through Alice
- decisions and commitments become easier to recall
- resumption becomes cleaner
- provenance remains visible

### Typical flow

1. Identify the OpenClaw workspace or memory directory you want to use
2. Run the Alice OpenClaw import path
3. Let Alice normalize imported content into continuity objects
4. Start using Alice recall, resume, explain, and open-loop workflows against imported memory

### Example outcomes

After import, you should be able to ask questions like:

- What did we decide about this project?
- What changed recently?
- What am I waiting on?
- What should happen next?

---

## Integration mode 2: Augment an existing OpenClaw workflow

Use this mode when you want to keep OpenClaw as the main runtime but improve continuity with Alice.

In this setup, Alice can be used for:

- recall
- resumption
- open-loop review
- correction-aware memory
- explain / provenance flows

### Typical flow

1. Keep OpenClaw as your active workflow
2. Connect Alice through the documented integration path
3. Use Alice when you need:
   - better recall
   - a resumption brief
   - open-loop review
   - memory correction
   - explanation of why something is in memory

### Best use cases

This mode is especially useful when:

- a project has been running for days or weeks
- important decisions are buried in old sessions
- you want a cleaner “get me back into this” workflow
- you need explicit provenance and correction rather than loose summarization

---

## Recommended workflow

A strong default workflow looks like this:

### 1. Work normally in OpenClaw
Keep using OpenClaw the way you already do.

### 2. Use Alice for continuity
When context becomes large or fragmented, use Alice to:

- recall key decisions
- generate a resumption brief
- inspect open loops
- explain why a memory item exists
- correct stale or inaccurate memory

### 3. Improve memory quality over time
Use Alice’s correction-aware workflows so future recall improves instead of drifting.

---

## Example questions Alice is good at

Alice is especially useful for questions like:

- What did we decide about this?
- What changed since the last time I worked on it?
- What am I still waiting on?
- What are the active blockers?
- Why is this memory showing up?
- Is this still current, or was it superseded?

---

## What makes this different from basic memory

This integration is useful because Alice does more than store raw conversation history.

It adds:

- structured continuity objects
- correction and supersession
- trust-aware memory handling
- provenance-backed explanations
- resumption-oriented retrieval
- open-loop awareness

So the goal is not “more memory.”

The goal is **better continuity**.

---

## Notes

- Alice is designed as a continuity layer, not a closed assistant silo.
- OpenClaw remains useful as the primary runtime.
- Alice is most valuable when work spans multiple sessions, decisions change over time, or you need a clean way to resume without rereading everything.

## Project

GitHub: https://github.com/samrusani/AliceBot