## Description:

This skill helps developers analyze local Git repository collaboration patterns and produce repository-level aggregate reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect a local Git repository and generate aggregate collaboration reports covering commit cadence, code churn, conventional commit compliance, and file-level bus-factor indicators. It is intended for repository workflow insight, not personal performance evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Declared write tooling and save/delete-style instructions conflict with the skill's read-only privacy claims.

Mitigation: Remove the write tool declaration and generic create, modify, delete, save, and import instructions before relying on read-only behavior.

Risk: Generic network troubleshooting text conflicts with the local, zero-network operating posture described by the skill.

Mitigation: Narrow triggers to explicit local Git repository analysis and delete generic network troubleshooting instructions.

Risk: Local command execution over repository paths can expose commit metadata or run broader commands if parameters are not constrained.

Mitigation: Require user-confirmed absolute repository paths, dry-run command review, and a reviewed read-only git command whitelist.

## Reference(s):

- [Artifact SKILL.md](artifact/SKILL.md)
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/actor-identifier-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Repository-level aggregate metrics; file-level bus-factor notes may include contributor names.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
