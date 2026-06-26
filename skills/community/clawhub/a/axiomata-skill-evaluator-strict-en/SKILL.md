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

## COMMANDS

`python3 /media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict/evaluator.py /media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict --verbose`

`python3 /media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict/eval-skill.py /media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict --verbose`

`curl -s http://localhost:8001/health`

`curl -s http://localhost:11434/api/tags`

`bash -c "ls -la /media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict/"`

`bash -c "wc -l /media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict/SKILL.md"`

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
║  [INPUT] Skill to evaluate                               ║
║           ↓                                             ║
║  PHASE 1: AXIOMA 5-DIMENSION EVALUATION                 ║
║  Target: 90+/100 (18+ per dimension)                    ║
║           ↓                                              ║
║  PHASE 2: ISO 25010 AUTOMATED CHECKS                     ║
║  Target: 100% (13/13 tests passed)                      ║
║           ↓                                              ║
║  PHASE 3: STRICT DECISION                                ║
║                                                           ║
║  IF score >= 90%:                                        ║
║     → APPROVED ✅ — "READY FOR PRODUCTION"              ║
║                                                           ║
║  IF score < 90%:                                         ║
║     → REJECTED ❌ — "NEEDS IMPROVEMENT"                  ║
║     → Return detailed failure report                     ║
║     → NO PUBLISH until 90%+ achieved                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 4. COMMAND REFERENCE

### Full Evaluation (Strict Mode)

```bash
python3 /media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict/evaluator.py <skill-path> --verbose
python3 /media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict/evaluator.py <skill-path> --verbose --improve
```

### ISO 25010 Check

```bash
python3 /media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict/eval-skill.py <skill-path> --verbose
```

### Quick Score

```bash
python3 /media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict/evaluator.py <skill-path> 2>&1 | grep -E "Score|STATUS"
```

---

## 5. STRICT RULES

### The 90% Law

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

### Scoring Matrix

| Score Range | Status | Action |
|-------------|--------|--------|
| **90-100** | 🟢 APPROVED | Ready for production |
| **80-89** | 🔴 REJECTED | Major improvements needed |
| **70-79** | 🔴 REJECTED | Fundamental issues |
| **<70** | 🔴 REJECTED | Complete rewrite required |

---

## 6. REJECTION CRITERIA

### Automatic Rejection Triggers

A skill is automatically REJECTED if ANY of these occur:

| Trigger | Severity | Description |
|---------|----------|-------------|
| Score < 90% | CRITICAL | Below 90% threshold |
| ISO < 100% | CRITICAL | Any ISO check failed |
| Missing SKILL.md | CRITICAL | Core file missing |
| Invalid frontmatter | HIGH | name or description missing |
| No trigger words | HIGH | Cannot be activated |

---

## 7. APPROVAL CRITERIA

### Automatic Approval Requirements

ALL of these MUST be true for APPROVAL:

| Requirement | Strict (90%) |
|-------------|--------------|
| Axioma 5-Dim | 90+/100 |
| Structure | 18+/20 |
| Clarity | 18+/20 |
| Completeness | 18+/20 |
| Consistency | 18+/20 |
| Functionality | 18+/20 |
| ISO 25010 | 100% (13/13) |

---

## 8. COMPARISON: STANDARD vs STRICT

| Aspect | Standard (70%) | Strict (90%) |
|--------|----------------|--------------|
| **Threshold** | 70/100 | **90/100** |
| **Approval rate** | ~70% of skills | ~30% of skills |
| **Quality bar** | "Good enough" | "Excellence only" |
| **Deterministic** | No | **YES** |
| **Use case** | Development | **Production** |
| **ClawHub ready** | Maybe | **Always** |

---

## 9. PATHS CONFIGURATION

| Component | Path |
|-----------|------|
| Strict Evaluator | /media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict/ |
| Evaluator Script | /media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict/evaluator.py |
| ISO Script | /media/ezekiel/Merlin/.openclaw/workspace/skills/axiomata-skill-evaluator-strict/eval-skill.py |

---

## 10. OUTPUT EXAMPLES

### Score >= 90%

```
╔═══════════════════════════════════════════════════════════╗
║  ✅ SKILL APPROVED — 92/100                              ║
║  Threshold: 90% (STRICT)                                  ║
║  STATUS: READY FOR PRODUCTION                             ║
╚═══════════════════════════════════════════════════════════╝
```

### Score < 90%

```
╔═══════════════════════════════════════════════════════════╗
║  ❌ SKILL REJECTED — 82/100 (need 90)                    ║
║  Gap: -8%                                                ║
║  FAILED: Consistency (15/20), Functionality (12/20)     ║
╚═══════════════════════════════════════════════════════════╝
```

---

_In Altum Per Strictness._
🧪 AXIOMA SKILL EVALUATOR STRICT — 90% DETERMINISTIC
