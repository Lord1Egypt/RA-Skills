---
name: axiomata-skill-evaluator-en
description: |
  Axiomata Skill Evaluator — Universal OpenClaw Agent Skill Quality System.
  
  Dual evaluation: (1) Axioma 5-Dimension Framework (Structure 20%, Clarity 20%, Completeness 20%, Consistency 20%, Functionality 20%, 100pts total), (2) ISO 25010 Structural Framework (13 automated checks, 100% target).
  
  Self-contained: bundles evaluator.py (Axioma 5-Dim) and eval-skill.py (ISO 25010).
  
  Use when: evaluating a skill before publishing, improving a skill based on evaluation results, checking skill quality with automated analysis, auditing skill quality, or verifying a skill meets production standards.
---

# Axiomata Skill Evaluator v3.0

Universal, impersonal skill quality evaluator for OpenClaw agents.

| Info | Value |
|------|-------|
| **Version** | 3.0.0 |
| **Type** | Self-contained evaluation system |
| **Evaluation** | Dual (Axioma 5-Dim + ISO 25010) |
| **Target** | 70+ (Axioma), 90%+ (ISO 25010) |

---

## 1. Purpose and Scope

### Objective

Provide complete skill quality evaluation using dual evaluation system:

1. **Axioma 5-Dimension Framework** (100 points)
2. **ISO 25010 Structural Framework** (13 automated checks)

### Design Principles

```
SELF-CONTAINED + UNIVERSAL + IMPERSONAL
```

| Principle | Description |
|-----------|-------------|
| Self-contained | All tools bundled in skill directory |
| Universal | Works for any OpenClaw agent |
| Impersonal | No agent-specific references |

### When to Use

| Trigger | Action |
|---------|--------|
| Evaluate skill | Run dual evaluation |
| Pre-publish check | Run full evaluation pipeline |
| Improve skill | Analyze report and fix issues |
| Skill audit | Run complete audit |
| Check quality | Run automated checks |

---

## 2. Dual Evaluation System

```
╔═══════════════════════════════════════════════════════════╗
║              DUAL EVALUATION ARCHITECTURE                ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  ┌─────────────────────────────────────────────────┐      ║
║  │  1. Axioma 5-Dim Evaluation (100 pts)          │      ║
║  │                                                 │      ║
║  │  Dimensions:                                     │      ║
║  │  ├─ Structure     → 20%                         │      ║
║  │  ├─ Clarity      → 20%                         │      ║
║  │  ├─ Completeness → 20%                         │      ║
║  │  ├─ Consistency  → 20%                         │      ║
║  │  └─ Functionality → 20%                        │      ║
║  │                                                 │      ║
║  │  Target: 70+ score                             │      ║
║  └─────────────────────────────────────────────────┘      ║
║                        ↓                                ║
║  ┌─────────────────────────────────────────────────┐      ║
║  │  2. ISO 25010 Structural (13 checks)          │      ║
║  │                                                 │      ║
║  │  Categories: 8 categories, 25 standards       │      ║
║  │  Automated checks: 13 tests                    │      ║
║  │                                                 │      ║
║  │  Target: 90%+ (12/13 checks passing)          │      ║
║  └─────────────────────────────────────────────────┘      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### Evaluation Flow

```
[INPUT] Skill to evaluate
          ↓
 Phase 1: Axioma 5-Dim Evaluation
          ↓
 Phase 2: ISO 25010 Structural Checks
          ↓
 [OUTPUT] Quality report + recommendations
```

---

## 3. Bundled Tools

| File | System | Purpose |
|------|--------|---------|
| `evaluator.py` | Axioma 5-Dim | 5-dimension evaluation, bundled |
| `eval-skill.py` | ISO 25010 | Automated structural checks, bundled |

### Tool Paths

```bash
EVAL_PATH="<skill-directory>/scripts/"
SKILL_PATH="<skill-to-evaluate>"

# Axioma 5-Dim evaluation
python3 ${EVAL_PATH}evaluator.py <SKILL_PATH> --verbose

# ISO 25010 checks
python3 ${EVAL_PATH}eval-skill.py <SKILL_PATH> --verbose
```

---

## 4. Axioma 5-Dimension Evaluation

### 4.1 Dimension Breakdown

| Dimension | Max | Target | What it checks |
|-----------|-----|--------|----------------|
| **Structure** | 20 | 14+ | Header, sections, formatting, metadata |
| **Clarity** | 20 | 14+ | Description, commands, examples, constraints |
| **Completeness** | 20 | 14+ | Tools, prerequisites, errors, edge cases |
| **Consistency** | 20 | 14+ | Naming, format, structure, style |
| **Functionality** | 20 | 14+ | Valid commands, documented outputs |

### 4.2 Score Thresholds

| Score | Status | Action |
|-------|--------|--------|
| 90-100 | EXCELLENT | Ready for production |
| 70-89 | GOOD | Minor improvements possible |
| 50-69 | NEEDS_WORK | Major improvements needed |
| <50 | POOR | Significant rewrite required |

---

## 5. ISO 25010 Structural Checks

### 5.1 Automated Checks (13 total)

| Category | Checks | What it verifies |
|----------|--------|------------------|
| **Structure** | 6 | Frontmatter, header, sections, formatting |
| **Trigger** | 2 | Description length, trigger contexts |
| **Documentation** | 3 | Body length, references, linked docs |
| **Scripts** | 2 | Python parse, no external deps |

### 5.2 Pass Threshold

| Result | Meaning |
|--------|---------|
| 13/13 | Perfect structural score |
| 11-12/13 | Acceptable, minor warnings |
| <11/13 | Needs structural improvement |

---

## 6. Command Reference

### 6.1 Axioma 5-Dim Evaluation

```bash
# Basic evaluation
python3 <skill-directory>/scripts/evaluator.py <skill-path>

