## Description:

Monthly and quarterly budget vs. actual variance analysis for businesses, including variance tables, root-cause commentary, and rolling forecast recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

CFOs, controllers, FP&A analysts, and finance operators use this skill to compare planned and actual revenue, expenses, margins, and EBITDA for a closed month, quarter, or YTD period. It helps produce management or board commentary and update a rolling forecast from supplied budget and actuals data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive business financial data and may require budget files, actuals exports, account mappings, or QBO access.

Mitigation: Provide only the financial files or QBO access needed for the specific analysis, and remove unrelated client, payroll, vendor, or banking details before use.

Risk: Outputs can be misleading when no formal budget exists or assumptions are not explicit.

Mitigation: Use a separate budgeting workflow first, or require explicit baseline assumptions before relying on the variance analysis.

Risk: Ambiguous account mappings, materiality thresholds, or favorable/unfavorable sign conventions can distort variance commentary.

Mitigation: Confirm the chart of accounts mapping, threshold settings, and raw actual-minus-budget sign convention before sharing management or board-facing output.

Risk: The skill is not intended for tax preparation, transactional bookkeeping, real-time cash tracking, or multi-entity consolidation with eliminations.

Mitigation: Route those tasks to dedicated tax, bookkeeping, cash management, or consolidation workflows before using this skill's commentary.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samledger67-dotcom/skills/budget-vs-actual)
- [Skill Source](artifact/SKILL.md)
- [Dogfood Test Report](artifact/DOGFOOD-TEST-2026-03-17.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown management report, one-page flash summary, or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes variance tables, materiality flags, root-cause analysis, management commentary, and rolling forecast updates.]

## Skill Version(s):

98.0.2 (source: server release metadata; source skill frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
