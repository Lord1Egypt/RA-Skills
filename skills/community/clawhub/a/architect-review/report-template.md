# Report Template

This file defines the output format for architecture review reports.
The skill strictly follows this template. Customize it to control report structure,
detail level, and language.

---

## Overall Report Structure

```markdown
# Architecture Review Report

**Project**: {project_name}
**Date**: {date}
**Spec Source**: {spec_path}
**Mode**: {full | spec-only | focused(dimensions)}

---

## Scoreboard

| Dimension | Score | Verdict |
|-----------|-------|---------|
| {dimension_name} | {score}/10 | {verdict_emoji} {one_line_verdict} |
| ... | ... | ... |

**Overall Score**: {weighted_average}/10

---

{per_dimension_sections}

---

## Top Critical Issues

{top_n_issues}

---

## Consolidated Recommendations

{priority_ordered_recommendations}

---

## Next Steps

{interactive_discussion_candidates}
```

---

## Verdict Emoji Rules

| Score Range | Emoji | Label |
|-------------|-------|-------|
| 9-10 | ✅ | Excellent |
| 7-8 | 🟡 | Adequate |
| 4-6 | 🟠 | Needs Improvement |
| 0-3 | 🔴 | Critical |

---

## Per-Dimension Section Format

Each dimension produces one section following this format:

```markdown
## {dimension_name} — {score}/10 {verdict_emoji}

### Strengths
- {strength_1}: {brief explanation, reference spec requirement or code path}
- {strength_2}: ...

### Weaknesses
- {weakness_1}: {brief explanation, reference spec requirement or code path}
- {weakness_2}: ...

### Recommendations

| # | Priority | Recommendation | Related Spec/Code |
|---|----------|---------------|-------------------|
| 1 | {high/medium/low} | {actionable suggestion} | {requirement name or file path} |
| 2 | ... | ... | ... |
```

---

## Top Critical Issues Format

Select the 3 lowest-scoring dimensions and present:

```markdown
### Issue 1: {dimension_name} (Score: {score}/10)

**Root Cause**: {one paragraph explaining why this dimension scored low}

**Impact**: {what goes wrong if this is not addressed}

**Suggested Fix**: {concrete first step to improve}
```

---

## Selected Issues (user confirmed)

These issues were selected by the user for inclusion in the formal report.
Each issue includes location info for a downstream fix agent.

```markdown
## Selected Architectural Issues

### Issue 1: {title}

- **Dimension**: {dimension_name}
- **Severity**: {high|medium|low}
- **Location**: `{module/file path where the problem is rooted}`
- **Related Spec**: {requirement name(s)}

**Problem**: {architectural problem description — what is structurally wrong}

**Impact**: {what goes wrong if not addressed}

**Architectural Direction**: {suggested structural approach — NOT a code-level fix,
but a pattern/boundary/responsibility change}
```

---

## Deferred Issues (recorded for future cycles)

Issues identified but not selected for this report cycle.

```markdown
## Deferred Issues

| # | Dimension | Severity | Summary | Location |
|---|-----------|----------|---------|----------|
| 1 | {dim} | {sev} | {one-line summary} | `{module/path}` |
| 2 | ... | ... | ... | ... |
```

---

## Machine-Readable Metadata

At the END of the report file, include a hidden metadata block for downstream agents:

```markdown
<!-- ARCH-REVIEW-META
project: {project_path}
date: {iso_date}
dimensions_reviewed: [dim1, dim2, ...]
selected_issues:
  - id: issue-1
    dimension: {dimension_id}
    severity: high
    location: {module or file path}
    spec_refs: [requirement_name_1, requirement_name_2]
    summary: {one-line}
deferred_issues:
  - id: deferred-1
    dimension: {dimension_id}
    severity: medium
    location: {module or file path}
    summary: {one-line}
-->
```

This metadata enables a separate fix agent to:
- Parse the report programmatically
- Navigate directly to problem locations
- Understand severity and scope without reading prose
