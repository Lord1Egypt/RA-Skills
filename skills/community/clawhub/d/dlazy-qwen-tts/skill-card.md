## Description:

Generates speech from text with Alibaba Bailian Qwen3-TTS, using curated system voices or a custom voice description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can turn text into speech with a selected system voice or a voice described in natural language. The skill returns a generated audio asset or a link to it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial: the CLI package and related files were unavailable for review, and the CLI login behavior was not established by the scan.

Mitigation: Review the CLI package and confirm its credential flow before signing in or providing an API key.

Risk: The skill sends prompts to dLazy’s hosted API, and its CLI login stores an API key in local CLI configuration.

Mitigation: Avoid sending sensitive text unless that use is approved, protect the local API key, and rotate or revoke it if exposed.

## Reference(s):

- [CLI homepage (metadata.clawdis)](https://github.com/dlazy-ai/cli)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)
- [ClawHub release page](https://clawhub.ai/dlazyai/skills/dlazy-qwen-tts)

## Skill Output:

**Output Type(s):** [Audio, JSON]

**Output Format:** [Generated speech audio asset or hosted audio URL, with result metadata in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio may be saved locally; asynchronous requests may return a task identifier before the asset is ready.]

## Skill Version(s):

1.3.41 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
