## Description:

Claude Code Connector lets an agent send prompt text to Claude Code through an ACP bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[partigle](https://clawhub.ai/user/partigle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to delegate prompt-based tasks, such as file or project analysis, to Claude Code through a local ACP bridge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated prompt content may leave the current agent boundary when sent to Claude Code.

Mitigation: Avoid sending secrets, private files, or sensitive project context unless the user is comfortable with that data being handled by Claude Code.

Risk: The skill depends on a local ACP bridge script outside the bundled artifact.

Mitigation: Review and trust the local bridge script separately before installation or use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/partigle/skills/claude-code-connector)
- [Bundled Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Prompt-dependent text returned from Claude Code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill forwards a user-provided prompt to a local Claude Code ACP bridge.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
