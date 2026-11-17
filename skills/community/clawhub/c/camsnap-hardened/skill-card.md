## Description:

Capture frames or clips from RTSP/ONVIF cameras.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide agents through local camera discovery, setup, snapshots, short clips, motion watching, and troubleshooting with the camsnap CLI while protecting camera credentials and footage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Homebrew install path uses an unpinned third-party tap for a camera-access tool.

Mitigation: Install only from a trusted camsnap tap, and prefer a pinned or otherwise verified camsnap release before deployment.

Risk: Camera credentials entered on command lines can be exposed through shell history, process lists, logs, or copied troubleshooting output.

Mitigation: Use credentials only with camsnap add, avoid echoing or reusing them in other commands, and keep them confined to the camsnap configuration workflow.

Risk: Snapshots, clips, and stream data may contain surveillance footage.

Mitigation: Keep captures local unless the user explicitly authorizes another destination, and do not pipe camsnap output to network-transmitting commands.

## Reference(s):

- [Camsnap homepage](https://camsnap.ai)
- [Faberlens camsnap safety evaluation](https://faberlens.ai/explore/camsnap)
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/camsnap-hardened)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the camsnap binary and ffmpeg on PATH; guidance should avoid exposing camera credentials, IP addresses, file paths, and footage unless explicitly needed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
