## Description:

Provides a knowledge transfer protocol for giving newly created or migrated OpenClaw agents complete identity, skills, memory, context, and required workspace access before activation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stefanferreira](https://clawhub.ai/user/stefanferreira)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to prepare OpenClaw agents by transferring identity files, user context, system knowledge, skills documentation, memory files, and role-appropriate tool access before activation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The protocol can copy sensitive user profile, memory, history, and tool-context files into agent workspaces.

Mitigation: Transfer only files each agent needs, redact private or secret information before transfer, and apply retention and access controls to copied workspace data.

Risk: Bulk transfers can spread unnecessary context to multiple agents.

Mitigation: Avoid bulk --all transfers by default and approve each target agent's file set before running transfer commands.

Risk: Shell snippets rely on operator-provided agent names and workspace paths.

Mitigation: Validate agent names and paths before execution, and use the skill only in trusted OpenClaw environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stefanferreira/skills/agent-knowledge-transfer)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with checklists, shell command snippets, configuration examples, and verification questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires operator review before copying user profile, memory, history, and tool-context files into agent workspaces.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
