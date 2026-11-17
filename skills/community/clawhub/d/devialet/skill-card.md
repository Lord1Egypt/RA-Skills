## Description:

Control Devialet Phantom speakers via HTTP API for play/pause, volume control, mute/unmute, source selection, and speaker status on supported Devialet firmware.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jgm2025](https://clawhub.ai/user/jgm2025)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to control Devialet Phantom, Reactor, Dialog, and Mania speakers on a trusted local network, including playback, volume, source, status, and optional Spotify playback workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control Spotify playback and automate a local Spotify desktop session.

Mitigation: Install it only if Spotify playback-control access is acceptable, and remove or avoid spotify.sh when Spotify integration is not needed.

Risk: Spotify token handling is flagged as insecure by the security evidence.

Mitigation: Store credentials and tokens with restrictive file permissions and review token storage before using the skill in automation.

Risk: Devialet speaker control uses unauthenticated HTTP on the local network.

Mitigation: Use the skill only on a trusted LAN and avoid exposing Devialet control endpoints beyond the local network.

Risk: Volume input validation needs review before automated use.

Mitigation: Constrain volume values to the documented 0-100 range in any agent workflow that calls the scripts.

## Reference(s):

- [Devialet HTTP API Reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/jgm2025/skills/devialet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local-network HTTP API commands and Spotify setup guidance; users must supply their own speaker IP address and optional Spotify credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
