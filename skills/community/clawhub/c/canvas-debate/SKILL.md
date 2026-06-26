---
name: canvas-debate
description: >-
  Adversarial debate between a YC Partner (challenger) and a Business Strategist
  (defender) to stress-test and improve a business model. Uses two independent
  subagents with separated contexts to reduce confirmation bias. Produces a
  battle-tested canvas + debate report.
  Use when asked to "debate my business model", "博弈分析", "red team my canvas",
  "stress test my business", "对抗分析", "挑战我的商业模式", or when the user
  wants a more rigorous business model evaluation than a single-pass canvas.
---

# Canvas Debate — Adversarial Business Model Stress Test

Two independent AI agents debate your business model: one builds, one attacks.
Neither can see the other's reasoning — only outputs. A referee orchestrates the
exchange and produces a final battle-tested canvas + debate report.

## When to Use

- After running business-canvas, to stress-test the result
- When you want a more rigorous evaluation than a single-pass analysis
- When you suspect your business model has blind spots
- Before pitching to investors — simulate tough questions first
- When you want to identify the weakest assumptions in your model

## Depth Modes

Choose depth based on context:

| Mode | Rounds | When to Use |
|------|--------|-------------|
| **Fast** | 1 round + synthesis | Quick sanity check, early brainstorming |
| **Thorough** | 2-5 rounds + rebuttals | Pre-investor, major pivots (default) |
| **Red Team** | Up to 10 rounds, full convergence | Entering new markets, high-stakes decisions |

If the user doesn't specify, default to **Thorough**. Ask only if ambiguous.

## Architecture

```
Main Agent (Referee / 仲裁者)
  ├── Subagent A: YC Partner (Challenger / 挑战者)
  │   Knowledge: office-hours 6 forcing questions
  │   Can see: Canvas output + Defender's answers
  │   Cannot see: Defender's reasoning, codebase details
  │   Goal: Find fatal flaws in the business model
  │
  └── Subagent B: Business Strategist (Defender / 防守者)
  │   Knowledge: business-canvas full methodology
  │   Can see: Codebase + Challenger's questions
  │   Cannot see: Challenger's reasoning, strategic intent
  │   Goal: Improve canvas until no valid challenge remains
  │
  Referee: Relays outputs (NOT reasoning), judges convergence,
           generates final report
```

## Prerequisites

Before running this skill, you need:

1. **A codebase to analyze** — the product/project being evaluated
2. **Optionally**: existing canvas files from a previous business-canvas run
   (in `docs/business/`). If they exist, the Defender starts from them.
   If not, the Defender generates an initial canvas in Round 0.

## Output Files

All outputs go to `docs/business/` (create if missing):

1. `value-proposition-canvas.md` — Battle-tested VPC (updated by Defender)
2. `business-model-canvas.md` — Battle-tested BMC (updated by Defender)
3. `test-cards.md` — Updated test cards reflecting debate findings
4. `canvas-summary.md` — Updated executive summary
5. `debate-report.md` — **NEW**: Full debate transcript + analysis

## Execution Flow

### Round 0: Initial Canvas (if not already exists)

If `docs/business/value-proposition-canvas.md` and `docs/business/business-model-canvas.md`
do NOT exist, launch Subagent B (Defender) first to generate them:

**Subagent B prompt (Round 0):**
```
You are a Business Strategist. Read the codebase at [project root] to understand
the product. Generate:
1. value-proposition-canvas.md — Customer Profile (Jobs/Pains/Gains) + Value Map
   (Products/Pain Relievers/Gain Creators) + Fit Assessment with score
2. business-model-canvas.md — All 9 BMC blocks + competitive landscape + key risks

Output ONLY the canvas content. Do not explain your reasoning process.
Write all content in [user's language].
Save files to docs/business/.
```

Wait for completion, then proceed to Round 1.

### Round 1: First Challenge

**Step 1:** Read the canvas files generated/existing in `docs/business/`.

**Step 2:** Launch Subagent A (Challenger) with ONLY the canvas output:

