## Description:

Record, track, and analyze personal or professional decisions with structured reflection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to record decisions, compare options, schedule reviews, and analyze decision patterns over time. It supports personal and professional reflection but is not intended for crisis support or licensed medical, legal, or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decision records are stored locally in plaintext and may contain sensitive personal or professional information.

Mitigation: Use the skill only on trusted machines, protect ~/.openclaw/decisions with appropriate OS permissions, and avoid recording information that should not be stored locally.

Risk: The skill can be misapplied to crisis, medical, legal, or investment-advice situations.

Mitigation: Stop the normal decision-journal workflow for those situations and route the user to qualified professional or emergency support.

Risk: CSV exports may expose sensitive decision history or create spreadsheet-handling risks.

Mitigation: Treat exported files as sensitive, share them carefully, and open CSV files only in trusted spreadsheet environments.

## Reference(s):

- [Decision Analysis](references/analysis.md)
- [Decision Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, CLI commands, JSON, Markdown, and CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores decision, review, pattern, and index files under ~/.openclaw/decisions by default.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
