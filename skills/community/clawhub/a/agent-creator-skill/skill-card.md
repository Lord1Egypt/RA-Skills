## Description:

Automatically create a new OpenClaw agent, translate its name, and initialize its persona/system prompt based on user requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freesaber](https://clawhub.ai/user/freesaber)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agent developers use this skill to create durable peer agents from natural-language role requests, including agent IDs, display names, and detailed identity prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent peer agents and stores generated operating instructions without a clear confirmation or review step.

Mitigation: Before each run, require the agent to show the exact agent ID, display name, workspace path, and full identity prompt, then approve execution explicitly.

Risk: Untrusted or copied prompt text could be injected into a durable agent identity.

Mitigation: Avoid using the skill with untrusted prompt text and review the generated identity prompt before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freesaber/skills/agent-creator-skill)
- [README](artifact/README.md)
- [README zh-CN](artifact/README.zh-CN.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with generated command arguments and shell execution steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent OpenClaw agent configuration and injects a generated identity prompt when executed.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
