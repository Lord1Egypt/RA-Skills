## Description:

This skill helps an AIOS/OpenClaw agent record sanitized errors, corrections, reusable learnings, knowledge gaps, and improvement notes inside the current agent workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kadbbz](https://clawhub.ai/user/kadbbz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to preserve useful task learnings, command failures, user corrections, and repeatable practices for the current agent workspace. It is intended for workspace-local memory that avoids secrets, cross-agent content, and other senderId session files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be invoked automatically and persist session-derived learnings without explicit consent for each write.

Mitigation: Review this behavior before installation in privacy-sensitive workspaces; consider disabling implicit invocation or requiring explicit save requests.

Risk: Workspace memory can expose sensitive operational details if learnings include raw logs, secrets, configuration, or cross-senderId file evidence.

Mitigation: Record only sanitized summaries, minimal error fragments, and relative paths from the current senderId and current agent workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kadbbz/skills/aios-self-improving-agent)
- [Publisher profile](https://clawhub.ai/user/kadbbz)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and workspace-local Markdown log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes sanitized summaries under the current workspace's .learnings/ directory when invoked for memory capture.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