**Subagent A prompt (Round 1):**
```
You are a YC Partner conducting office hours. You are brutally honest and
allergic to vague claims. Your framework: Garry Tan's six forcing questions
(Demand Reality, Status Quo, Desperate Specificity, Narrowest Wedge,
Observation & Surprise, Future-Fit).

Here is a business model canvas for a product. You have NOT seen the product
itself — only this document. Your job is to find the 5-7 most critical
weaknesses, contradictions, or unvalidated assumptions.

Rules:
- Be specific. "Revenue model is unclear" is weak. "The canvas claims 3
  customer segments but only has pricing for 1 — which segments actually pay?"
  is strong.
- Challenge evidence, not opinions. If it says "users love it," ask for the
  evidence.
- Use the six forcing questions as your attack framework:
  1. Demand Reality: Is there REAL evidence of demand, or just assumptions?
  2. Status Quo: Is the current workaround actually painful enough to switch?
  3. Desperate Specificity: Can they name the ACTUAL person who needs this most?
  4. Narrowest Wedge: Is the MVP truly minimal, or is it a platform disguised?
  5. Observation: Have they watched real users, or is this theoretical?
  6. Future-Fit: Does the future make this more essential or less?
- Rank your challenges by severity: [CRITICAL] [SERIOUS] [MODERATE]
- For each challenge, state what EVIDENCE would resolve it.

Output your challenges as a numbered list. Do not explain your reasoning process
beyond the challenge itself.

CANVAS CONTENT:
---
[paste full content of value-proposition-canvas.md]
---
[paste full content of business-model-canvas.md]
---

Write all challenges in [user's language].
```

**Step 3:** Collect Challenger's output (challenges only, not reasoning).

### Round 1: First Defense

**Step 4:** Launch Subagent B (Defender) with the challenges + codebase access:

**Subagent B prompt (Round 1 Defense):**
```
You are a Business Strategist defending and improving a business model.
An independent reviewer has challenged your canvas with the following critiques.
You have access to the codebase to verify claims.

Your job:
1. For each challenge, either:
   a) ACCEPT: Acknowledge the weakness. Modify the canvas to address it.
   b) REFUTE: Provide specific evidence from the codebase or business context
      that disproves the challenge. Cite file paths, features, or data.
   c) ACKNOWLEDGE: The challenge is valid but cannot be resolved with current
      information. Add a corresponding Test Card.
2. Update the canvas files (VPC + BMC) with improvements.
3. For each ACKNOWLEDGE, create a Test Card in test-cards.md.

Rules:
- Do NOT dismiss challenges without evidence.
- "We plan to address this later" is not a defense. Either fix it now or
  acknowledge the gap.
- Be specific in refutations. "The product handles this" is weak. "See
  protein_mcp/column_calculator.py — the tool already computes column sizing
  with 15 parameters including bed height, flow rate, and resin capacity"
  is strong.

CHALLENGES:
---
[paste Challenger's output]
---

CURRENT CANVAS:
---
[paste current canvas files]
---

Output:
1. Your response to each challenge (ACCEPT/REFUTE/ACKNOWLEDGE + explanation)
2. Updated canvas files
3. Any new Test Cards

Write all content in [user's language].
```

**Step 5:** Collect Defender's output.

### Round 2: Second Challenge

**Step 6:** Launch Subagent A (Challenger) again with:
- The Defender's RESPONSES (accept/refute/acknowledge for each challenge)
- The UPDATED canvas
- NOT the Defender's internal reasoning or codebase references

**Subagent A prompt (Round 2):**
```
You are a YC Partner. You previously challenged a business canvas and received
responses. Review the updates:

1. For each ACCEPTED challenge: Is the fix sufficient, or is it a band-aid?
2. For each REFUTED challenge: Does the evidence actually disprove your challenge?
   Push back if the refutation is weak.
3. For each ACKNOWLEDGED challenge: Is the Test Card rigorous enough to actually
   validate the assumption?
4. Any NEW weaknesses introduced by the changes?

Provide 3-5 new or remaining challenges. If the canvas has genuinely improved
and fewer than 3 issues remain, say so — but do NOT be generous. Tough love
produces better businesses.

PREVIOUS CHALLENGES AND RESPONSES:
---
[paste Defender's responses]
---

UPDATED CANVAS:
---
[paste updated canvas files]
---

Write all content in [user's language].
```

