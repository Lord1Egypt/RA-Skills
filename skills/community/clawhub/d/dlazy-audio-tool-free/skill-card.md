## Description:

A lightweight text-to-speech and basic sound-effect generation skill for personal content creation, supporting multilingual TTS through the dlazy CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to generate narration, audiobook-style reading, and simple sound effects from text prompts through a third-party audio CLI and hosted audio service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes a third-party CLI and cloud audio service.

Mitigation: Review proposed commands before execution and use the skill only for explicit TTS or sound-effect generation tasks.

Risk: API key handling may expose credentials if keys are persisted locally or included in generated commands.

Mitigation: Prefer DLAZY_API_KEY as an environment variable and avoid hardcoding or storing keys in shared files.

Risk: Input text and hosted output URLs may be processed by or exposed through the dlazy service.

Mitigation: Do not send private scripts, business text, regulated content, or other sensitive material unless that processing is acceptable.

Risk: The skill text includes broader triggers than the stated audio-generation purpose.

Mitigation: Constrain use to text-to-speech and sound-effect generation rather than translation, media conversion, or general file-processing workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dlazy-audio-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or link to generated audio files through the dlazy service.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
