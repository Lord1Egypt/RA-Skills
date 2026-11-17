## Description:

AI Agent Self-Reflection Engine that scans session logs, detects failure patterns, analyzes recurrence trends, and suggests automated fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qize-auto](https://clawhub.ai/user/qize-auto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use DreamCycle to inspect AI agent session logs, identify recurring failures and trends, and obtain suggested fixes after configuration or workflow changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session logs may contain secrets or sensitive operational data.

Mitigation: Run the skill only on approved session directories and redact sensitive log content before scanning.

Risk: The documented package install is not pinned to a specific package hash or artifact.

Mitigation: Install in a virtual environment and review the package or source before operational use.

Risk: Trend history is retained locally after scans.

Mitigation: Review or delete ~/.dreamcycle/scan_history.json when local retention is not desired.

## Reference(s):

- [DreamCycle ClawHub page](https://clawhub.ai/qize-auto/skills/dreamcycle)
- [DreamCycle project homepage](https://github.com/qize-auto/dreamcycle)
- [qize-auto publisher profile](https://clawhub.ai/user/qize-auto)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON diagnostic output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diagnostics may reference session-log paths and local trend history at ~/.dreamcycle/scan_history.json.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
