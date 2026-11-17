## Description:

Send customized voice messages to Feishu chats by generating and uploading TTS audio with configurable credentials and voice options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuwudou](https://clawhub.ai/user/jisuwudou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate shell-based workflows for sending Feishu audio messages with configurable app credentials, chat IDs, default text, and TTS voice settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Edge TTS script has an input-handling flaw that can execute arbitrary local code.

Mitigation: Review and fix the Edge TTS input handling before use, and avoid running that script with untrusted message text or voice values.

Risk: The script may install Python packages at runtime without pinned versions.

Mitigation: Install dependencies explicitly in an isolated environment with pinned versions instead of allowing automatic pip installation.

Risk: Feishu credentials are stored in a local configuration file.

Mitigation: Use only non-sensitive message content, create the Feishu config file with private permissions, and prefer environment overrides for temporary credentials.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Feishu voice-message configuration and shell-script guidance for agent use.]

## Skill Version(s):

1.0.0 (source: target metadata and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
