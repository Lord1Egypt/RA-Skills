## Description:

Systematic 4R framework for AI agent error diagnosis, retry, recovery, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to handle tool failures, timeouts, permission errors, missing files, API errors, and process failures through a structured record, reason, recover, and report workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill can steer agents toward elevated permissions and side-effecting upload paths without clear approval or scoping.

Mitigation: Treat remediation steps as suggestions and require user approval before sudo, chmod, API uploads, credential changes, or other state-changing alternatives.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aptratcn/skills/error-recovery-xiaobai)
- [README.md](artifact/README.md)
- [README_EN.md](artifact/README_EN.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first workflow with an English README summary; remediation steps are advisory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
