# Five Knives Framework

## Table of Contents

1. [Overview](#overview)
2. [Knife 1: Cut Assumptions](#knife-1-cut-assumptions)
3. [Knife 2: Cut to Constraints](#knife-2-cut-to-constraints)
4. [Knife 3: Cut the Goal](#knife-3-cut-the-goal)
5. [Knife 4: Reconstruct the Path](#knife-4-reconstruct-the-path)
6. [Knife 5: Validate the Loop](#knife-5-validate-the-loop)
7. [Quick Reference](#quick-reference)

---

## Overview

The Five Knives Framework is the rapid-action first-principles framework. It's designed for situations requiring fast, decisive first-principles analysis.

**Philosophy**:
> First-principles is not a ceremony. It's a knife. Use it to cut through noise.

**Core Pattern**:
```
Cut Assumptions → Cut to Constraints → Cut the Goal → Reconstruct Path → Validate Loop
```

**Time to execute**: 15-60 minutes (depending on complexity)

**When to use**:
- Rapid decision-making
- Quick problem diagnosis
- Emergency response
- Time-constrained analysis
- First-pass evaluation

---

## Knife 1: Cut Assumptions

**Objective**: Identify and eliminate inherited assumptions.

**Time**: 5-10 minutes

### The Cutting Process

**Step 1: List All Assumptions**
- Write down everything you're assuming
- Don't filter initially — list everything
- Include explicit and implicit assumptions

**Step 2: Classify by Source**
- Inherited from industry: "Industry standard is..."
- Inherited from organization: "We've always done..."
- Inherited from personal experience: "Based on my experience..."
- Linguistic: "Everyone says..."

**Step 3: Apply the Knife**
For each assumption, ask:
1. Is this true? (Evidence?)
2. Is this necessary? (Can we proceed without it?)
3. Is this a constraint? (Or just a preference?)

**Step 4: Decision Matrix**

| Assumption | True? | Necessary? | Action |
|-----------|-------|------------|--------|
| "Customers want X" | ? | ? | Test with real customers |
| "Competitors are doing Y" | ✓ | ✗ | Ignore (not necessary) |
| "We need Z to succeed" | ✗ | ✗ | Eliminate |

**Step 5: Cut**
- Eliminate false assumptions
- Eliminate unnecessary assumptions
- Keep only true, necessary assumptions

### Quick Questions

- "What would I assume if I had no experience in this domain?"
- "What would an alien think about this?"
- "What assumptions do I take for granted?"

### Output
List of verified assumptions (typically 3-5 core assumptions)

---

## Knife 2: Cut to Constraints

**Objective**: Identify the hard constraints — what cannot be violated.

**Time**: 5-10 minutes

### The Cutting Process

**Step 1: Distinguish Constraints vs. Preferences**
- **Constraint**: Cannot be violated without system failure
- **Preference**: Would be nice to have, but not essential

**Step 2: Identify Constraint Types**
- **Physical**: Laws of nature (physics, biology)
- **Logical**: Laws of logic (contradiction, causality)
- **Economic**: Resource constraints (time, money, energy)
- **Human**: Incentive constraints (behavior, motivation)
- **Institutional**: Regulatory, policy constraints

**Step 3: Test for Hardness**
For each constraint, ask:
1. What happens if we violate this?
2. Is the consequence catastrophic or inconvenient?
3. Is there any way to bypass this constraint?

**Step 4: Constraint Validation Matrix**

| Constraint | Type | Test Result | Status |
|-----------|------|-------------|--------|
| "Energy conserved" | Physical | Violation impossible | ✗ Hard |
| "Need $10M funding" | Economic | Can bootstrap | ✓ Soft |
| "Must hire 50 people" | Human | Can automate | ✓ Soft |

**Step 5: Cut to Core**
- Keep only hard constraints
- Soft constraints become preferences or goals

### Quick Questions

- "What would make this system impossible?"
- "What cannot be violated?"
- "What are the deal-breakers?"

### Output
List of hard constraints (typically 2-5 core constraints)

---

## Knife 3: Cut the Goal

**Objective**: Refine and redefine the goal to ensure it's the right goal.

**Time**: 5-10 minutes

### The Cutting Process

**Step 1: Articulate the Current Goal**
- What are we trying to achieve?
- Why are we trying to achieve this?
- What does success look like?

**Step 2: Question the Goal**
- Is this the right goal?
- What's the ultimate objective behind this goal?
- Could we achieve the ultimate objective a different way?

**Step 3: Apply the "Five Whys"**
- Why do we want X?
  - Because we need Y
    - Why do we need Y?
      - Because we want Z
        - Why do we want Z?
          - Ultimate objective revealed

**Step 4: Goal Redefinition**
From: "Increase market share by 20%"
To: "Profitably serve more customers better" (ultimate objective)

**Step 5: Test the New Goal**
- Is it measurable?
- Is it achievable within constraints?
- Does it align with ultimate objectives?

### Quick Questions

- "Why are we doing this?"
- "What's the real problem?"
- "What's the end state we want?"

### Output
Refined, clarified goal (single sentence)

---

## Knife 4: Reconstruct the Path

**Objective**: Build the optimal path from constraints to goal.

**Time**: 10-20 minutes

### The Reconstruction Process

**Step 1: Start from Constraints**
- Given the hard constraints (Knife 2)
- And the verified assumptions (Knife 1)
- What are the available paths?

**Step 2: Start from Goal (Reverse)**
- Given the goal (Knife 3)
- What must be true immediately before achieving the goal?
- What must be true before that?
- Continue until you reach current state

**Step 3: Find the Intersection**
- Forward (from constraints): What can we do?
- Backward (from goal): What do we need to do?
- Intersection: Optimal path

**Step 4: Path Compression**
- Are there unnecessary steps?
- Can we compress multiple steps into one?
- Can we remove intermediaries?

**Step 5: Energy Optimization**
- Which path has minimum energy (time, cost, friction)?
- Are there bottlenecks?
- How can we reduce friction?

### Reconstruction Template

```
Given:
  - Constraints: [C1, C2, C3]
  - Goal: [G]
  - Current state: [S]

Path:
  S → [A] → [B] → [C] → G

Optimization:
  - Remove [B] (unnecessary)
  - Combine [A] and [C] (parallelizable)
  - Result: S → [A+C] → G
```

### Quick Questions

- "What's the shortest path from here to the goal?"
- "What's the lowest-cost path?"
- "What are we doing that's not necessary?"

### Output
Actionable path (3-7 steps)

---

## Knife 5: Validate the Loop

**Objective**: Ensure the reconstructed path is valid and learnable.

**Time**: 5-10 minutes

### The Validation Process

**Step 1: Logic Check**
- Does the path logically lead from constraints to goal?
- Are there contradictions?
- Are there circular dependencies?

**Step 2: Feasibility Check**
- Is each step achievable?
- What resources are needed?
- What are the risks?

**Step 3: Testability Check**
- How will we know if each step succeeds?
- What are the success metrics?
- What are the failure modes?

**Step 4: Feedback Loop Design**
- How will we measure outcomes?
- How quickly can we iterate?
- What will we learn if we fail?

**Step 5: Go/No-Go Decision**
- Confidence level (0-100%)
- Critical risks
- Mitigation strategies
- Go or No-Go?

### Validation Checklist

- [ ] Path is logically sound
- [ ] Each step is feasible
- [ ] Success is measurable
- [ ] Feedback loop exists
- [ ] Risks are identified
- [ ] Mitigation planned

### Quick Questions

- "What would make this fail?"
- "How will we know if we're on track?"
- "What's the worst case?"

### Output
Validated action plan with confidence level and risk assessment

---

## Quick Reference

### Five Knives in 5 Minutes

| Knife | Action | Question | Output |
|-------|--------|----------|--------|
| 1. Cut Assumptions | List, classify, eliminate | "Is this true and necessary?" | 3-5 core assumptions |
| 2. Cut to Constraints | Identify hard constraints | "What cannot be violated?" | 2-5 hard constraints |
| 3. Cut the Goal | Refine with "Five Whys" | "What's the real objective?" | 1 clarified goal |
| 4. Reconstruct Path | Build forward + backward | "What's the optimal path?" | 3-7 step path |
| 5. Validate Loop | Check logic, feasibility, testability | "What could go wrong?" | Action plan + confidence |

### Execution Time

- **Simple problem**: 15-20 minutes
- **Medium problem**: 30-45 minutes
- **Complex problem**: 60+ minutes

### When to Use Five Knives

✅ **Use when**:
- Rapid decision needed
- Emergency response
- First-pass evaluation
- Quick diagnosis
- Time-constrained analysis

❌ **Don't use when**:
- Deep, comprehensive analysis needed
- Extremely complex systems
- High-stakes, long-term decisions
- When you have time for full framework

### Relationship to Full Framework

Five Knives = Rapid subset of full 14-layer framework

- Knife 1 ≈ Layer 1 (Assumption Extraction)
- Knife 2 ≈ Layer 2 (Verification) + Layer 5 (Math: Constraints)
- Knife 3 ≈ Layer 4 (Reconstruction: Reverse Engineering)
- Knife 4 ≈ Layer 4 (Reconstruction: Multiple Methods)
- Knife 5 ≈ Layer 8 (Practice Loop: Validation)

Use Five Knives for speed; use full framework for depth.

---

## Example: Product Launch

### Knife 1: Cut Assumptions

**Initial assumptions**:
- Need $100K marketing budget
- Competitors are outspending us
- Customers prefer established brands
- Need 6-month launch timeline

**After cutting**:
- Market need is real (verified)
- Can launch with $10K (bootstrap marketing)
- Competitors don't matter if value proposition is clear (not a constraint)
- Timeline can be 2 months with MVP approach

### Knife 2: Cut to Constraints

**Identified constraints**:
- Must solve real problem (verified)
- Must be economically viable (positive ROI)
- Must be legally compliant (regulatory)

**Status**: 3 hard constraints, all manageable

### Knife 3: Cut the Goal

**Initial goal**: "Launch product in 6 months with $100K marketing"

**After "Five Whys"**:
- Why launch in 6 months? Because we think we need to be first
- Why be first? To capture market share
- Why capture market share? To be profitable
- Why be profitable? To create sustainable business

**Refined goal**: "Create a sustainable, profitable business solving this problem"

### Knife 4: Reconstruct Path

**Forward (from constraints)**:
- Can build MVP in 2 months
- Can bootstrap marketing ($10K)
- Can iterate based on feedback

**Backward (from goal)**:
- Need paying customers
- Need product that solves problem
- Need to reach target customers
- Need to validate market

**Optimal path**:
1. Build MVP (2 months, $5K)
2. Beta test with 50 users (1 month, $2K)
3. Launch to early adopters (1 month, $3K)
4. Gather feedback, iterate (ongoing)

### Knife 5: Validate Loop

**Logic check**: Path leads to sustainable business ✓
**Feasibility**: Each step achievable with resources ✓
**Testability**: Clear metrics at each step ✓
**Feedback loop**: Rapid iteration based on user feedback ✓

**Decision**: Go with 85% confidence

---

## Mastery Indicators

You've mastered the Five Knives when:

1. **Speed**: Can complete all 5 knives in <15 minutes for simple problems
2. **Precision**: Identify the right assumptions and constraints instinctively
3. **Insight**: Regularly find non-obvious paths
4. **Action**: Always produce actionable output
5. **Learning**: Each application improves your intuition

---

## The Ultimate Insight

> Five Knives = First-principles for the impatient

It's not a replacement for deep analysis. It's the tool for when you need to move fast without sacrificing clarity.

---

**Cut through noise. Find the signal. Act decisively.**
