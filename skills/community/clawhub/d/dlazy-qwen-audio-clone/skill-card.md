## Description:

Alibaba Bailian qwen3-tts voice cloning lets users upload a clean voice sample and create a custom voice for later text-to-speech calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can submit a clean voice sample to create a custom voice for subsequent text-to-speech use through dLazy's hosted service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports an unclear CLI login step and incomplete evidence for some referenced items; its benign verdict has medium confidence.

Mitigation: Review the pinned CLI install details and login flow before authenticating, and confirm that the package and service are the ones you intend to use.

Risk: The skill documentation says local audio samples are uploaded to dLazy media storage for processing, which can expose personal or sensitive voice recordings to a hosted service.

Mitigation: Use only recordings you have permission to submit, avoid sensitive material, and check the service terms and data handling details before uploading.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-qwen-audio-clone)
- [Publisher profile: dlazyai](https://clawhub.ai/user/dlazyai)
- [CLI source listed in skill metadata (GitHub import provenance unavailable)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [Structured JSON API response describing the voice-cloning result or asynchronous task status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A completed response may include a result URL; asynchronous responses may include a task identifier and status.]

## Skill Version(s):

1.3.43 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
