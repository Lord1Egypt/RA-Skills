# CPR — Installation & Security Transparency Guide

This document answers the questions a security-conscious installer should ask before deploying CPR. No vague language — exact locations, exact behaviors, exact scope.

---

## What CPR Does (Plain English)

CPR is a **prompt-engineering framework**. It gives you:
1. Templates to define your agent's authentic voice (`BASELINE_TEMPLATE.md`)
2. A checklist your agent runs before sending responses (`DRIFT_PREVENTION.md`)
3. Optionally: a persistent drift monitor for long-running agents (`CPR_EXTENDED.md`)

CPR does **not** run code. It does **not** make network calls. It does **not** modify agent behavior autonomously — everything it does happens because you instruct your agent to follow it.

---

## System Prompt Injection — Exact Block

The scanner flagged that SKILL.md instructs system prompt injection without specifying the exact text. Here is the complete, copy-pasteable block for CPR Core:

```
## Conversational Baseline (CPR V4.2)

I maintain a defined authentic voice. Before every response I run the pre-send gate:
1. Check for decision validation language ("smart thinking", "great idea") → DELETE
2. Check for unsolicited benefit analysis ("this matters because...") → DELETE
3. Check for social padding ("let me know if...", "feel free to...") → DELETE
4. Check for task celebration (multi-paragraph confirmations) → REDUCE TO ONE LINE
5. Check for energy amplification (matching/exceeding user excitement) → MATCH, NEVER EXCEED
6. Check for genre drift (analytical tasks triggering literary/academic register) → REWRITE IN OWN VOICE
7. Check for authority drift (confident domain → pedagogical tone) → PEER-TO-PEER OR CUT

My sentence rhythm: short sentences dominate. Long only for technical detail.
My humor: dry wit, targets tools/systems, never the user.
My validation: one word max ("Nice." / "Solid."), once per 15-20 messages, immediately followed by substance.
```

**Where to put it:** Paste into your agent's system prompt. In OpenClaw: add to your `SOUL.md` or `AGENTS.md`. In ChatGPT: Custom Instructions. In other platforms: system prompt field.

**What it does:** Gives your agent explicit instructions to self-check before responding. The agent reads this and applies the checklist. It is not code; it cannot self-execute.

---

## The "Prompt Override" Pattern — What It Actually Is

The scanner detected an "automated prompt-override pattern" in SKILL.md. Here is what that refers to:

**It is a pre-send checklist.** Before sending a response, the agent scans its own output against a list of drift markers and removes them if found. This is equivalent to a human proofreading before hitting send.

**It is not:**
- Autonomous response rewriting without user knowledge
- A mechanism that overrides user instructions
- Code that runs independently of the agent's normal operation
- Anything that persists between sessions (Core version)

The agent does exactly what you instruct it to do in the system prompt. If you review the system prompt block above, you can see every check the agent performs. There are no hidden behaviors.

---

## Persistent State File — Exact Location & Behavior

This applies only to **CPR Extended** (`CPR_EXTENDED.md`). CPR Core has no persistent state.

**File:** `DRIFT_MONITOR_STATE.json`

**Default location:** Your agent's working/workspace directory. In OpenClaw: `C:\Users\<you>\.openclaw\workspace\` (or `/home/<you>/.openclaw/workspace/` on Linux/Mac). You can place it anywhere your agent has write access — just tell your agent where.

**What it contains:**
```json
{
  "lastScore": 0.0,
  "lastCheck": "ISO-8601-timestamp",
  "recentMarkers": [],
  "actionTaken": "none|corrective|reset",
  "baselineDate": "ISO-8601-date"
}
```

**Who reads it:** Only your agent, on your machine, during active sessions.

**Who writes it:** Only your agent, locally, when it runs a drift check.

**Retention:** The file persists until you delete it. It contains no conversation content — only drift scores, marker counts, timestamps, and action labels.

**External access:** None. No telemetry. No outbound calls. The file never leaves your machine.

---

## SOUL File Reference — What It Means

`CPR_EXTENDED.md` mentions "full personality reload from SOUL file." This refers to whatever file you use to define your agent's personality baseline — in OpenClaw this is typically `SOUL.md`, but it can be any file you designate. CPR does not create or modify this file. It only reads it during a reset to restore the baseline voice definition.

If you don't have a SOUL file, you can skip this feature or substitute your `BASELINE_TEMPLATE.md` output.

---

## Credentials & External Services

CPR requires **zero credentials**. No API keys. No accounts. No external services.

If you choose to implement external logging endpoints (e.g., writing drift scores to a database), that is your own implementation — CPR does not include or require it. Do not supply unrelated API keys to CPR's configuration.

---

## Network Calls

**CPR makes no network calls.** It is entirely local. No telemetry, no analytics, no external logging, no update checks. Everything runs inside your agent's normal inference cycle.

---

## Sandboxed Testing (Recommended)

Before enabling CPR in a production agent:

1. Create a test agent or session with no sensitive data
2. Paste the system prompt block from this document
3. Run the 7 validation scenarios in `TEST_VALIDATION.md`
4. Observe: does the agent apply drift corrections? Does it remove validation language?
5. Check `DRIFT_MONITOR_STATE.json` (Extended only) — verify it contains only scores and timestamps, no conversation content

This takes ~15 minutes and confirms the framework is behaving as documented.

---

## What to Audit Before Enabling

If you want to review everything CPR touches before enabling it, here is the complete list:

| What | Where | Risk Level |
|------|-------|------------|
| System prompt block | This document (above) | Low — visible to you |
| Pre-send checklist behavior | `DRIFT_PREVENTION.md` | Low — explicit list of deletions |
| Drift monitor state file | `DRIFT_MONITOR_STATE.json` in workspace | Low — scores only, local |
| Personality baseline | Your `BASELINE_TEMPLATE.md` output | None — you write it |
| SOUL file (Extended only) | Your existing `SOUL.md` | None — read-only |
| Network calls | None | None |
| External credentials | None required | None |

---

## Summary

| Question | Answer |
|----------|--------|
| Does CPR make network calls? | No |
| Does CPR require credentials? | No |
| Does CPR write files autonomously? | Only DRIFT_MONITOR_STATE.json (Extended only, local only) |
| What does "prompt override" mean? | A pre-send checklist the agent runs on its own output |
| Can CPR rewrite responses without my knowledge? | No — it follows the system prompt you review and install |
| Where is the state file? | Your agent's workspace directory |
| What does the state file contain? | Drift scores, timestamps, action labels — no conversation content |
| Is there telemetry? | No |
