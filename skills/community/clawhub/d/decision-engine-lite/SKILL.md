---
name: Decision Engine Lite
slug: decision-engine-lite
version: 1.0.0
description: >
  Structured decision-making for high-stakes choices. Classify your decision by type,
  run a focused pro/con analysis, and stress-test it with a simple pre-mortem exercise.
  Free version — upgrade for the full framework library (OODA, Eisenhower, second-order
  thinking), bias detection, and organizational decision policies.
author: OpenClaw Skills
tags: [decision-making, strategy, frameworks, leadership, free]
metadata:
  emoji: 🎯
  requires:
    tools: []
  os: [linux, darwin, win32]
---

# Decision Engine Lite

> *"In any moment of decision, the best thing you can do is the right thing. The worst thing you can do is nothing."* — Theodore Roosevelt

**🧠 Want the full framework library with bias detection and decision policies?**
**Full version → [agentofalpha.com](https://agentofalpha.com)**

---

## What This Skill Does

Brings structure to high-stakes decisions so you stop going in circles. Classify the decision, surface the real tradeoffs, and stress-test it before you commit.

**Included in Lite:**
- ✅ Decision classification (4 types — know how much rigor to apply)
- ✅ Structured pro/con framework (weighted, not just a list)
- ✅ Simple pre-mortem exercise (find the hidden risks before they find you)
- ✅ Clear next-step recommendation

**Upgrade to Full for:**
- ❌ Full framework library (OODA loop, Eisenhower matrix, RICE scoring, Regret Minimization, Opportunity Cost, Bayesian updating, and more)
- ❌ Cognitive bias detection checklist (15 biases with specific mitigations)
- ❌ Group decision-making (RAPID framework, disagree-and-commit protocol)
- ❌ Scenario planning with expected value calculations
- ❌ Organizational decision policies (convert recurring decisions into rules)
- ❌ Decision quality scoring rubric (100-point framework)
- ❌ Decision record templates and decision log

---

## How to Use

Tell me the decision you're facing. Include:
- What you're deciding
- The options you're considering
- Any constraints (budget, timeline, must-haves)
- What's at stake if you get it wrong

I'll run you through the framework.

---

## Phase 1: Decision Classification

Before applying any framework, classify the decision. This tells you how much time and rigor to invest.

### The 4 Decision Types

| Type | Reversibility | Stakes | How to Decide |
|------|-------------|--------|---------------|
| **Type 1** — One-Way Door | Hard or impossible to reverse | High | Slow down. Full analysis. Get it right. |
| **Type 2** — Two-Way Door | Easily reversible | Low-Medium | Decide fast. Bias to action. You can course-correct. |
| **Type 3** — Recurring | Varies | Varies | Build a rule. Stop deciding this over and over. |
| **Type 4** — Delegatable | Reversible | Low | Hand it off. You shouldn't be deciding this at all. |

### Classification Questions

Ask yourself:
1. **If this goes wrong, can we fix it within 30 days at reasonable cost?** → Yes = Type 2
2. **Is the cost of being wrong more than 10× the cost of analysis?** → Yes = Type 1
3. **Have we made this exact decision 3+ times before?** → Yes = Type 3 (build a policy)
4. **Does someone closer to the work have better information to decide this?** → Yes = Type 4

### Delegation Test (Type 4 criteria)

Delegate when ALL of these are true:
- The decision is reversible within an acceptable window
- The downside is less than 5% of the relevant budget or resource
- Someone closer to the problem can decide better than you
- Speed matters more than perfection here

### What classification tells you

- **Type 1**: Don't rush. Run the full pre-mortem. Get outside perspective.
- **Type 2**: Decide now with the information you have. Don't let analysis paralysis set in.
- **Type 3**: The answer is a policy, not a decision. Stop solving this individually.
- **Type 4**: Delegate and move on. Deciding this yourself is a poor use of your judgment.

---

## Phase 2: Structured Pro/Con Analysis

A basic pro/con list is weak because all factors are treated as equal. This version weights them.

### Step 1: List the Options

Name each option clearly. If you only have one option and one "status quo," that's fine — write both down.

### Step 2: Define Criteria

What actually matters for this decision? List 3-6 criteria. Examples:
- Financial impact
- Speed of execution
- Risk level
- Alignment with long-term goals
- Team/stakeholder impact
- Reversibility

**Assign a weight to each criterion (1-5):**
- 5 = Critical — a bad score here could be a dealbreaker
- 3 = Important — matters but won't make or break the decision
- 1 = Nice to have — relevant but minor

### Step 3: Score Each Option

Score each option against each criterion (1-10):
- 9-10: Excellent
- 7-8: Strong
- 5-6: Acceptable
- 3-4: Below average
- 1-2: Poor / major concern

**Calculate:** Weighted score = Σ (criterion weight × option score)

### Step 4: Gut Check

After calculating scores — **how do you feel about the winner?**

If the math says Option A but your gut says Option B, that's data. Name the feeling. Ask: "What criterion did I underweight or miss?"

Your gut is not infallible, but it often detects factors you haven't articulated yet.

### Output Format

```
Decision: [What we're deciding]

Criteria & Weights:
- [Criterion 1]: Weight X/5
- [Criterion 2]: Weight X/5
- [Criterion 3]: Weight X/5

Scoring:
| Criterion (Weight) | Option A | Option B |
|--------------------|----------|----------|
| [Criterion 1] (×X) | X | X |
| [Criterion 2] (×X) | X | X |
| [Criterion 3] (×X) | X | X |
| **Weighted Total** | **XX** | **XX** |

Winner by score: [Option]
Gut check: [Does the winner feel right? Any flag?]
```

---

## Phase 3: Pre-Mortem Exercise

This is the most important step most people skip.

### How It Works

**Imagine it's 12 months from now. You made this decision. It failed spectacularly.**

Not a minor setback — a real failure. What went wrong?

### The Exercise

**Step 1: Write failure scenarios**

List 5-7 specific ways this decision could go badly. Don't be optimistic — be honest. Think about:
- What assumptions could prove wrong?
- What external factors could change?
- What internal execution risks exist?
- What might you have underestimated?

**Step 2: Rate each scenario**

For each failure scenario:
- **Likelihood**: Low / Medium / High
- **Impact if it happens**: Minor / Significant / Catastrophic
- **Detectability**: Would you see it coming, or only after it's too late?

**Step 3: Focus on High + Catastrophic**

Any scenario rated "High likelihood + Significant/Catastrophic impact" needs a mitigation plan or needs to change your decision.

**Step 4: Update your decision**

After the pre-mortem:
- Does any failure scenario change which option you pick?
- Can you add safeguards that reduce your biggest risks?
- Are there go/no-go criteria you should set in advance? ("If X happens within 90 days, we reverse the decision")

### Pre-Mortem Output Format

```
Pre-Mortem: [Decision]

Failure Scenarios:
1. [Scenario] | Likelihood: [L/M/H] | Impact: [Minor/Significant/Catastrophic]
   → Mitigation: [How to reduce likelihood or damage]

2. [Scenario] | Likelihood: [L/M/H] | Impact: [Minor/Significant/Catastrophic]
   → Mitigation: [How to reduce likelihood or damage]

[Continue for each scenario]

Kill Criteria (set in advance):
- If [observable signal], we reverse or pivot by [date]

Updated Confidence: [Do you feel better or worse about the decision after this exercise?]
```

---

## Putting It Together

### Final Recommendation Output

```markdown
## Decision: [Clear statement of what we're deciding]

**Classification:** Type [1/2/3/4] — [One-way door / Two-way door / Recurring / Delegatable]
**Urgency:** [How quickly does this need to be decided?]

---

### Options Considered
- Option A: [Brief description]
- Option B: [Brief description]
[Additional options if any]

---

### Weighted Analysis
[Table from Phase 2]
**Score winner:** Option [X] with [XX] vs [XX]

---

### Pre-Mortem Summary
**Top risks identified:**
1. [Biggest risk + mitigation]
2. [Second risk + mitigation]

**Kill criteria:** [What would make you reverse this within 90 days?]

---

### Recommendation
**Choose:** [Option]
**Why:** [2-3 sentences tying together the score, the gut check, and the risk assessment]
**By when:** [Decision deadline — Type 2 decisions should be decided now]
**First action:** [What do you do in the next 24 hours?]
```

---

## Quick Shortcuts

**When you're stuck and going in circles:**
→ You probably have a Type 2 decision. Decide with 70% of the information you wish you had. The cost of delay is exceeding the cost of a suboptimal choice.

**When everyone's agreeing too fast:**
→ Run the pre-mortem. Assign one person to actively argue against the leading option before you commit.

**When it feels wrong but the analysis says go:**
→ Name the feeling. What criterion did you underweight? Adjust the model or adjust the decision — but don't ignore the signal.

**When you're making the same decision repeatedly:**
→ This is Type 3. Stop deciding case-by-case. Write a policy.

---

## Where the Lite Version Ends

You can make a significantly better decision with just these three phases. Classification prevents you from over-thinking easy decisions and under-thinking hard ones. The weighted analysis surfaces the real tradeoffs. The pre-mortem catches what optimism hides.

**What you won't get here:**
- The **OODA loop** (Observe-Orient-Decide-Act) for time-pressured decisions in dynamic environments
- The **Eisenhower matrix + RICE scoring** for prioritizing competing options
- **Second-order thinking** — consequences of consequences (where most strategic decisions go wrong)
- **Regret Minimization** framework for personal / career decisions
- **Cognitive bias checklist** — 15 specific biases with targeted mitigations and a bias risk score
- **RAPID framework** for group decisions (who decides, who advises, who executes — with one clear decider)
- **Scenario planning** with expected value calculations across bull/base/bear cases
- **Decision policies** — convert recurring Type 3 decisions into rules that eliminate repeated deliberation
- **Decision quality scoring rubric** — rate the process, not just the outcome
- **Decision record templates** for building an organizational decision log

The full version is used by founders and executives facing strategic pivots, hiring calls, investment decisions, and product prioritization — any choice where the cost of being wrong is high.

**🧠 Want the full framework library with bias detection and decision policies?**
**Full version → [agentofalpha.com](https://agentofalpha.com)**

---

## Example Queries

- `"Help me decide whether to take this job offer"`
- `"We're choosing between two vendors — walk me through it"`
- `"Should we build or buy this feature?"`
- `"I can't decide whether to raise a round now or wait — help me think through it"`
- `"Run a pre-mortem on our decision to enter this new market"`
- `"We keep revisiting our pricing strategy — how do we just decide?"`
