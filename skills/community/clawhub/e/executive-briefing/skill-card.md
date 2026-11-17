## Description:

Report Builder helps agents turn detailed source material into concise executive briefings, decision memos, one-pagers, and board reports using BLUF and So What structure plus local validation and density checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dabin0927](https://clawhub.ai/user/dabin0927)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, consultants, and business teams use this skill to compress detailed plans or research into executive-facing decision reports for CEOs, boards, investors, or department leaders. It is intended for decision summaries, management briefings, one-page reports, and board materials rather than technical documentation, data visualization, or slide layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local Python scripts can create, modify, or overwrite report files outside the intended report area when report names or paths are not constrained.

Mitigation: Use explicit safe report names without path separators or absolute paths, review script commands before execution, and prefer dry-run modes where available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dabin0927/skills/executive-briefing)
- [Style Guide](references/style-guide.md)
- [Narrative Methodology](references/narrative-methodology.md)
- [Structure Validation](references/structure-validation.md)
- [Collaboration Workflow](references/collaboration-workflow.md)
- [Edge Cases](references/edge-cases.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and guidance with optional JSON validation output and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or modify local report files through Python helper scripts.]

## Skill Version(s):

2.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
