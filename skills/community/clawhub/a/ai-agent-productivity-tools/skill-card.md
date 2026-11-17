## Description:

Curated toolkit for business productivity with installation guidance for Google Workspace CLI, task management, notes, health checks, and security scanning tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[certainlogicai](https://clawhub.ai/user/certainlogicai)

### License/Terms of Use:

Business Source License 1.1

## Use Case:

Business users and agent operators use this skill to guide setup of a productivity stack for email, calendar, notes, task management, health checks, and skill scanning. It is documentation-oriented and helps agents propose installation and configuration steps rather than providing automation code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides agents toward installing and authenticating multiple unpinned third-party tools that may access sensitive Google Workspace and Notion data.

Mitigation: Review each dependency's publisher, version, requested permissions, and OAuth/API scopes before installation; prefer pinned or verified releases.

Risk: Productivity tools may receive broad workspace, calendar, document, or notes access during setup.

Mitigation: Start with least-privilege or read-only access where possible and expand permissions only after confirming the workflow requires them.

Risk: The sample context store pattern could expose secrets or sensitive business content if copied directly.

Mitigation: Avoid storing secrets or sensitive content in the sample context.jsonl pattern unless access controls, retention limits, and redaction are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/certainlogicai/skills/ai-agent-productivity-tools)
- [README](README.md)
- [Personal Assistant Build Guide](PA_GUIDE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Tone Guide](docs/TONE_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no automated tool execution is included.]

## Skill Version(s):

1.0.1 (source: target metadata and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
