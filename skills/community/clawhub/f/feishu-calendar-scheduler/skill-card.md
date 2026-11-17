## Description:

Recommends Feishu meeting times, supports batch schedule management, and generates meeting reports for OpenClaw users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2389275723](https://clawhub.ai/user/2389275723)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to automate Feishu calendar scheduling workflows, including meeting time recommendations, batch meeting management, and meeting-report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled publishing tooling includes hard-coded credential material.

Mitigation: Remove the embedded token from the artifact and rotate any exposed ClawHub credential before use.

Risk: Publishing tooling can upload broad sets of local skill files.

Mitigation: Require explicit user confirmation and a file allowlist before any upload or publication action.

Risk: Installation and helper scripts may be unsafe on machines with sensitive files.

Mitigation: Review the scripts first and run installation only in an isolated environment or a least-privilege workspace.

Risk: Bulk calendar actions can create, modify, or cancel meetings at scale.

Mitigation: Preview affected events and require explicit confirmation before performing any bulk calendar operation.

Risk: Artifact fixtures include real-looking license and user data.

Mitigation: Remove fixture data from release packages or replace it with clearly synthetic examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2389275723/skills/feishu-calendar-scheduler)
- [ClawHub documentation](https://docs.clawhub.com/skills/feishu-calendar-scheduler)
- [ClawHub publisher profile](https://clawhub.ai/user/2389275723)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate calendar recommendations, command examples, configuration files, and report-export guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact package metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
