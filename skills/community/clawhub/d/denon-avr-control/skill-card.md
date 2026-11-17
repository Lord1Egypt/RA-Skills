## Description:

Control a network-connected Denon AVR/AVC receiver over its classic IP control interface (TCP telnet-style commands or the goform HTTP endpoint), and expose local audio libraries through DLNA/UPnP for receiver playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuqian-shi](https://clawhub.ai/user/yuqian-shi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and home-theater users use this skill to query and control Denon AVR/AVC receivers on a local network and to serve user-chosen local audio libraries for receiver playback through DLNA/UPnP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DLNA and temporary HTTP server modes can expose selected local audio files or folders on the LAN.

Mitigation: Use only dedicated media folders, bind the server to a trusted LAN interface, keep firewall exposure narrow, and stop the server when playback is finished.

Risk: Raw receiver commands and mutating controls can change receiver power, input, mute, and volume.

Mitigation: Query receiver status first, send one mutating action at a time, and use raw commands only when the target Denon model and command are understood.

## Reference(s):

- [Denon AVR IP Control Notes](references/commands.md)
- [Experimental DLNA push to a Denon receiver](references/dlna-push.md)
- [Real DLNA media server mode](references/dlna-server.md)
- [Local audio playback on the computer](references/local-playback.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May operate local playback, receiver-control, and DLNA helper scripts when the agent has user-provided host and folder inputs.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
