## Description:

You are an incident response expert specializing in production debugging, log analysis, root cause analysis, and rapid system recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and on-call operators use this skill to triage production incidents, analyze logs and traces, identify root causes, propose mitigations, and document incident response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes high-impact production commands and automatic remediation examples.

Mitigation: Require human approval before executing production changes, rollbacks, cache clearing, cleanup, or remediation commands.

Risk: Debug containers and operational commands can broaden access to production systems.

Mitigation: Pin and restrict debug container images and limit command execution to authorized operators and scoped environments.

Risk: Cleanup or rollback actions can remove evidence needed for diagnosis.

Mitigation: Preserve relevant logs, traces, metrics, and incident notes before cleanup or rollback actions.

## Reference(s):

- [Incident Responder Code Examples](references/examples.md)
- [ClawHub Skill Release](https://clawhub.ai/mtsatryan/skills/ah-incident-responder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with incident assessments, runbook steps, diagnostic commands, code examples, and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory incident-response material; production changes should require human approval]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
