---
name: axioma-skill-evaluator
description: "Advanced skill evaluation for OpenClaw agents. Use when: (1) evaluating a skill before publishing, (2) improving a skill based on evaluation results, (3) checking skill quality with automated + manual analysis, (4) any skill audit or quality check. Combines dual evaluation systems: Axioma 5-dimension framework (100 max) with ISO 25010 international framework (25 criteria, 100 max). Features: colorful terminal output, dual evaluation, 25-criteria rubric, self-contained bundled scripts."
---

# AXIOMA SKILL EVALUATOR 🧙‍♂️

> Advanced Skill Evaluation: Dual System (Automated + Manual)

| Info | Value |
|------|-------|
| **Version** | 2.1.0 — 2026-05-07 |
| **Status** | OPERATIONAL |

---

## 1. PURPOSE AND SCOPE

### Objective

Provide comprehensive skill evaluation using dual systems:
- **Axioma System** (5 dimensions, 100 max) — colorful, fast
- **ISO 25010 System** (25 criteria, 100 max) — international standard

### When to Use

| Trigger | Action |
|---------|--------|
| Before publishing a skill | Run both evaluations |
| Improving a skill | Get both automated + manual scores |
| Quality audit | Use 25-criteria rubric |
| Pre-publication check | Run all checks |

---

## 2. BUNDLED TOOLS

### evaluator.py (Axioma System)

```bash
# Run Axioma 5-dimension evaluation
python3 evaluator.py <skill-path> --verbose --improve
```

### eval-skill.py (ISO 25010 System)

```bash
# Run automated ISO 25010 checks
python3 eval-skill.py <skill-path> --verbose

# JSON output
python3 eval-skill.py <skill-path> --json
```

---

## 3. AXIOMA EVALUATION SYSTEM

### Quick Start

```bash
python3 evaluator.py <skill-path> --verbose --improve
```

### 5 Dimensions (100 max)

| Dimension | Weight | Focus |
|-----------|--------|-------|
| Structure | 20% | Header, sections, formatting, meta |
| Clarity | 20% | Description, instructions, examples |
| Completeness | 20% | Tools, prerequisites, errors, edge cases |
| Consistency | 20% | Style, naming, integration |
| Functionality | 20% | Commands work, expected results |

### Output Format

```
╔═══════════════════════════════════════════════════════════╗
║ 📊 SKILL EVALUATION REPORT — [Skill Name]              ║
║ Score: XX/100 [STATUS]                                  ║
╠═══════════════════════════════════════════════════════════╣
║ STRUCTURE:     XX/20 ████████████░░░░ XX%                ║
║ CLARITY:      XX/20 ████████████░░░░ XX%                ║
║ COMPLETENESS: XX/20 ████████████░░░░ XX%                ║
║ CONSISTENCY:  XX/20 ████████████░░░░ XX%                ║
║ FUNCTIONALITY: XX/20 ████████████░░░░ XX%                ║
╠═══════════════════════════════════════════════════════════╣
║ STATUS: ✅ APPROVED (score >= 70%)                      ║
╚═══════════════════════════════════════════════════════════╝
```

### Thresholds

| Score | Status | Action |
|-------|--------|--------|
| 90-100 | 🟢 EXCELLENT | Ready for production |
| 70-89 | 🟡 GOOD | Publishable, minor notes |
| 50-69 | 🟠 NEEDS_WORK | Fix before publishing |
| <50 | 🔴 POOR | Major rework needed |

---

## 4. ISO 25010 EVALUATION SYSTEM

### Automated Checks (eval-skill.py)

Runs 13 automated checks:
- File structure validation
- Frontmatter YAML parsing
- Description quality (65+ words, trigger contexts)
- Script syntax validation
- Credential scanning
- Dependency audit

**Target: 90%+ (12+/13 checks passed)**

### Manual Assessment (25 Criteria)

| Category | Framework | Max | Criteria |
|----------|-----------|-----|----------|
| 1. Functional Suitability | ISO 25010 | /12 | Completeness, Correctness, Appropriateness |
| 2. Reliability | ISO 25010 | /12 | Fault Tolerance, Error Reporting, Recoverability |
| 3. Performance | ISO 25010 | /8 | Token Cost, Execution Efficiency |
| 4. Usability (AI) | Shneiderman | /12 | Learnability, Consistency, Feedback |
| 5. Usability (Human) | Tognazzini | /8 | Discoverability, Forgiveness |
| 6. Security | ISO 25010 | /12 | Credentials, Input Validation, Data Safety |
| 7. Maintainability | ISO 25010 | /12 | Modularity, Modifiability, Testability |
| 8. Agent-Specific | Novel | /24 | Trigger Precision, Progressive Disclosure, Composability |
| **TOTAL** | | **/100** | |

---

## 5. COMPLETE EVALUATION WORKFLOW

```
1. AUTOMATED: python3 eval-skill.py <path> --verbose
   → Target: 90%+ structural score
   ↓
2. AXIOMA: python3 evaluator.py <path> --verbose --improve
   → Target: 70+ score
   ↓
3. MANUAL: Score 25 criteria rubric
   → Target: 80+ score
   ↓
4. FIX: Issues from all three sources
   ↓
5. RE-EVALUATE: Until all targets met
   ↓
6. PUBLISH: To ClawHub
```

---

## 6. ERROR HANDLING

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| No frontmatter | YAML not at start | Add `---` at start of SKILL.md |
| Poor description | Missing triggers | Add "Use when:" clauses |
| Empty directories | Unused folders | Remove or populate |
| Name mismatch | Directory ≠ frontmatter | Rename to match |

### Security Issues

| Issue | Severity | Action |
|-------|----------|--------|
| Hardcoded credentials | CRITICAL | Remove immediately |
| Missing input validation | HIGH | Add validation |
| No error handling | MEDIUM | Add try/catch blocks |

---

## 7. EDGE CASES

| Case | Input | Expected Output |
|------|-------|-----------------|
| Empty SKILL.md | Empty file | Error message, suggest template |
| Very long SKILL.md | >500 lines | Warning, recommend split |
| Missing description | No frontmatter | Fail with instructions |
| No scripts | No scripts/ dir | Pass, document as standalone |

---

## 8. DEPENDENCIES

| Dependency | Purpose | Required |
|------------|---------|----------|
| Python 3.6+ | Script execution | Yes |
| PyYAML | Frontmatter parsing | Optional |

---

_In Altum Per Quality._
🧙‍♂️ Axioma Skill Evaluator v2.1