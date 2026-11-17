## Description:

Use this skill to work through prioritized findings from an audit report, applying focused fixes and verifying each one.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use Expedite to execute prioritized findings from an audit backlog. It guides focused code changes, verification of each fix, and reporting of completed, skipped, parked, or remaining work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository edits, tests, and commits may introduce unintended changes.

Mitigation: Review the audit backlog and resulting diffs, and inspect test results before accepting the changes.

Risk: Referenced helper skills or lint scripts may have behavior that has not been reviewed.

Mitigation: Review referenced helper skills and scripts separately before relying on them.

## Reference(s):

- [Expedite on ClawHub](https://clawhub.ai/solomonneas/skills/expedite)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Markdown, Guidance]

**Output Format:** [Repository code changes and a Markdown progress report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focused changes are verified one finding at a time; unresolved items are reported as parked or remaining.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
