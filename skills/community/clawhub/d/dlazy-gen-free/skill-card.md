## Description:

Dlazy Generate helps an agent choose and run dLazy CLI models to generate or transform images, video, and audio from user prompts or supplied media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and agent users use this skill to route image, video, or audio generation and editing requests to an appropriate dLazy CLI model. It supports authentication guidance, command execution, CLI help lookup, and piping JSON results between dLazy commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run external CLI commands for media generation.

Mitigation: Review the selected dLazy command and model-specific help output before execution.

Risk: Prompts and selected local media files may be sent to dLazy-hosted services.

Mitigation: Use only media and voices the user has rights or consent to process, and avoid sensitive files unless upload is intended.

Risk: Authentication may persist an API key in local CLI configuration.

Mitigation: Use the DLAZY_API_KEY environment variable for per-invocation credentials when persistent key storage is not desired.

Risk: The artifact and security summary note under-scoped or inconsistent setup details.

Mitigation: Confirm the intended @dlazy/cli version and authentication method before installing or running the CLI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dlazy-gen-free)
- [dLazy homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is returned through dLazy-hosted URLs when the CLI call succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
