# Analysis of Competing Hypotheses (ACH)

## Purpose

ACH is a structured analytical technique designed to eliminate confirmation bias. Instead of building a case for the most obvious conclusion, ACH forces the analyst to systematically test all plausible hypotheses against all available evidence — and eliminate hypotheses based on inconsistent evidence rather than selecting the one with the most support.

**Key insight:** The hypothesis with the *most inconsistent evidence* is the one to eliminate. The surviving hypothesis is the one that best survives contradiction — not the one with the most confirming evidence (which any motivated analyst can always find).

---

## When to Apply ACH

Mandatory in FULL assessments when:
- Two or more explanations for an event are plausible
- Stakes are high and a wrong assessment has serious consequences
- The "obvious" explanation seems too convenient
- Sources are contradicting each other

Optional in BRIEF assessments when the situation is genuinely ambiguous.

---

## The 4-Step ACH Process

### Step 1: Define All Plausible Hypotheses

Generate at least 3, ideally 4–5 hypotheses. Include:
- The most obvious explanation
- The opposing party's stated explanation
- A "nothing is happening" null hypothesis (often underweighted)
- At least one explanation that would embarrass or surprise the analyst

**Labeling:** H1, H2, H3...

**Example (military buildup near border):**
- H1: Preparation for offensive military action
- H2: Coercive signaling — no intent to attack, designed to extract concessions
- H3: Defensive repositioning in response to perceived threat
- H4: Domestic political theater — no strategic intent
- H5: Military exercise, no political intent

---

### Step 2: Compile All Evidence

List every significant piece of evidence. For each item record:
- Source and tier
- The fact itself (not your interpretation of it)
- Date/recency

Label evidence items E1, E2, E3...

---

### Step 3: Build the ACH Matrix

Create a matrix: hypotheses as columns, evidence as rows.

For each cell, score:
- **C** = Consistent (evidence is consistent with this hypothesis — does NOT confirm it)
- **I** = Inconsistent (evidence contradicts this hypothesis)
- **N** = Not applicable / irrelevant to this hypothesis

```
Evidence         | H1: Offensive | H2: Coercive | H3: Defensive | H4: Theater | H5: Exercise
─────────────────────────────────────────────────────────────────────────────────────────────
E1: Troop movmt  |      C        |      C       |      C        |      C      |      C
E2: No air cover |      I        |      C       |      C        |      C      |      C
E3: Rhetoric ↑   |      C        |      C       |      N        |      C      |      N
E4: Reserves home|      I        |      C       |      I        |      C      |      C
E5: Border open  |      I        |      C       |      C        |      C      |      C
─────────────────────────────────────────────────────────────────────────────────────────────
Inconsistency    |      3        |      0       |      1        |      0      |      0
```

---

### Step 4: Evaluate and Rank

**Eliminate** hypotheses with the most **I** (inconsistent) scores.

**Sensitivity check:** For the leading hypothesis, identify which single piece of evidence, if wrong, would most change the conclusion. Flag this as the key intelligence gap.

**Output format for assessments:**

```markdown
### ACH Summary
Hypotheses evaluated: [H1, H2, H3...]
Evidence items: [count]

| Hypothesis | Inconsistency Count | Status |
|------------|--------------------|---------
| [H1]       | [n]                | ELIMINATED / PLAUSIBLE / LEADING |

**Leading hypothesis:** [H#] — [description]
**Key uncertainty:** [The evidence item that, if wrong, would change the conclusion]
**Eliminated:** [H# — reason: inconsistent with E1, E3]
```

---

## Common ACH Traps to Avoid

### Mirror Imaging
Assuming the adversary thinks and reasons the same way you do.
- Fix: Explicitly ask "What would this decision look like from their domestic political context?"

### Vividness Bias
Giving disproportionate weight to dramatic, recent, or emotionally salient evidence.
- Fix: Check if the "vivid" evidence is actually more reliable than quieter contradicting evidence

### Anchoring on First Hypothesis
The first plausible explanation becomes the default and evidence is selectively gathered to support it.
- Fix: Generate all hypotheses before gathering evidence

### Absence of Evidence = Evidence of Absence
Treating the lack of information about H2 as evidence against H2.
- Fix: "No evidence" and "evidence of absence" are analytically different. State which you have.

---

## ACH for Incomplete Data (Common Situation)

When evidence is sparse:
1. Reduce to 3 hypotheses maximum
2. Increase weight on structural factors (historical pattern, actor incentives) as proxies for direct evidence
3. Explicitly state: "Assessment based primarily on structural factors due to limited direct evidence — confidence LOW"
4. Identify the observable that would most rapidly distinguish between surviving hypotheses

---

## Integration with Red Team Check (Step 8 of main workflow)

ACH and the Red Team Check are complementary, not redundant:
- **ACH** challenges the selection of hypothesis (did we consider all explanations?)
- **Red Team** challenges the conclusion (what would have to be true for us to be wrong?)

Run ACH first. Then Red Team the ACH output.
