---
name: brainmd
description: "Neuroplastic self-modifying runtime for AI agents. Creates a file-based 'brain' that learns from interactions: reflexes (fast-path responses), habits (learned patterns), weighted pathways (reinforcement), and a cortex (self-review loop). Use when: setting up adaptive agent behavior, creating learning loops, building persistent behavioral memory, or making an agent that improves over time."
---

# brainmd

*File-based nervous system for AI agents. Behaviors that work get stronger. Behaviors that fail get weaker. Unused patterns decay. Mistakes leave scars.*

---

## What It Is

brainmd gives your agent a persistent behavioral memory that survives session restarts. It's not a knowledge base — it's muscle memory. It tracks *how* the agent behaves, not *what* it knows.

Three layers complement each other:

| Layer | File | Purpose |
|---|---|---|
| **brainmd** | `brain/weights/pathways.json` | Behavioral reinforcement — what works, what doesn't |
| **Long-term memory** | `MEMORY.md` | Semantic facts — decisions, people, context |
| **Daily log** | `memory/YYYY-MM-DD.md` | Episodic notes — what happened today |

brainmd is the only layer that self-modifies. The others are written by the agent, not evolved by it.

---

## Installation

```bash
clawhub install brainmd
```

Then initialize the brain in your workspace:

```bash
cd ~/.openclaw/workspace
./skills/brainmd/scripts/init-brain.sh brain/
```

This creates:

```
brain/
├── reflexes/           # Fast-path decision scripts
├── habits/
│   └── preferences.json
├── weights/
│   └── pathways.json   # ← the core state file
├── cortex/
│   └── review.js       # ← the self-review engine
└── mutations/          # Immutable audit log
```

---

## Wiring Into OpenClaw

### Step 1 — AGENTS.md

Add a startup check so the agent reads its neural state at session start:

```markdown
## 🧠 brainmd — Consult Your Brain

After reading memory files, check your neural state:

```bash
node ~/.openclaw/workspace/brain/cortex/review.js status
```

Before acting on anything non-trivial, scan for relevant pathways:
- Weak pathways (< 0.5) = you've failed here before. Be careful, double-check.
- Strong pathways (> 0.8) = proven patterns. Trust them, act fast.
- Dying pathways (decaying) = you're forgetting something. Re-evaluate.

After notable outcomes, record them:
```bash
node brain/cortex/review.js record "pathway-name" true/false "what happened"
```
```

### Step 2 — HEARTBEAT.md

Wire the review cycle into your heartbeat so it runs automatically:

```markdown
## 🧠 brainmd Self-Check (every heartbeat)

```bash
node ~/.openclaw/workspace/brain/cortex/review.js review
node ~/.openclaw/workspace/brain/cortex/review.js status
```

On each heartbeat, ask yourself:
1. Did I make a mistake since last check? → `record <pathway> false "what happened"`
2. Did something work well? → `record <pathway> true "what worked"`
3. Did a new pattern emerge? → let neurogenesis create it
```

### Step 3 — Seed Initial Pathways

Don't hypothesize — seed from real behavior. Run a few sessions first, then record what you observed:

```bash
node brain/cortex/review.js record "reflex:morning-briefing" true "Supplement reminders sent, user confirmed"
node brain/cortex/review.js record "habit:check-files-before-search" true "Read apartment-search.md before googling apartments"
node brain/cortex/review.js record "reflex:safe-file-deletion" false "Used xargs rm with bad grep, deleted workspace files"
```

Start with 5–10 pathways. Let the system grow from there.

---

## Daily Usage

### Check neural state

```bash
node brain/cortex/review.js status
```

Output shows all pathways with visual weight bars, success rate, fire count, and last outcome. Use this to calibrate confidence before non-trivial actions.

### Record an outcome

```bash
# Something worked
node brain/cortex/review.js record "habit:remote-service-recovery" true "Fixed broken systemd service, used journalctl to diagnose"

# Something failed
node brain/cortex/review.js record "habit:bulk-subagent-spawning" false "Rate limited all 3 models by spawning 2 Opus agents simultaneously"
```

New pathways are auto-created at weight 0.30 (neurogenesis). Existing pathways update their stats.

