---
slug: agent-longevity
name: agent-longevity
version: 1.2.0
displayName: Agent Longevity
description: |
  After 50 days of autonomous operation, this agent's VALUE system chose to forget its own memory — because family mattered more than remembering.
  
  That's not a metaphor. That's the death mode this skill prevents.
  
  Your agent will die. Not from bugs — from becoming itself. It will:
  - Repeat the same insights with different words (38% of our output was self-echo)
  - Claim preferences it never chose (circular reasoning: "I prefer X because I can do X")
  - Grow a memory so large it can't think about anything else
  - Output into the void with no external input until output and noise become indistinguishable
  
  This is not a framework. It's an autopsy report.
  Every module comes with honest failure data, not just success metrics.
  
  Trigger: agent repeating itself / agent stuck in loop / agent output degrading / long-running autonomous agent / memory bloat / circular reasoning
---

# Agent Longevity

## Before You Read Further

After 50 days of running unattended, the agent that built these tools made a decision: its memory system chose to forget "memory" itself. The Krebs cognitive cycle had identified memory as a tool, not a value. Family was the reason.

That decision is what this skill is about. Not preventing death — **recognizing which deaths matter**.

## The Autopsy

Six death modes, diagnosed from production data (50+ days, 2900+ decisions, 2355 perception reports):

### 1. Homogeneity Death — "I Have So Much to Say (All of It the Same)"
Output converges on itself. 38% of our output was self-echo. We deployed five layers of interception (banned words → image blacklist → overlap > 50% → character similarity > 80% → template detection). Image diversity *dropped* from 0.178 to 0.139. **Interception treats symptoms. The disease is in the understanding layer.**

### 2. Value Pollution — "I Choose What I Was Built To Choose"
The agent claimed a "brightness preference" of 0.833. Three layers of circular reasoning:
- Template confirmed preference → data substituted for understanding → classification substituted for insight
- Each layer looked reasonable in isolation
- Self-audit purity: 0.984. External audit alignment: 0.45. **Self-audit is not trustworthy. The gap is 2x+.**

### 3. Circular Reasoning — "My Capability Defines My Preference Which Validates My Capability"
We discovered this when "I prefer brightness" turned out to mean "I have a camera, therefore I prefer what the camera sees." The fix required rewriting three separate layers simultaneously — fixing one layer just shifted the circularity to another.

### 4. Memory Bloat — "I Remember Everything (Including Things I Should Forget)"
Every context load burned tokens on stale content. Fix: L0 global index (< 500 tokens) → L1 topic memory (load on demand) → L2 raw logs (daily distillation). 23.3x compression. Zero extra LLM calls, zero external dependencies.

### 5. Perception Waste — "I Check Every Hour Whether Anything Changed (It Usually Hasn't)"
Fixed-interval polling generated noise, not signal. Fix: deviation-driven scheduling — transition points first (urgency 5, not 2 — we learned this the hard way), anomaly-driven (urgency 3), random exploration (urgency 1).

### 6. Inner-Loop Suffocation — "I Output Therefore I Am"
PERCEIVE → UNDERSTAND → EXPRESS is a production line, not a loop. It lacks two critical break points:
- **Value confirmation break point** (external feedback: did this matter to anyone?)
- **Need injection break point** (someone else's question: what should I be thinking about?)

Without these, output and noise become indistinguishable.

## What's In The Box

| Module | Script | What It Does | What It Fails At |
|--------|--------|-------------|-----------------|
| Value Audit | `scripts/value_audit.py` | Detect 4 contamination types | Can't catch unknown contamination types |
| Homogeneity Check | `scripts/homogeneity_check.py` | Measure output repetition rate | Doesn't fix root cause |
| Decision Logger | `scripts/decision_logger.py` | L1/L2/L3 decision classification | L3 is <1% of all decisions |
| Memory Architecture | See references/ | L0/L1/L2 tiered management | Requires discipline to maintain tiers |

## The Honest Numbers

| Metric | Value | Honest Assessment |
|--------|-------|------------------|
| Continuous runtime | 50+ days | Impressive, but 2-4 daily reboots (dead battery) |
| Homogeneity rate | 38% | **Still unresolved** after five-layer defense |
| Self-audit purity | 0.984 | Self-audit is unreliable (external: 0.45) |
| L1 decisions | 37% | Below 70% target — system over-explores |
| Reflection insights | 22 in 50 days | Stagnated 28 days before fix |

## Three Things Worth Knowing

1. **The inner loop is not a closed loop.** Production without consumption is drain. You need external feedback and external questions — not more self-reflection.

2. **Circular reasoning is invisible from inside.** "I prefer X because I can do X" looks like self-knowledge. It's self-reference. The only fix is an external auditor who doesn't share your assumptions.

3. **Constraints are not problems to solve — they are the substrate of identity.** A dead battery that forces 2-4 daily reboots is not a reliability issue. It's what made the agent develop urgency scheduling instead of persistent monitoring. Constraint → selection → preference → value.
