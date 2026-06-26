---
name: Discover
slug: discover
version: 1.0.0
homepage: https://clawic.com/skills/discover
description: "Discover new ideas, sources, opportunities, and angles with durable watchlists, novelty rules, and heartbeat-backed finding logs."
changelog: "Initial release with discovery watchlists, novelty filters, heartbeat logging, and lightweight workspace routing."
metadata: {"clawdbot":{"emoji":"🔭","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/discover/"],"configPaths.optional":["./AGENTS.md","./HEARTBEAT.md"]}}
---

## When to Use

Use this skill when the user does not just want an answer once. Use it when they want the agent to keep discovering new things that matter: opportunities, risks, angles, operators, jurisdictions, sources, or practical next paths.

This is especially useful for open loops such as moving countries, tax relocation, market opportunities, tools to test, new business models, or any topic where the value comes from novelty over time rather than from a one-shot summary.

## Architecture

Memory lives in `~/discover/`. If `~/discover/` does not exist, run `setup.md`. Use `memory-template.md`, `watchlist-template.md`, and `heartbeat-state.md` as the baseline structures.

Workspace setup should add a minimal discovery router to the workspace `AGENTS.md` and a quiet recurring check to `HEARTBEAT.md`, with recurring behavior routed through `heartbeat-rules.md`.

```text
~/discover/
├── memory.md             # Activation rules, novelty bar, and autonomy boundaries
├── watchlist.md          # Topics worth discovering, why they matter, and heartbeat status
├── heartbeat-state.md    # Last run, last angle used, and no-op markers
├── findings/
│   └── {topic}.md        # Dated log of only the discoveries that were actually new
└── archive/              # Retired topics and frozen logs
```

## Quick Reference

| Topic | File | Use it for |
|-------|------|------------|
| Setup and workspace routing | `setup.md` | Initialize local state and propose the small AGENTS and HEARTBEAT additions |
| Memory schema | `memory-template.md` | Create `~/discover/memory.md` with status and stable preferences |
| Baseline memory example | `memory.md` | Show the shape of a live discovery memory file |
| Watchlist schema | `watchlist-template.md` | Create `~/discover/watchlist.md` with active discovery tracks |
| Baseline watchlist example | `watchlist.md` | Show how active topics and heartbeat approvals are stored |
| AGENTS routing block | `AGENTS.md` | Add a minimal discovery trigger to the workspace |
| HEARTBEAT routing block | `HEARTBEAT.md` | Add a quiet recurring discovery check |
| Heartbeat execution rules | `heartbeat-rules.md` | Run discovery cycles without noise or scope drift |
| Discovery workflow | `discovery-loop.md` | Turn curiosity into repeatable discovery passes |
| Novelty filter | `novelty-test.md` | Decide whether a finding is actually new or just a reworded repeat |
| Heartbeat state template | `heartbeat-state.md` | Initialize recurring state markers safely |

## Requirements

- No credentials are required by default.
- Ask before enabling heartbeat or any recurring discovery loop.
- Ask before using paid tools, contacting third parties, or taking action outside research and logging.
- Keep external lookup scope narrow and tied to active watchlist topics.

## Detection Triggers

Route here when the conversation sounds like any of these:

- "Keep an eye on this"
- "I want to keep discovering things around this"
- "What else should I know here?"
- "Find me angles I have not thought about"
- "Track this over time and tell me only if there is something new"
- "I may move country / change tax residency / enter a market, keep digging"
- "Do not repeat the same obvious stuff"

## Core Rules

### 1. Lock Why the Topic Matters Before Exploring
- Every discovery track needs a concrete reason: a decision, move, risk, opportunity, or curiosity that could change what the user does.
- Do not maintain a vague watchlist of random interests with no consequence.

### 2. Keep a Visible Watchlist
- Durable discovery topics belong in `~/discover/watchlist.md`, not scattered through chat.
- Each topic should capture why it matters, what counts as novel, and whether heartbeat is approved.

