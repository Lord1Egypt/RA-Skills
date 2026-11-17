## Description:

Captures learnings, errors, corrections, and feature requests so coding agents can review recurring lessons and promote reviewed guidance into project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kondifun](https://clawhub.ai/user/kondifun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record command failures, user corrections, knowledge gaps, and feature requests in markdown learning logs. Reviewed lessons can then be promoted into project or workspace guidance for future agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs may capture sensitive conversation details, secrets, or personal data.

Mitigation: Redact secrets and personal data before logging, and keep `.learnings/` out of version control unless entries have been reviewed.

Risk: Promoting learnings into future-agent instruction files can introduce incorrect or misleading guidance.

Mitigation: Require an explicit diff review before promoting entries into agent instruction files or extracting a new skill.

Risk: Broad hook-based reminders can affect many sessions if installed globally.

Mitigation: Prefer project-local setup and avoid global hooks unless the behavior is intentionally desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kondifun/skills/artefact-144794445)
- [Entry Examples](references/examples.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or updates markdown learning logs and may propose reviewed updates to agent instruction files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
