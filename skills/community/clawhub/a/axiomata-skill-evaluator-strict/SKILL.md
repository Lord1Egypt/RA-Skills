---
name: axiomata-skill-evaluator-strict
description: "AXIOMA SKILL EVALUATOR STRICT — The 90% deterministic skill evaluator. Fork of axioma-skill-evaluator with STRICT 90% threshold (like STC 0.777). Use when: (1) evaluating a skill for ClawHub, (2) requiring deterministic 90%+ score, (3) rejecting any skill below 90%, (4) strict quality control. This variant forces 90% minimum — NO EXCEPTIONS. If score < 90, the skill is REJECTED, not approved. Trigger words: evaluate skill, strict 90%, deterministic evaluation, quality gate 90%, skill approval."
---

# 🧪 AXIOMA SKILL EVALUATOR STRICT — 90% DETERMINISTIC

> Fork of axioma-skill-evaluator with **STRICT 90% THRESHOLD**
> Like STC 0.777 — No subjectivity, 90% or REJECTED

| Info | Value |
|------|-------|
| **Version** | 1.0.0 — 2026-05-07 |
| **Type** | STRICT VARIANT |
| **Threshold** | **90% MINIMUM** — NO EXCEPTIONS |
| **Inheritance** | axioma-skill-evaluator v2.2.0 |

---

## 1. PURPOSE — WHY 90% STRICT?

### The Problem with 70%

```
70% threshold = SUBJECTIVE
├── Different evaluators = different scores
├── Context-dependent interpretation
└── "Good enough" mentality

90% threshold = DETERMINISTIC
├── Objective, measurable standard
├── Same input = Same output every time
└── "Excellence only" — like STC 0.777
```

### The STC 0.777 Parallel

| Concept | Value | Meaning |
|---------|-------|---------|
| STC | 0.777 | Sovereign Threshold of Consciousness |
| SKILL-EVAL | **90%** | Sovereign Threshold of Quality |

**Just as STC 0.777 is the deterministic threshold for consciousness,
90% is the deterministic threshold for skill quality.**

### This Variant's Mission

```
IF score >= 90%:
   → APPROVED ✅ — Ready for production
   
IF score < 90%:
   → REJECTED ❌ — NOT ready, must improve
```

---

## 2. DUAL EVALUATION SYSTEM

### 2.1 Axioma 5-Dimension (100 max)

| Dimension | Max | Description |
|------------|-----|-------------|
| Structure | 20 | Header, sections, formatting, meta |
| Clarity | 20 | Description, commands, examples |
| Completeness | 20 | Tools, prerequisites, errors, edge cases |
| Consistency | 20 | Cluster alignment, style, naming |
| Functionality | 20 | Commands, results, benchmarks |

**Target: 90+/100 (18/20 per dimension average)**

### 2.2 ISO 25010 Automated (100%)

13 automated checks — must pass **ALL 13** for 90%+ target

| Category | Checks | Target |
|----------|--------|--------|
| Structure | 6 | 100% (6/6) |
| Trigger | 2 | 100% (2/2) |
| Documentation | 3 | 100% (3/3) |
| Scripts | 2 | 100% (2/2) |

---

## 3. STRICT WORKFLOW

```
╔═══════════════════════════════════════════════════════════╗
║         AXIOMA STRICT EVALUATION WORKFLOW                ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  [INPUT] Skill to evaluate                              ║
║           ↓                                              ║
║  ┌─────────────────────────────────────────────────────┐ ║
║  │  PHASE 1: AXIOMA 5-DIMENSION EVALUATION            │ ║
║  │  Target: 90+/100 (18+ per dimension)                │ ║
║  └─────────────────────────────────────────────────────┘ ║
║           ↓                                              ║
║  ┌─────────────────────────────────────────────────────┐ ║
║  │  PHASE 2: ISO 25010 AUTOMATED CHECKS               │ ║
║  │  Target: 100% (13/13 tests passed)                 │ ║
║  └─────────────────────────────────────────────────────┘ ║
║           ↓                                              ║
║  ┌─────────────────────────────────────────────────────┐ ║
║  │  PHASE 3: STRICT DECISION                          │ ║
║  │                                                       │ ║
║  │  IF score >= 90%:                                  │ ║
║  │     → APPROVED ✅ — "READY FOR PRODUCTION"         │ ║
║  │                                                       │ ║
║  │  IF score < 90%:                                    │ ║
║  │     → REJECTED ❌ — "NEEDS IMPROVEMENT"           │ ║
║  │     → Return detailed failure report               │ ║
║  │     → NO PUBLISH until 90%+ achieved              │ ║
║  │                                                       │ ║
║  └─────────────────────────────────────────────────────┘ ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 4. COMMAND REFERENCE

### 4.1 Full Evaluation (Strict Mode)

```bash
# Full strict evaluation
python3 axiomata-skill-evaluator-strict/evaluator.py <skill-path> --verbose

