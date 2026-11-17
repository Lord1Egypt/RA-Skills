## Description:

Use when someone wants to install, configure, onboard, script, or troubleshoot the ricebowl.ai-first ai-media CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinchanzis](https://clawhub.ai/user/jinchanzis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to install and configure the ai-media CLI, onboard to ricebowl.ai, and generate or inspect image and video tasks with scriptable commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys could be exposed through chat transcripts, logs, shell history, or shared configuration files.

Mitigation: Use a dedicated limited API key, avoid pasting real keys into chat or logs, and rotate or revoke keys if exposure is suspected.

Risk: Prompts, media URLs, uploaded images, and metadata may be sent to ricebowl.ai during image or video generation workflows.

Mitigation: Submit confidential content only after ricebowl.ai is approved for that data and the user understands the external processing path.

Risk: Installing the wrong package or using an unexpected publisher could execute unintended CLI code.

Mitigation: Verify that ai-media-generator is the intended package from the expected publisher and prefer an isolated, non-admin install.

## Reference(s):

- [ai-media CLI Commands](artifact/references/cli-commands.md)
- [Platform Onboarding](artifact/references/platform-onboarding.md)
- [ai-media-generator homepage](https://github.com/214140846/ai-media-generator)
- [ricebowl.ai](https://ricebowl.ai)
- [ricebowl.ai pricing](https://ricebowl.ai/pricing)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API-key handling guidance, CLI command sequences, and model-specific parameter examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
