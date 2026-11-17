## Description:

Edge TTS 中文定制版，包含儿童配音预设，生成后自动发送到对话。

This skill is ready for commercial/non-commercial use.

## Publisher:

[systiger](https://clawhub.ai/user/systiger)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to generate Chinese MP3 voiceovers with adult and child-oriented Edge TTS presets, then return the generated audio to the conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically send generated audio back into the conversation, including audio derived from sensitive text.

Mitigation: Review input text before synthesis and prefer deployments that ask for confirmation before sending generated audio.

Risk: The package depends on mutable external Edge TTS code and scripts that are not fully pinned in this release.

Mitigation: Pin and review dependencies before deployment, and install only after accepting the external script execution risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/systiger/skills/edge-tts-kids)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline JavaScript and shell command examples; generated audio is MP3.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Chinese Edge TTS voice presets and depends on external edge-tts scripts plus network access.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill-info.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
