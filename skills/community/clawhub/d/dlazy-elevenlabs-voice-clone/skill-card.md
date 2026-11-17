## Description:

Clones a custom ElevenLabs voice from a clean audio sample for use with text-to-speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use the skill to create a custom voice from a clean sample for ElevenLabs text-to-speech. It sends the request through dLazy's hosted service and returns a result or asynchronous task status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial and flags that the reported login command is not linked to the skill's stated voice-cloning purpose in the scan evidence.

Mitigation: Review the CLI login behavior and confirm it matches your expectations before installing or signing in.

Risk: The skill sends audio samples to a hosted service for voice cloning.

Mitigation: Use samples you have permission to clone, avoid sensitive recordings, and review the service's data terms before uploading.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dlazyai/skills/dlazy-elevenlabs-voice-clone)
- [CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [CLI homepage listed in release metadata](https://github.com/dlazy-ai/cli)

## Skill Output:

**Output Type(s):** [API Calls, Audio, JSON, Guidance]

**Output Format:** [JSON result with output details or asynchronous task status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Voice-cloning requests may return immediately with a task identifier when asynchronous mode is used.]

## Skill Version(s):

1.3.41 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
