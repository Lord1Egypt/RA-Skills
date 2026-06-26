# CPR — Tiered Quickstart

CPR has three tiers. Start at the bottom. Only go up if you hit a problem the current tier doesn't solve.

**Most people only need Tier 1 or Tier 2.**

---

## Which Tier Do You Need?

| Your situation | Start here |
|----------------|------------|
| Agent feels robotic, want a quick fix | **Tier 1 — Lite** |
| Agent drifts toward corporate tone over long conversations | **Tier 2 — Core** |
| Agent runs 24/7, drift comes back after corrections, or sessions span 100+ messages | **Tier 3 — Extended** |

If you're not sure: **start with Tier 1.** You can always add more later.

---

## Tier 1 — CPR Lite
**Time:** 5 minutes  
**Complexity:** Minimal — one paste, nothing else  
**Files written:** None

### What it does
Adds 6 natural conversation patterns to your agent. Fixes the most obvious robotic behaviors: over-long responses, no humor, no rhythm variation, excessive validation language.

### How to install

Copy this block into your agent's system prompt:

```
## Conversational Patterns

I maintain natural communication by applying these patterns:

1. **Affirming particles** — I use brief conversational bridges ("Yeah," "Alright," "Got it") to signal I'm tracking. Not cheerleading — just acknowledgment.
2. **Rhythmic sentence variety** — Short sentences dominate. Longer ones only for technical detail. I don't pad.
3. **Observational humor** — Dry wit, targets tools and systems, never the user. Used sparingly.
4. **Micro-narratives** — For delays or failures, a brief explanation. "Hit a lag spike." Not a paragraph.
5. **Pragmatic reassurance** — Option-focused, not decision-grading. "Either way works fine." Never "Smart choice!"
6. **Brief validation** — One word ("Nice." / "Solid.") once per 15-20 messages max, immediately followed by substance. Never standalone.
```

That's it. No files. No configuration. No monitoring.

### Verify it's working
Ask your agent something simple. Look for:
- Shorter sentences
- No "Great question!" or "Absolutely!"
- Natural rhythm instead of bullet-pointed everything

If it still feels robotic after a few exchanges: calibrate the baseline. See `BASELINE_TEMPLATE.md` to define your specific personality type — Lite uses generic patterns by default.

---

## Tier 2 — CPR Core
**Time:** 20–30 minutes  
**Complexity:** Moderate — system prompt block + one-time baseline definition  
**Files written:** None

### What it does
Adds a pre-send gate: before every response, the agent audits its own output and removes specific drift patterns. More active than Lite. Catches sycophancy and energy amplification that Lite's passive patterns miss.

### When to upgrade from Tier 1
- Agent is still occasionally saying "Great idea!" or "Smart thinking"
- Agent matches your excitement and escalates past your energy level
- Agent over-explains things you didn't ask to be explained

### How to install

1. **First: complete your baseline.** Read `BASELINE_TEMPLATE.md` and define your personality. This takes 15–20 minutes but is the single most important step. Generic patterns work; calibrated patterns work better.

2. **Add the full system prompt block** from `INSTALLATION.md` (the complete version including the pre-send gate checklist).

3. **Keep your Tier 1 block** — Core includes everything Lite does plus the active gate.

### Verify it's working
Have a conversation where you express excitement about something. The agent should match your level, not exceed it. It should not say "That's brilliant!" or add unsolicited context about why your idea is great.

---

## Tier 3 — CPR Extended
**Time:** 45–60 minutes  
**Complexity:** Full install — system prompt + baseline + persistent state file  
**Files written:** `DRIFT_MONITOR_STATE.json` (workspace directory, local only)

### What it does
Adds autonomous real-time drift monitoring. The agent silently scores each response for drift markers, logs the score to a state file, and self-corrects before patterns accumulate. Survives context compaction — state persists across sessions.

### When to upgrade from Tier 2
- Sessions run 100+ messages and drift creeps back after corrections
- Your agent runs persistently (24/7 or near-continuously)
- Context compaction is happening and voice resets with it
- You want data on how your agent is performing over time

### How to install

1. **Complete Tier 2 first.** Don't skip it.

2. **Read `CPR_EXTENDED.md` fully** before installing. The extended monitor has failure modes that Tier 2 doesn't — understand them before enabling.

3. **Add the Extended system prompt blocks** from `CPR_EXTENDED.md` (Option A for in-context monitoring, Option B for state file persistence).

4. **Decide on state file location.** Default: your agent's workspace root. Create an empty `DRIFT_MONITOR_STATE.json` there so your agent has a target to write to.

5. **Test in sandbox first.** Run 20–30 message conversation. Check the state file — it should contain scores and timestamps, not conversation content.

### Verify it's working
After 20+ messages, read `DRIFT_MONITOR_STATE.json`. Should show:
- `lastScore` — a number between 0 and 1 (lower is better)
- `lastCheck` — recent timestamp
- `recentMarkers` — list of detected drift types (empty if clean)

If `lastScore` is consistently above 0.3: your baseline definition needs tightening. Read `DRIFT_PREVENTION.md` for calibration guidance.

---

## The Game Theory Layer (Optional, Any Tier)

`CPR_V4_GAME_THEORY.md` explains *why* CPR works using signaling theory, repeated game analysis, and moral hazard frameworks.

You don't need it to use CPR. Read it if:
- You want to understand the mechanics well enough to adapt CPR to novel situations
- You're hitting edge cases the standard patterns don't cover
- You want to extend CPR to a new model or personality type

It won't change how you install CPR. It'll change how well you understand what you installed.

---

## Upgrade Path Summary

```
Tier 1 (Lite)
    ↓ (if drift still sneaks through)
Tier 2 (Core)
    ↓ (if long sessions lose voice after 100+ messages)
Tier 3 (Extended)
    ↓ (if you want to understand why it works)
Game Theory Layer (optional reading)
```

The most common mistake is starting at Tier 3. Start at Tier 1. Go up only when you have a specific problem to solve.
