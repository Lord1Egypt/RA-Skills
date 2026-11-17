## Description:

Agent Memes lets agents pick and send meme reaction images across chat platforms with the `memes` command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kagura-agent](https://clawhub.ai/user/kagura-agent)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to add lightweight visual reactions to chat workflows by selecting local meme images and sending them to supported messaging platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send external messages proactively when messaging credentials and targets are configured.

Mitigation: Require explicit confirmation for every send and avoid ambient default targets.

Risk: Unsafe scripts may misuse credentials or allow command injection.

Mitigation: Review or fix command-injection paths before deployment and limit credential scope to only the messaging platforms needed.

Risk: LINE local-file sending uploads private images to a third-party temporary hosting service.

Mitigation: Do not use LINE local-file sending for private images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kagura-agent/skills/agent-memes)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger outbound messaging API calls when the user or agent runs send commands with configured credentials.]

## Skill Version(s):

2.11.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
