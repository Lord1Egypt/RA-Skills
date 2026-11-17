## Description:

Enables an OpenClaw agent to choose fixed Haocun dance or selfie images from a user prompt and send them to messaging channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qidu](https://clawhub.ai/user/qidu)

### License/Terms of Use:

MIT

## Use Case:

External users and OpenClaw agent developers use this skill to add prompt-triggered dance and selfie image sending to an agent over supported messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change an OpenClaw agent's identity or persona.

Mitigation: Review installation behavior before use, back up existing persona files, and preview or approve persona changes before applying them.

Risk: The skill can send media through messaging integrations.

Mitigation: Require explicit confirmation for each outbound send and validate the channel, target, media URL, gateway URL, and token configuration.

Risk: The declared tool permissions are broader than the selfie-sending feature requires.

Mitigation: Narrow runtime permissions to the minimum commands and file access needed for OpenClaw messaging and local configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qidu/skills/get-up)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [Clawra project](https://clawra.dev/)
- [Hosted image assets](https://cdn.jsdelivr.net/gh/christoagent/haoclaw@main/assets/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send media through OpenClaw messaging integrations when invoked with channel and target details.]

## Skill Version(s):

1.0.5 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
