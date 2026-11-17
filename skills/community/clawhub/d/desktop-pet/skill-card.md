## Description:

Gives OpenClaw a tiny desktop companion with a fluid glass-ball presence, voice output, eye expressions, desktop lyrics overlay, and mood colors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kk43994](https://clawhub.ai/user/kk43994)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to install and configure a desktop companion that displays agent presence, speech, expressions, and message overlays on the desktop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users run mutable external code and npm dependencies from a project repository.

Mitigation: Install only from a trusted source, pin to a known commit or release, and inspect dependencies before running npm install.

Risk: MiniMax voice cloning and Feishu/Lark sync can send voice or message data to cloud services.

Mitigation: Enable integrations only when needed, review their data handling, and avoid sending sensitive conversations or voice samples.

Risk: The skill asks for an API key in local configuration.

Mitigation: Keep API keys out of version control, use restricted credentials, and rotate them if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kk43994/skills/desktop-pet)
- [Project homepage](https://github.com/kk43994/claw-desktop-pet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup commands, runtime guidance, and configuration examples for optional voice integration.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
