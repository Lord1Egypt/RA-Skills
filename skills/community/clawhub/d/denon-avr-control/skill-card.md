## Description: <br>
Control a network-connected Denon AVR/AVC receiver over its classic IP control interface (TCP telnet-style commands or the goform HTTP endpoint), and expose local audio libraries through DLNA/UPnP for receiver playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yuqian-Shi](https://clawhub.ai/user/Yuqian-Shi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and home-theater operators use this skill to query and control Denon AVR/AVC receivers on a local network, including power, volume, mute, input selection, status checks, and model-specific raw commands. It can also help expose user-selected local music folders for playback through local output, DLNA push, or a minimal DLNA media server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send mutating commands to a Denon receiver, including power, volume, mute, input, and raw model-specific commands. <br>
Mitigation: Query receiver state first, confirm the intended receiver host, and send one mutating action at a time unless the user explicitly requests a batch. <br>
Risk: DLNA push and media-server modes can expose selected local music files on the local network. <br>
Mitigation: Use a dedicated music-only folder, avoid directories containing private files, verify the bind address and port, and stop playback or server processes when finished. <br>
Risk: Local firewalls, LAN reachability, and receiver codec support can make DLNA playback unreliable. <br>
Mitigation: Confirm the receiver and local machine are on the same LAN, allow only the needed local ports, and fall back to local computer playback or receiver control when DLNA playback fails. <br>


## Reference(s): <br>
- [Denon AVR IP Control Notes](references/commands.md) <br>
- [Local Audio Playback](references/local-playback.md) <br>
- [Experimental DLNA Push to a Denon Receiver](references/dlna-push.md) <br>
- [Real DLNA Media Server Mode](references/dlna-server.md) <br>
- [ClawHub Release Page](https://clawhub.ai/Yuqian-Shi/denon-avr-control) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include receiver hostnames or IP addresses, local music folder paths, port settings, and one-at-a-time command recommendations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
