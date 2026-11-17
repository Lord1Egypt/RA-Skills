## Description:

Connects to a user-deployed audiolla server for audio processing, analysis, and MIDI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and audio engineers use this skill when the user explicitly requests Audiolla and has a running server, to process or analyze audio and create or transform MIDI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial: one of two components was fully inspected, and the skill manifest could not be parsed.

Mitigation: Treat the benign verdict as limited coverage and review the complete release before deployment.

Risk: The documented latest Docker image tags can resolve to changing builds.

Mitigation: Pin any Docker image used to a specific tag or digest.

Risk: Enabling remote URL fetch or upload adds an SSRF surface.

Mitigation: Keep URL I/O disabled unless needed; when enabled, use an allowlist and retain private-address blocking.

## Reference(s):

- [Audiolla ClawHub release](https://clawhub.ai/psyb0t/skills/audiolla)
- [Audiolla API reference](https://psyb0t.github.io/docker-audiolla/api/)
- [Setup guide](references/setup.md)

## Skill Output:

**Output Type(s):** [API calls, Analysis, Audio and MIDI files, Images and video]

**Output Format:** [JSON API requests and responses; audio, MIDI, image, or video files when supported by the server]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available operations and outputs depend on the deployed Audiolla server and its configured engines.]

## Skill Version(s):

2.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