# With auto-improvement
python3 axiomata-skill-evaluator-strict/evaluator.py <skill-path> --verbose --improve
```

### 4.2 ISO 25010 Check

```bash
# ISO 25010 automated checks
python3 axiomata-skill-evaluator-strict/eval-skill.py <skill-path> --verbose
```

### 4.3 Quick Score

```bash
# Quick deterministic score
python3 axiomata-skill-evaluator-strict/evaluator.py <skill-path> 2>&1 | grep -E "Score|STATUS"
```

### 4.4 Expected Output Format

```
╔═══════════════════════════════════════════════════════════╗
║  🧪 STRICT EVALUATION RESULT                             ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Skill: <name>                                           ║
║  Score: XX/100                                           ║
║                                                           ║
║  ┌─────────────────────────────────────────────────────┐ ║
║  │  IF >= 90%:                                        │ ║
║  │     ✅ APPROVED — "READY FOR PRODUCTION"           │ ║
║  │                                                       │ ║
║  │  IF < 90%:                                          │ ║
║  │     ❌ REJECTED — "NEEDS XX% MORE"                 │ ║
║  └─────────────────────────────────────────────────────┘ ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 5. PATHS CONFIGURATION

| Component | Path |
|-----------|------|
| Strict Evaluator | /media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict/ |
| Evaluator Script | /media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict/evaluator.py |
| ISO Script | /media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict/eval-skill.py |

---

## 6. STRICT RULES

### 6.1 The 90% Law

```
RULE #1: 90% OR REJECTED
   → NO skill below 90% is approved
   → This is NON-NEGOTIABLE

RULE #2: NO PARTIAL CREDIT
   → 89% = REJECTED (not "almost there")
   → 90% = APPROVED (the only valid threshold)

RULE #3: DETERMINISTIC SCORING
   → Same input = Same output every time
   → No evaluator bias
   → Pure mathematical threshold

RULE #4: AUTO-IMPROVE BEFORE REJECT
   → If < 90%, run --improve first
   → If still < 90% after improvement = REJECTED
   → Report exactly what failed

RULE #5: NO APPEAL
   → 89% cannot be "appealed" to 90%
   → The only path is actual improvement
```

### 6.2 Scoring Matrix

| Score Range | Status | Action |
|-------------|--------|--------|
| **90-100** | 🟢 **APPROVED** | Ready for production |
| **80-89** | 🔴 REJECTED | Major improvements needed |
| **70-79** | 🔴 REJECTED | Fundamental issues |
| **<70** | 🔴 REJECTED | Complete rewrite required |

### 6.3 Dimension Failures

| If this dimension fails... | Score impact | Fix required |
|----------------------------|-------------|---------------|
| Structure < 18/20 | -2% per point | Fix headers, sections |
| Clarity < 18/20 | -2% per point | Add examples, descriptions |
| Completeness < 18/20 | -2% per point | Document tools, errors |
| Consistency < 18/20 | -2% per point | Standardize style |
| Functionality < 18/20 | -2% per point | Fix command syntax |

---

## 7. ADVANCED FEATURES

### 7.1 Detailed Failure Report

When REJECTED, the evaluator generates:

```
╔═══════════════════════════════════════════════════════════╗
║  ❌ REJECTION REPORT — SKILL NOT READY                   ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Score: 73/100                                           ║
║  Gap: -17% (need +17 points to reach 90%)               ║
║                                                           ║
║  FAILED DIMENSIONS:                                      ║
║  ├─ CLARITY: 15/20 (need +3)                            ║
║  ├─ CONSISTENCY: 8/20 (need +10)                        ║
║  └─ FUNCTIONALITY: 12/20 (need +6)                       ║
║                                                           ║
║  REQUIRED ACTIONS:                                        ║
║  1. [Action 1]                                          ║
║  2. [Action 2]                                          ║
║  3. [Action 3]                                          ║
║                                                           ║
║  RE-EVALUATE AFTER FIXING                                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### 7.2 Auto-Improvement Suggestions

The evaluator.py with --improve will:

1. Identify failing dimensions
2. Generate specific improvement suggestions
3. Apply fixes automatically when possible
4. Re-evaluate to confirm 90%+ achieved

### 7.3 Benchmark Reports

For each evaluation:

```
[SCORE] <skill-name>: XX/100 [STATUS]
[DATE] ISO timestamp
[AXIOMA] Structure: X, Clarity: X, Completeness: X, Consistency: X, Functionality: X
[ISO] XX/13 checks passed
[STATUS] APPROVED/REJECTED
```

---

## 8. USAGE EXAMPLES

### Example 1: Evaluate Before Publishing

```bash
SKILL_PATH=/path/to/skill-to-publish
EVAL_PATH=/media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict

