## Description: <br>
Control Spotify playback: play, pause, resume, skip, previous, restart, search, queue, set volume, shuffle, repeat, and view now-playing status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ejatapibeda](https://clawhub.ai/user/ejatapibeda) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to let an agent or terminal session control Spotify playback, search tracks and playlists, queue music, adjust playback settings, and report current player status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to extract Spotify browser session cookies and stores them locally. <br>
Mitigation: Treat sp_dc and sp_key like passwords, avoid exposing them in terminals or transcripts, restrict permissions on ~/.config/spotapi/session.json, and rotate sessions if cookies may have been disclosed. <br>
Risk: Spotify authentication and playback are handled through the external SpotAPI dependency. <br>
Mitigation: Review the dependency before installing and use the skill only if that dependency can be trusted with access to the Spotify browser session. <br>
Risk: Playback commands can be asynchronous and may not immediately reflect the actual device state. <br>
Mitigation: Check Spotify app or device state after command execution and allow longer timeouts for status, search, and playback operations. <br>


## Reference(s): <br>
- [ClawSpotify ClawHub page](https://clawhub.ai/ejatapibeda/clawspotify) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [SpotAPI dependency](https://github.com/ejatapibeda/SpotAPI) <br>
- [Spotify Web Player](https://open.spotify.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text CLI output with shell setup and invocation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, Python 3, SpotAPI, browser session cookies, an active Spotify account, and Spotify open on at least one device.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
