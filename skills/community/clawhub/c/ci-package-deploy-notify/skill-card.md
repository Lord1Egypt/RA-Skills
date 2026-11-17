## Description:

Triggers approved Jenkins CI/CD package or deployment jobs for selected services and sends a Feishu notification after successful completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunyang777](https://clawhub.ai/user/sunyang777)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release operators use this skill to trigger Jenkins CI/CD packaging or deployment for configured services in dev, test, demo, or sit environments. The skill waits for job completion and sends one Feishu summary notification for successful services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published artifact includes live Jenkins and Feishu credentials.

Mitigation: Do not install it as-is; rotate the exposed secrets, remove credentials from the package, and load them from a protected runtime secret source.

Risk: Jenkins credentials may be sent when following unvalidated Jenkins queue or build URLs.

Mitigation: Validate Jenkins queue and build URLs before attaching credentials and use a narrowly scoped service account limited to the intended jobs.

Risk: The skill can trigger CI/CD jobs and send deployment notifications when invoked with actionable release parameters.

Mitigation: Require an explicit user request, validate repositories, branch or environment, and change description before execution, and reject unsupported production or master targets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunyang777/skills/ci-package-deploy-notify)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text status summary with shell command invocation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires selected repositories, branch or environment, change description, optional job type, optional SQA mentions, and initiator identity.]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