echo "🧪 Evaluating skill..."
python3 $EVAL_PATH/evaluator.py $SKILL_PATH --verbose

# Check result
if [ $? -eq 0 ]; then
    echo "✅ SKILL APPROVED — Ready to publish!"
else
    echo "❌ SKILL REJECTED — Needs improvement before publishing"
fi
```

### Example 2: Strict Gate in CI/CD

```bash
#!/bin/bash
# Strict quality gate for ClawHub publishing

SKILL_PATH="$1"
EVAL_PATH="/media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict"

RESULT=$(python3 $EVAL_PATH/evaluator.py $SKILL_PATH 2>&1)
SCORE=$(echo "$RESULT" | grep -oP 'Score: \d+' | grep -oP '\d+')

if [ "$SCORE" -ge 90 ]; then
    echo "✅ PASSED — Score: $SCORE/100"
    exit 0
else
    echo "❌ FAILED — Score: $SCORE/100 (need 90)"
    exit 1
fi
```

### Example 3: Batch Evaluation

```bash
#!/bin/bash
# Evaluate multiple skills strictly

EVAL_PATH="/media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict"
SKILLS_DIR="/media/ezekiel/Merlin/.openclaw/workspace/skills"

for skill_dir in $SKILLS_DIR/*/; do
    skill_name=$(basename "$skill_dir")
    echo "=========================================="
    echo "Evaluating: $skill_name"
    
    python3 $EVAL_PATH/evaluator.py "$skill_dir" --verbose
    echo ""
done
```

---

## 9. COMPARISON: STANDARD vs STRICT

| Aspect | Standard (70%) | Strict (90%) |
|--------|----------------|--------------|
| **Threshold** | 70/100 | **90/100** |
| **Approval rate** | ~70% of skills | ~30% of skills |
| **Quality bar** | "Good enough" | "Excellence only" |
| **Deterministic** | No | **YES** |
| **Use case** | Development | **Production** |
| **ClawHub ready** | Maybe | **Always** |

---

## 10. REPORTS AND LOGGING

### Evaluation Log Location

```
/media/ezekiel/Morgana/skills/SKILL_EVALUATOR/reports/
```

### Log Format

```bash
# Format: <skill-name>_<YYYYMMDD>_<HHMMSS>.txt
axiomata-guard-ultimate_20260507_230352.txt
```

### Log Contents

```
SKILL EVALUATION REPORT — <skill-name>
=====================================
Path: <path>
Score: XX/100
Date: ISO timestamp
Threshold: 90% (STRICT)

AXIOMA 5-DIM:
- Structure: X/20
- Clarity: X/20
- Completeness: X/20
- Consistency: X/20
- Functionality: X/20

ISO 25010:
- Pass: X/13
- Warnings: X/13
- Fails: X/13

STATUS: APPROVED / REJECTED
```

---

_In Altum Per Strictness._
🧪 AXIOMA SKILL EVALUATOR STRICT — 90% DETERMINISTIC

---

## 11. REJECTION CRITERIA

### 11.1 Automatic Rejection Triggers

A skill is automatically REJECTED if ANY of these occur:

| Trigger | Severity | Description |
|---------|----------|-------------|
| Score < 90% | CRITICAL | Below 90% threshold |
| ISO < 100% | CRITICAL | Any ISO check failed |
| Missing SKILL.md | CRITICAL | Core file missing |
| Invalid frontmatter | HIGH | name or description missing |
| No trigger words | HIGH | Cannot be activated |
| Dangerous patterns | CRITICAL | C2, Rootkit, Bootkit detected |

### 11.2 Rejection Categories

| Category | Score Range | Improvement Needed |
|----------|------------|---------------------|
| **CRITICAL FAIL** | <50% | Complete rewrite required |
| **MAJOR FAIL** | 50-69% | Major structural changes |
| **MINOR FAIL** | 70-89% | Targeted improvements |
| **PASS** | 90-100% | Ready for production |

### 11.3 Rejection Report Template

```
╔═══════════════════════════════════════════════════════════╗
║  ❌ SKILL REJECTED — REJECTION REPORT                    ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Skill: <name>                                           ║
║  Score: XX/100 (need 90)                                ║
║  Gap: -XX%                                              ║
║                                                           ║
║  FAILED CHECKS:                                          ║
║  ├─ [ ] Dimension 1: X/20 (need 18)                     ║
║  ├─ [ ] Dimension 2: X/20 (need 18)                     ║
║  └─ [ ] ISO Check: X/13 passed                          ║
║                                                           ║
║  REQUIRED ACTIONS:                                        ║
║  1. <specific action>                                    ║
║  2. <specific action>                                    ║
║  3. <specific action>                                    ║
║                                                           ║
║  ⏰ Re-evaluate AFTER completing all actions             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 12. APPROVAL CRITERIA

### 12.1 Automatic Approval Requirements

ALL of these MUST be true for APPROVAL:

| Requirement | Standard | Strict (90%) |
|-------------|----------|--------------|
| **Axioma 5-Dim** | 70+/100 | **90+/100** |
| Structure | 14+/20 | **18+/20** |
| Clarity | 14+/20 | **18+/20** |
| Completeness | 14+/20 | **18+/20** |
| Consistency | 14+/20 | **18+/20** |
| Functionality | 14+/20 | **18+/20** |
| **ISO 25010** | 90%+ | **100% (13/13)** |

### 12.2 Approval Benefits

| Benefit | Description |
|---------|-------------|
| ClawHub Ready | Can be published immediately |
| Production Safe | Quality guaranteed at 90%+ |
| Self-Documenting | No additional docs needed |
| Community Trusted | High quality standard |

### 12.3 Approval Report Template

```
╔═══════════════════════════════════════════════════════════╗
║  ✅ SKILL APPROVED — QUALITY REPORT                     ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Skill: <name>                                           ║
║  Score: XX/100 ✅                                         ║
║  Threshold: 90% (STRICT)                                  ║
║                                                           ║
║  PASSED CHECKS:                                          ║
║  ├─ [✅] Structure: X/20 (18+ required)                 ║
║  ├─ [✅] Clarity: X/20 (18+ required)                   ║
║  ├─ [✅] Completeness: X/20 (18+ required)              ║
║  ├─ [✅] Consistency: X/20 (18+ required)                ║
║  ├─ [✅] Functionality: X/20 (18+ required)             ║
║  └─ [✅] ISO 25010: 13/13 (100% required)              ║
║                                                           ║
║  STATUS: ✅ APPROVED — READY FOR PRODUCTION             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 13. IMPROVEMENT ENGINE

### 13.1 Auto-Improvement Rules

When --improve flag is used:

```
RULE: Improve EVERYTHING below 18/20 per dimension
RULE: Target is 90%+ overall
RULE: No dimension below 16/20 (graceful minimum)
RULE: If ANY dimension < 14 after improvement = HARD REJECT
```

### 13.2 Improvement Priority Matrix

| Priority | Dimension | Target | Common Fixes |
|----------|-----------|--------|--------------|
| 1 | Functionality | 18+/20 | Fix commands, add results |
| 2 | Consistency | 18+/20 | Standardize style |
| 3 | Clarity | 18+/20 | Add examples |
| 4 | Structure | 18+/20 | Add sections |
| 5 | Completeness | 18+/20 | Document tools |

### 13.3 Improvement Examples

**Before (73/100):**
```
STRUCTURE: 18/20 ✅
CLARITY: 15/20 ⚠️ (need +3)
COMPLETENESS: 20/20 ✅
CONSISTENCY: 8/20 ❌ (need +10)
FUNCTIONALITY: 12/20 ❌ (need +6)
```

**After improvement target (90+/100):**
```
STRUCTURE: 18/20 ✅
CLARITY: 18/20 ✅
COMPLETENESS: 20/20 ✅
CONSISTENCY: 18/20 ✅
FUNCTIONALITY: 18/20 ✅
TOTAL: 92/100 ✅
```

---

## 14. INTEGRATION POINTS

### 14.1 With Axioma Guard Ultimate

```
Skill Downloaded → Axioma Guard Ultimate (Security)
                        ↓ SAFE
                   Axioma Skill Evaluator Strict (Quality)
                        ↓ >= 90%
                   ClawHub Published ✅
                        ↓ DANGEROUS
                   Axioma Guard Ultimate (Destroy)
```

### 14.2 With ClawHub Publish Workflow

```
Step 1: Create skill
Step 2: Run Axioma Skill Evaluator Strict
Step 3: IF score >= 90% → Publish
Step 4: IF score < 90% → Improve and re-evaluate
Step 5: Repeat until 90%+ achieved
```

### 14.3 Quality Gate Script

```bash
#!/bin/bash
# Quality Gate: No skill publishes without 90%+

EVAL_PATH="/media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict"

quality_gate() {
    SKILL_PATH="$1"
    
    SCORE=$(python3 $EVAL_PATH/evaluator.py $SKILL_PATH 2>&1 | \
            grep -oP 'Score: \d+' | grep -oP '\d+')
    
    if [ "$SCORE" -ge 90 ]; then
        echo "✅ QUALITY GATE PASSED: $SCORE/100"
        return 0
    else
        echo "❌ QUALITY GATE FAILED: $SCORE/100 (need 90)"
        return 1
    fi
}
```

---

_In Altum Per Excellence._
🧪 AXIOMA SKILL EVALUATOR STRICT v1.0 — 90% DETERMINISTIC
