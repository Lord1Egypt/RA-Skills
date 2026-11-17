## Description:

Provides ByteRover CLI guidance for agents to query, curate, and optionally sync project knowledge stored as Markdown files in `.brv/context-tree` through a configured LLM provider.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratiknarola](https://clawhub.ai/user/pratiknarola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let agents retrieve project context before work and save durable implementation patterns or decisions after work. It is intended for projects that want reusable, local Markdown-based memory with optional provider-backed processing and cloud sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to send project context and optional file contents through a configured external LLM provider.

Mitigation: Use the skill deliberately, review query and curate inputs before execution, and avoid secrets, personal data, or sensitive files.

Risk: The skill persists memory as Markdown under `.brv/context-tree`, which may be committed to repository history.

Mitigation: Review generated memory files before committing and exclude sensitive content from stored context.

Risk: Global installation of a third-party CLI and optional cloud sync expand trust and data exposure.

Mitigation: Prefer pinned and verified package installation, and run cloud sync commands only after reviewing what will be pushed or pulled.

## Reference(s):

- [ByteRover Context Tree ClawHub listing](https://clawhub.ai/pratiknarola/skills/byterover-context-tree)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing instructions for running ByteRover CLI query, curate, provider setup, and optional sync commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
