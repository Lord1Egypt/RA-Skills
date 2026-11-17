## Description:

Connects voice transcripts and agent responses through the hotbutter.ai hosted relay for remote voice interaction with OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michael-stajer](https://clawhub.ai/user/michael-stajer)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to connect a local OpenClaw agent to a browser-based voice session through a hosted relay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted relay receives voice transcripts and agent responses and can submit prompts to the local OpenClaw agent while the bridge is running.

Mitigation: Use the skill only for non-sensitive work, prefer a self-hosted relay or local alternative, and avoid pairing it with agents that have broad file, shell, credential, or account access.

Risk: Install and dependency steps are not tightly verifiable.

Mitigation: Install only from a versioned artifact with integrity checks and lockfile-backed dependencies.

## Reference(s):

- [hotbutter-os local alternative](https://github.com/hotbutter-ai/hotbutter-os)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the openclaw CLI and a WebSocket relay URL; defaults to the hosted hotbutter.ai relay.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
