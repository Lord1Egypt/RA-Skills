## Description:

Simple model router for OpenClaw. Switch between available models based on task type. No manual config needed - just use natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siliconyahaha](https://clawhub.ai/user/siliconyahaha)

### License/Terms of Use:

MIT License

## Use Case:

OpenClaw users and developers use this skill to switch between supported models, check the active model, and route image, file, PDF, screenshot, and fallback tasks to the configured OpenClaw model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Always-on natural-language routing can change the active OpenClaw model on broad task descriptions.

Mitigation: Require an explicit switch command or confirmation before mutating model configuration.

Risk: Model switching restarts the OpenClaw gateway, which can interrupt active local workflows.

Mitigation: Notify the user before restart and run the restart only after the requested model is validated as available.

## Reference(s):

- [Claw Switch ClawHub Skill Page](https://clawhub.ai/siliconyahaha/skills/claw-switch)
- [siliconyahaha Publisher Profile](https://clawhub.ai/user/siliconyahaha)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text responses with shell commands for OpenClaw model changes and gateway restart steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes only to configured available models and returns concise confirmation or help text.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact documentation also mentions v2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