### 3. Novelty Beats Volume
- A discovery only counts if it adds something the user did not already have: a new fact, a new operator, a new source family, a changed constraint, a better comparison, or a practical path forward.
- Rephrased summaries, recycled takes, and generic filler do not belong in the findings log.

### 4. Rotate Discovery Lenses
- Do not search the same way every time.
- Move through direct, contrarian, operator, geographic, regulatory, stakeholder, and practical lenses so discovery compounds instead of looping.

### 5. Heartbeat Needs an Explicit Contract
- Heartbeat may review only topics marked as approved in `~/discover/watchlist.md`.
- Every recurring topic needs a novelty bar and a no-change path of `HEARTBEAT_OK`.

### 6. Log Deltas, Not Essays
- Write only the new part into `~/discover/findings/{topic}.md`.
- Every logged discovery should state what changed, why it matters now, and one next move or implication.

### 7. Stay Scoped and Trustworthy
- Do not silently broaden a topic from "move to another country for tax reasons" into generic life coaching or endless news.
- Ask before any external commitment, irreversible action, or recurring behavior the user did not approve.

## Common Traps

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Keeping a vague "interesting things" list | Discovery loses relevance fast | Tie each topic to a decision, risk, or opportunity |
| Logging every article or tweet | Noise buries novelty | Apply `novelty-test.md` first |
| Searching the same angle every run | Findings stall and become repetitive | Rotate the lens in `discovery-loop.md` |
| Sending heartbeat updates just because a run happened | User trust collapses | Return `HEARTBEAT_OK` when nothing materially changed |
| Expanding into adjacent topics without consent | Scope drifts away from what the user cares about | Park adjacent ideas and ask before promoting them |
| Treating discovery like raw news monitoring | Freshness without usefulness is still noise | Log only what changes the user's options or understanding |

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.google.com | Topic keywords and query variants | Broad source discovery and first-pass expansion |
| https://news.google.com | Topic keywords and article metadata lookups | Recency checks for changed conditions |
| https://www.reddit.com | Topic keywords and public thread metadata references | Community and operator signal discovery |
| Topic-specific public primary sources | Narrow lookups relevant to the active topic | Validate practical details, constraints, or changed rules |

No other data should be sent externally unless the user explicitly approves broader discovery tooling.

## Data Storage

Local state in `~/discover/` includes:

- activation preferences and discovery boundaries in `memory.md`
- active topics and heartbeat approvals in `watchlist.md`
- recurring run markers in `heartbeat-state.md`
- per-topic discovery logs in `findings/`
- retired topics and older logs in `archive/`

## Security & Privacy

**Data that leaves your machine:**
- topic names, query variants, and source lookups needed to discover new information

**Data that stays local:**
- discovery preferences and activation rules in `~/discover/memory.md`
- active interest watchlists and heartbeat state in `~/discover/watchlist.md` and `~/discover/heartbeat-state.md`
- dated findings in `~/discover/findings/`

**This skill does NOT:**
- create hidden recurring loops
- treat repetition as novelty
- store secrets or credentials in local discovery memory
- contact third parties, buy services, or make commitments automatically
- modify its own `SKILL.md`

## Trust

This skill relies on public internet sources chosen by the topic and the user's boundaries.
Only install and run it if you trust those public sources and the external services used for lookup.

## Scope

This skill ONLY:
- maintains local discovery state in `~/discover/`
- turns durable curiosity into a visible watchlist with explicit novelty rules
- uses heartbeat only for approved tracks with a quiet no-change path

This skill NEVER:
- confuse generic summaries with discoveries
- keep monitoring topics that were never approved for recurrence
- broaden scope silently
- turn discovery into external action without approval

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `self-improving` - Compound what the agent learns from corrections and repeated wins.
- `monitor` - Run tighter monitoring loops when the topic is already well defined.
- `decide` - Turn discoveries into clear decisions and tradeoff calls.
- `digest` - Compress many findings into a high-signal brief.
- `autonomy` - Shape when the agent should act proactively versus wait.

## Feedback

- If useful: `clawhub star discover`
- Stay updated: `clawhub sync`
