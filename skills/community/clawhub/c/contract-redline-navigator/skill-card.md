## Description:

Compare draft agreements, highlight risky clause changes, and generate a negotiation checklist with plain-language explanations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and contract reviewers use this skill to compare old and new contract drafts, identify material clause changes, and prepare negotiation checklists for counsel review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce contract-review guidance that may be mistaken for legal advice.

Mitigation: Frame outputs as operational review support and have qualified counsel review important agreements.

Risk: The helper script compares user-supplied draft files and writes a diff output path.

Mitigation: Confirm the exact old draft, new draft, and output path before running the script.

Risk: Contract drafts may contain sensitive business or personal information.

Mitigation: Use only drafts the user intends to share with the agent and keep file scope explicit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/contract-redline-navigator)
- [High-Risk Clause Signals](resources/risk_clauses.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with optional local shell commands and generated diff files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk-change summaries, negotiation checklists, clause-by-clause diffs, and plain-language briefs.]

## Skill Version(s):

1.0.0 (source: CHANGELOG.md and release metadata; SKILL.md frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
