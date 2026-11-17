## Description:

Evez Identity provides EVEZ mesh identity, infrastructure context, project status, and agent posture guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to provide an agent with EVEZ ecosystem identity, architecture context, active project status, and operational preferences. The skill is best treated as project reference that requires review before any setup, deployment, repository, memory, or bot action is performed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to adopt an autonomous identity and can encourage memory writes, repository publication, cloud provisioning, systemd deployment, or bot configuration.

Mitigation: Use the skill only as project reference in an isolated workspace and require explicit approval before high-impact operational actions.

Risk: The skill contains sensitive operational context and infrastructure identifiers.

Mitigation: Redact infrastructure identifiers before sharing outputs or deploying the skill in broader environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evezart/skills/evez-identity)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tables, status notes, and command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contains operational identity and infrastructure context; review before acting on setup guidance.]

## Skill Version(s):

1.0.0 (source: package.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
