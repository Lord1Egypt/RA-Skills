## Description:

Provides guidance for discovering and controlling DLNA/UPnP media renderers on a local network, including media playback, transport status, and default device setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxsdyhm](https://clawhub.ai/user/dxsdyhm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build agent workflows, CLIs, or Python utilities that discover DLNA devices on a trusted LAN and control playback, volume, seek, and status operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unvalidated device or media URLs could send unintended local-network requests or playback commands.

Mitigation: Limit control to devices found through trusted discovery and validate media URLs before issuing DLNA actions.

Risk: Playback, volume, or seek commands may target the wrong renderer on a shared network.

Mitigation: Require users or calling agents to confirm the target device before playback or volume changes.

Risk: Unescaped media titles or URLs in DIDL-Lite XML can produce malformed device commands.

Mitigation: Escape XML metadata before adapting the sample code for a CLI or agent workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dxsdyhm/skills/dlna)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs implementation guidance for local-network DLNA control; no external service calls or credentials are required by the skill itself.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
