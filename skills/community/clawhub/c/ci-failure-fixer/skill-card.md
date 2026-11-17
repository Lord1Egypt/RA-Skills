## Description:

Monitor GitHub Actions CI pipelines for failures and automatically fix common issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielgrobelny](https://clawhub.ai/user/danielgrobelny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to watch GitHub Actions runs, diagnose failed builds, apply known safe fixes for common failure patterns, and report cases that need human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead agents to make and push unattended repository changes with weak scope controls.

Mitigation: Use a dedicated low-privilege GitHub identity, set an explicit CI_REPOS allowlist, avoid unattended cron auto-repair, and require human review before commits or pushes.

Risk: The security scan reports a real script injection flaw.

Mitigation: Review and harden script inputs before deployment, and run the skill only in trusted repositories until the issue is fixed.

Risk: Token and authentication failures require secret rotation or updates that should not be automated by the skill.

Mitigation: Report credential failures for manual handling by an authorized operator.

Risk: An attacker-controlled CI_STATE_FILE path could affect local state handling.

Mitigation: Keep CI_STATE_FILE controlled by trusted operators and do not expose it to untrusted input.

## Reference(s):

- [CI Failure Fix Patterns](references/fix-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and diagnostic text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository-specific CI status, proposed fixes, pushed changes, or report-only diagnoses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
