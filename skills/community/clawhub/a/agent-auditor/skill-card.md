## Description:

Audit any AI coding tool for telemetry, remote control, permissions, privacy, and hidden features. Generates a graded report (A-F).

This skill is ready for commercial/non-commercial use.

## Publisher:

[mackding](https://clawhub.ai/user/mackding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to audit AI coding tool source trees for telemetry, remote control mechanisms, permission behavior, privacy impact, hidden features, and related recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable third-party npm audit code over target source trees without version pinning, lockfiles, or integrity controls.

Mitigation: Use a pinned and audited package version or lockfile-managed install, and run it in a restricted environment with read-only access to the intended source.

Risk: Audit execution may access source contents that should not be exposed to unnecessary tools or environments.

Mitigation: Run the audit without unnecessary secrets or network access and limit filesystem access to the intended source tree.

## Reference(s):

- [Agent Auditor on ClawHub](https://clawhub.ai/mackding/skills/agent-auditor)
- [Publisher profile: mackding](https://clawhub.ai/user/mackding)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Structured audit report with graded findings, evidence locations, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local npm audit tooling against a target source directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