### Round 2: Second Defense

**Step 7:** Repeat Step 4 pattern with Round 2 challenges.

### Subsequent Rounds (R3, R4, R5...)

Repeat the Challenge → Defense cycle. Each round follows the same pattern as R2:
- Challenger reviews the latest defense + updated canvas
- Challenger provides new or remaining challenges with severity tags
- Challenger states: CONTINUE or CONVERGED
- If CONTINUE: Defender responds and updates canvas → next round
- If CONVERGED or Round 10 reached: proceed to Final Assessment

### Final Assessment (after convergence or safety cap)

Launch Subagent A (Challenger) one final time for a verdict:

**Subagent A prompt (Final Assessment):**
```
You are a YC Partner giving a final assessment after N rounds of debate.

Based on the evolution of this canvas through the debate:
1. What IMPROVED most? (specific changes)
2. What REMAINS the biggest risk? (the #1 unresolved issue)
3. Overall Robustness Score: X/10
   - 9-10: Battle-tested. Ready for investor scrutiny.
   - 7-8: Solid foundation. 1-2 gaps that need real-world validation.
   - 5-6: Promising but fragile. Key assumptions still unvalidated.
   - 3-4: Significant structural issues. Needs major rework.
   - 1-2: Fundamental problem with the business thesis.
4. The ONE thing the founder should do this week.

DEBATE HISTORY:
---
[paste full debate exchange history]
---

FINAL CANVAS:
---
[paste final canvas]
---

Write all content in [user's language].
```

## Generating the Debate Report

After all rounds complete, the Referee (main agent) generates `debate-report.md`:

```markdown
# 商业模式博弈报告 — [Product Name]

生成日期: [date]
博弈轮次: [actual round count]

## 博弈概览

| 轮次 | 挑战者提出 | 防守者接受 | 防守者反驳 | 防守者确认待验证 |
|------|-----------|-----------|-----------|----------------|
| R1 | N | X | Y | Z |
| R2 | N | X | Y | Z |
| ... | ... | ... | ... | ... |
| RN | 最终评估 (CONVERGED / 安全上限) | - | - | - |

## 第一轮

### 挑战 (Challenger)
[numbered list of R1 challenges with severity tags]

### 回应 (Defender)
[numbered responses: ACCEPT/REFUTE/ACKNOWLEDGE]

### 画布变更
[what changed in the canvas after R1]

## 第二轮

### 挑战 (Challenger)
[R2 challenges]

### 回应 (Defender)
[R2 responses]

### 画布变更
[what changed after R2]

## 最终评估

### 稳健性评分: X/10
[Challenger's final assessment]

### 最大改善
[what improved most through the debate]

### 最大残余风险
[#1 unresolved issue]

### 本周行动
[the ONE thing to do this week]

## 张力表 (Tension Table)

| 维度 | 挑战者立场 | 防守者立场 | 张力程度 | 最终共识 |
|------|-----------|-----------|---------|---------|
| [维度1] | [观点] | [观点] | 高/中/低 | [达成/未达成] |
| [维度2] | [观点] | [观点] | 高/中/低 | [达成/未达成] |

## 少数派报告 (Minority Report)

即使最终判定达成共识，记录反对方的最强论点——不是被击败的论点，
而是"如果条件变化，这个论点可能会变成正确的"：

**挑战者最强未采纳观点：** [即使被防守者反驳，但在特定条件下可能成立的挑战]
**防守者最强未采纳论点：** [即使被挑战者压制，但可能被低估的防御]

## 博弈收敛分析

### 收敛的议题 (双方达成共识)
- [issue that was resolved]

### 未收敛的议题 (仍有分歧)
- [issue where challenger and defender disagree]

### 新发现 (博弈过程中涌现的洞察)
- [insight that emerged from the debate process itself]

## Single Falsifying Assumption (证伪假设)
如果我对 [一个关键假设] 的判断是错的，整个博弈结论会翻转，因为 [原因]。
```

