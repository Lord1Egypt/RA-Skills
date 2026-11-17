## Description:

Convert text into high-quality, emotional speech reading using Kling TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to invoke dLazy's Kling TTS wrapper for generating Chinese or English speech from text prompts with selectable voice, speed, format, and asynchronous execution options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires running the external dLazy npm CLI.

Mitigation: Prefer the pinned on-demand npx invocation or review the CLI source before installing it globally.

Risk: A dLazy API key is required and may be stored in local CLI configuration or supplied through the environment.

Mitigation: Do not paste real API keys into chat; use the CLI login or auth flow and rotate the key if it is exposed.

Risk: Text prompts and selected generation parameters are sent to dLazy's hosted service.

Mitigation: Avoid submitting sensitive text unless the user accepts dLazy's hosted processing model.

Risk: The artifact's output example shows an image result even though the skill is for text-to-speech.

Mitigation: Treat generated results as audio outputs and verify returned MIME types or URLs before downstream use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/dlazy-keling-tts)
- [dLazy publisher profile](https://clawhub.ai/user/dlazyai)
- [dLazy CLI homepage](https://github.com/dlazyai/cli)
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, text]

**Output Format:** [Markdown guidance with inline shell commands; CLI invocations return JSON result records for generated audio.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports mp3 or wav output, synchronous waiting or asynchronous task IDs, and hosted result URLs from dLazy.]

## Skill Version(s):

1.3.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
