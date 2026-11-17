## Description:

Quickly sends local images to a specified channel, copying small images directly and auto-compressing large images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deadlining](https://clawhub.ai/user/deadlining)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use this skill to send local image files to a named messaging channel or recipient, with compression for files at or above 10 MB.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell-interpreted input in the send helper can make channel, target, or message values unsafe to pass through execution.

Mitigation: Remove shell interpretation or otherwise prevent shell parsing, and validate channel and target values before use.

Risk: The staging path behavior can create unsafe or unreliable media handling.

Mitigation: Use a unique home-directory-based staging directory and clean generated media after successful sends.

Risk: Unpinned dependencies can change behavior across installs.

Mitigation: Pin runtime dependencies, including image-processing and CLI dependencies, before release.

## Reference(s):

- [Fast Image ClawHub listing](https://clawhub.ai/deadlining/skills/fast-image)

## Skill Output:

**Output Type(s):** [shell commands, text]

**Output Format:** [CLI output and messaging-side media delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one local image path with channel, target, and optional message arguments.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
