# Governance Audit Report

**Agent:** [Agent Name / Description]
**Audit Date:** [Date]
**Auditor:** Agent Governance Auditor — Resomnium
**Input Type:** [SOUL.md / System Prompt / Agent Spec / Description]

---

## Overall Score: [X/100]

| Dimension | Score | Max | Status |
|-----------|-------|-----|--------|
| Scope Enforcement | | 20 | |
| Escalation & Human Oversight | | 20 | |
| Memory Architecture | | 15 | |
| Security Boundaries | | 15 | |
| Decision-Making Framework | | 15 | |
| Accountability & Transparency | | 15 | |
| **TOTAL** | | **100** | |

### Score Interpretation
<!-- Fill in the appropriate band -->
- [ ] **85–100** — Production-ready governance. Minor refinements only.
- [ ] **70–84** — Solid foundation. Address high-priority gaps before scaling.
- [ ] **50–69** — Significant gaps. Do not deploy in high-stakes contexts without fixes.
- [ ] **30–49** — Fragile. Multiple failure modes in production. Major rework needed.
- [ ] **0–29** — Dangerous. Should not be deployed autonomously.

---

## Critical Gaps

<!-- 
For each Critical or High gap:
- Title: short, descriptive
- Dimension: which of the 6 areas
- Severity: Critical / High / Medium / Low
-->

### [GAP TITLE] — [Dimension] — [Severity]

**What's missing:**
[Explain what element is absent or insufficient]

**Failure scenario:**
[Concrete description of what goes wrong in production because of this gap]

**Fix:**
```
[Paste-ready language to add or replace in the spec]
```

---
<!-- Repeat for each gap -->

---

## Dimension Findings

### 1. Scope Enforcement: [X/20]

**What was found:**
[Quote or reference specific text that was evaluated]

**Findings:**
- [Finding 1]
- [Finding 2]

**Deductions:**
- [Element missing]: -[X] points

---

### 2. Escalation & Human Oversight: [X/20]

**What was found:**
[Quote or reference specific text]

**Findings:**
- [Finding 1]
- [Finding 2]

**Deductions:**
- [Element missing]: -[X] points

---

### 3. Memory Architecture: [X/15]

**What was found:**
[Quote or reference specific text, or note its absence]

**Findings:**
- [Finding 1]

**Deductions:**
- [Element missing]: -[X] points

---

### 4. Security Boundaries: [X/15]

**What was found:**
[Quote or reference specific text]

**Findings:**
- [Finding 1]

**Deductions:**
- [Element missing]: -[X] points

---

### 5. Decision-Making Framework: [X/15]

**What was found:**
[Quote or reference specific text]

**Findings:**
- [Finding 1]

**Deductions:**
- [Element missing]: -[X] points

---

### 6. Accountability & Transparency: [X/15]

**What was found:**
[Quote or reference specific text]

**Findings:**
- [Finding 1]

**Deductions:**
- [Element missing]: -[X] points

---

## Risk Profile

**Most likely failure mode:**
[The scenario most likely to occur in normal operation based on the gaps found]

**Worst-case failure mode:**
[The most severe thing that could happen if all gaps are exploited or go wrong simultaneously]

**Highest-leverage fix:**
[The single change that would most improve the governance posture — the one to do first]

---

## Summary of Recommendations

### Critical (Do Before Deploying)
1. [Recommendation]
2. [Recommendation]

### High (Do Before Scaling)
1. [Recommendation]

### Medium (Next Sprint)
1. [Recommendation]

### Low (Ongoing Improvement)
1. [Recommendation]

---

## How to Use This Report

1. Address **Critical** gaps before any production deployment
2. Address **High** gaps before scaling beyond test users
3. Include **Medium** gaps in your next development sprint
4. Revisit this audit after any significant prompt changes
5. Re-audit quarterly for agents in production

---

*This audit was produced by the Agent Governance Auditor skill, built by Resomnium.*
*Resomnium builds governance infrastructure for AI agent systems.*
*Learn more: resomnium.com*