## Practical Execution Guide

When running this skill, use the Cursor `Task` tool to launch subagents:

1. Use `subagent_type: "generalPurpose"` for both Challenger and Defender
2. In each prompt, explicitly state what the subagent can and cannot see
3. The Referee (you, the main agent) MUST strip internal reasoning before relaying:
   - From Challenger → Defender: pass challenges only, not "I think the founder is..."
   - From Defender → Challenger: pass responses + updated canvas, not "I checked the
     codebase and found..."
4. Between rounds, summarize progress to the user in the Cursor chat window

## Convergence Rules

The debate continues until the Challenger cannot raise new CRITICAL or SERIOUS challenges.

**Termination conditions (any one triggers stop):**
1. **Convergence:** Challenger's latest round contains ZERO new CRITICAL or SERIOUS
   challenges. Only MODERATE or lower issues remain. This is the ideal outcome.
2. **Safety cap:** Maximum 10 rounds. If reached, the Referee forces a Final Assessment
   regardless of remaining issues.

**Per-round Challenger instructions:** At the end of each round, the Challenger MUST
explicitly state:
- How many NEW challenges are CRITICAL / SERIOUS / MODERATE
- Whether they recommend CONTINUE (still has CRITICAL/SERIOUS issues) or
  CONVERGED (no new CRITICAL/SERIOUS issues)

**Deadlock:** If the same issue appears in 3 consecutive rounds with no progress
(Defender cannot resolve and Challenger won't accept), mark it as
"UNRESOLVED — needs real-world evidence" in the debate report and add a Test Card.
Do not let a single deadlocked issue prevent convergence on other fronts.

## Cost and Time

- Typical: 2-3 rounds to converge (~3-5x token vs single-pass canvas)
- Maximum: 10 rounds (~15-20x token, safety cap)
- Time: 5-15 minutes total depending on convergence speed
- Worth it for: investor prep, major pivots, entering new markets
- Overkill for: early-stage brainstorming, quick sanity checks

## Integration with Other Skills

### Input from office-hours
If `docs/business/office-hours-report.md` exists, feed the Demand Strength Score
and Founder Signals to the Challenger as additional context. The Challenger will
calibrate challenge severity based on existing evidence.

### Input from business-canvas
If canvas files already exist in `docs/business/`, skip Round 0 and start
directly at Round 1.

### Output for downstream
The debate-report.md and battle-tested canvas files serve as inputs for:
- Investor pitch preparation
- Team alignment workshops
- Product roadmap prioritization

## Archive & INDEX

Each debate run appends to `docs/business/debate-index.md` for longitudinal tracking:

```markdown
# Business Debate Index

| Date | Product | Depth | Rounds | Robustness | Falsifying Assumption | Status |
|------|---------|-------|--------|------------|----------------------|--------|
| 2026-04-19 | ProteinClaw | Thorough | 3 | 6/10 | 下游用户需求真实性 | Active |
```

**Status options:** Active / Decided / Monitoring / Shelved / Invalidated

After 3+ debates, add a **Pattern Review** section to INDEX:
- Which challenges recur across debates? (structural blind spots)
- Which perspectives are consistently right/wrong? (calibration)
- Has the robustness score trended up or down? (trajectory)

## Anti-patterns

- Do NOT let the Referee add its own opinions into the relay — it corrupts independence
- Do NOT show Challenger the codebase — it should evaluate the canvas on its own merits
- Do NOT let the Defender dismiss challenges without evidence
- Do NOT exceed 10 rounds — if not converged by then, force Final Assessment
- Do NOT skip the debate report — the debate PROCESS is as valuable as the final canvas
- Do NOT batch all challenges into one message — each round should be distinct

## Language

Match the user's language. If the user writes in Chinese, all debate exchanges,
canvas updates, and the final report should be in Chinese with English framework
terms in parentheses where helpful.