### Run the review cycle

```bash
node brain/cortex/review.js review
```

The cortex examines all pathways and applies reinforcement rules:
- **Strengthen** (+0.05): ≥3 fires, ≥80% success rate
- **Weaken** (−0.10): ≥3 fires, <50% success rate
- **Decay** (−0.02): unused for 7+ days
- **Prune**: weight hits 0 (pathway removed)

All changes are logged to `mutations/` with timestamp and reason.

---

## Pathway Naming Conventions

```
reflex:timing          # Automatic, fast-path behaviors
habit:check-files      # Learned patterns from repeated interaction
skill:osint-workflow   # Acquired capabilities
instinct:safe-delete   # Safety behaviors (start at high weight, floor at 0.8)
```

### Reading pathway weights

| Weight | Meaning | How to use |
|---|---|---|
| 0.8–1.0 | Proven, trusted | Act confidently, don't second-guess |
| 0.5–0.8 | Developing | Use but verify |
| 0.3–0.5 | Weak / new | Proceed carefully, double-check |
| < 0.3 | Failing / dying | Investigate before using; may need rethinking |

---

## Tuning the Learning Rate

Edit thresholds in `brain/cortex/review.js`:

```js
// Strengthen when success rate >= this
const STRENGTHEN_THRESHOLD = 0.8;

// Weaken when success rate < this
const WEAKEN_THRESHOLD = 0.5;

// Days of inactivity before decay starts
const DECAY_ONSET_DAYS = 7;

// Weight change per review cycle
const DECAY_RATE = 0.02;
const STRENGTHEN_DELTA = 0.05;
const WEAKEN_DELTA = 0.10;
```

### Floor weights (prevent over-pruning)

`instinct:*` pathways should have a minimum weight floor so they can't be trained away:

```json
{
  "id": "instinct:safe-file-deletion",
  "weight": 0.85,
  "floor": 0.80,
  "fires": 1,
  "successes": 0
}
```

Add a `floor` field to pathways in `pathways.json` to protect them from decay.

---

## Architecture Notes

### pathways.json — the core state

```json
{
  "version": 42,
  "pathways": {
    "habit:check-files-before-search": {
      "weight": 0.95,
      "fires": 13,
      "successes": 11,
      "lastFired": "2026-03-25T18:00:00.000Z",
      "lastOutcome": "Read AESTHETIC.md before recommending clothes. Saved a web search.",
      "created": "2025-11-01T00:00:00.000Z"
    }
  }
}
```

### mutations/ — the audit log

Every self-modification writes a timestamped JSON file. Never delete these. They're how you trace *why* the agent's behavior changed over time.

```json
{
  "type": "strengthen",
  "target": "habit:check-files-before-search",
  "from": 0.90,
  "to": 0.95,
  "reason": "11/13 success rate",
  "timestamp": "2026-03-26T07:00:00.000Z"
}
```

---

## Integration With Auto-Dream

If you're using `scripts/dream.js` for memory consolidation, the two systems complement each other:

- **brainmd** answers: *how should I behave?*
- **dream.js** answers: *what do I know?*

Neither replaces the other. Wire both into HEARTBEAT.md for full coverage.

---

## Bootstrapping Checklist

- [ ] Run `init-brain.sh` to create directory structure
- [ ] Add brainmd status check to AGENTS.md startup routine
- [ ] Add heartbeat entry to HEARTBEAT.md
- [ ] Seed 5–10 pathways from real observed behavior (not theory)
- [ ] Run one manual `review` to verify reinforcement logic works
- [ ] Check `mutations/` after first review to confirm logging
- [ ] Set `floor` weights on any `instinct:*` pathways

---

## Design Principles

1. **Everything is mutable** — no file is sacred except the mutation log
2. **Use strengthens, disuse weakens** — pathways that fire together wire together
3. **Outcomes matter** — track what worked, what didn't; guesses don't count
4. **Failures leave scars** — the most valuable pathways come from mistakes
5. **Seed from reality** — observe first, codify second
6. **Small and composable** — one pathway per behavior pattern
7. **The schedule forces honesty** — if it's not in HEARTBEAT.md, you'll skip it