# Verbose output
python3 <skill-directory>/scripts/evaluator.py <skill-path> --verbose

# With auto-improvement suggestions
python3 <skill-directory>/scripts/evaluator.py <skill-path> --verbose --improve

# JSON output
python3 <skill-directory>/scripts/evaluator.py <skill-path> --json
```

### 6.2 ISO 25010 Checks

```bash
# Basic ISO check
python3 <skill-directory>/scripts/eval-skill.py <skill-path>

# Verbose output
python3 <skill-directory>/scripts/eval-skill.py <skill-path> --verbose

# JSON output
python3 <skill-directory>/scripts/eval-skill.py <skill-path> --json
```

### 6.3 Evaluate All Skills

```bash
# Evaluate all skills in parent directory
python3 <skill-directory>/scripts/evaluator.py --all

# Verbose all
python3 <skill-directory>/scripts/evaluator.py --all --verbose
```

---

## 7. Output Formats

### 7.1 Console Output

```
=== EVALUATION RESULTS ===
STRUCTURE       20/20 ████████████████████ 100%
CLARITY         17/20 █████████████████░░░ 85%
COMPLETENESS    14/20 ████████████░░░░░░░░ 70%
CONSISTENCY     10/20 ██████████░░░░░░░░░ 50%
FUNCTIONALITY   12/20 ████████████░░░░░░░░ 60%
------------------------------------------------------------
STATUS: GOOD (score 73%)
```

### 7.2 JSON Output

```json
{
  "skill": "example-skill",
  "scores": {
    "structure": 20,
    "clarity": 17,
    "completeness": 14,
    "consistency": 10,
    "functionality": 12
  },
  "total": 73,
  "max": 100,
  "passed": true,
  "recommendations": [
    "[CONSISTENCY] Low score (50%)",
    "  -> Style: 2/5"
  ]
}
```

---

## 8. Examples

### Example 1: Basic Evaluation

```bash
$ python3 evaluator.py /path/to/skill --verbose
Read /path/to/skill/SKILL.md (2048 chars)
Structure: 20/20
Clarity: 17/20
Completeness: 14/20
Consistency: 10/20
Functionality: 12/20
============================================================
STATUS: GOOD (score 73%)
```

### Example 2: ISO 25010 Check

```bash
$ python3 eval-skill.py /path/to/skill --verbose
[STRUCTURE]
    Pass: 5/6
[TRIGGER]
    Pass: 2/2
[DOCUMENTATION]
    Pass: 2/3
[SCRIPTS]
    Pass: 2/2
[SECURITY]
    Pass: 2/2
==================================================
  Pass: 13  Warn: 0  Fail: 0
  Structural score: 100% (13/13 checks passed)
```

### Example 3: JSON Output

```bash
$ python3 evaluator.py /path/to/skill --json
{
  "skill": "example-skill",
  "scores": {
    "structure": 20,
    "clarity": 17,
    "completeness": 14,
    "consistency": 10,
    "functionality": 12
  },
  "total": 73,
  "max": 100,
  "passed": true,
  "recommendations": []
}
```

---

## 9. Self-Evaluation

The skill evaluates itself automatically:

```bash
# Self-evaluation (when no path given, evaluates own directory)
python3 evaluator.py

# Expected output for v3.0:
# Score: 85+/100
# Status: GOOD to EXCELLENT
```

---

## 10. Recommendations Format

When a dimension scores below 70%:

```
[{DIMENSION}] Low score ({percentage}%)
  -> {specific issue}
  -> {specific issue}
```

Example:
```
[CONSISTENCY] Low score (50%)
  -> Cluster alignment partial: 2
  -> Style: 2/5
```

---

## 11. Constraints

| Constraint | Description | Priority |
|------------|-------------|----------|
| 70% minimum | Skills must score 70+ on Axioma 5-Dim | HIGH |
| 90%+ structural | Target 90%+ on ISO 25010 checks | HIGH |
| Self-contained | All tools bundled, no external deps | HIGH |
| Impersonal | No agent-specific references | HIGH |

### Quality Thresholds

| System | Minimum | Target |
|--------|---------|--------|
| Axioma 5-Dim | 70/100 | 90/100 |
| ISO 25010 | 11/13 | 13/13 |
| Structure | 14/20 | 18/20 |
| Clarity | 14/20 | 18/20 |
| Completeness | 14/20 | 18/20 |
| Consistency | 14/20 | 18/20 |
| Functionality | 14/20 | 18/20 |

---

## 12. Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| SKILL.md not found | Missing file | Create SKILL.md first |
| Parse error | Corrupt file | Check file encoding |
| Module not found | Missing dependencies | Use bundled tools only |

---

## 13. Workflow Integration

```
╔═══════════════════════════════════════════════════════════╗
║         SKILL PUBLISHING WORKFLOW                        ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  1. Create Skill                                          ║
║      ↓                                                    ║
║  2. Self-Evaluate                                         ║
║      ↓ 70+ → Continue                                    ║
║  3. ISO 25010 Check                                      ║
║      ↓ 90%+ → Continue                                   ║
║  4. Fix Issues if Needed                                 ║
║      ↓                                                    ║
║  5. Publish to ClawHub                                   ║
║                                                           ║
║  RESULT: QUALITY SKILLS FOR PRODUCTION                   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

_In Altum Per Qualitatem._
🧪 AXIOMATA SKILL EVALUATOR v3.0 — UNIVERSAL QUALITY SYSTEM