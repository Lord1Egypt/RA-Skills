## Description: <br>
Control Devialet Phantom speakers via HTTP API for play/pause, volume control, mute/unmute, source selection, and speaker status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JGM2025](https://clawhub.ai/user/JGM2025) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to control Devialet Phantom, Dialog, and Mania speakers on a trusted local network, including playback, volume, source selection, status checks, and optional Spotify playback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control local Devialet speaker playback and volume over unauthenticated HTTP on the local network. <br>
Mitigation: Use it only on a trusted local network and verify the configured speaker IP before running commands. <br>
Risk: Spotify integration stores Spotify credentials and tokens in local configuration files. <br>
Mitigation: Protect the Spotify config and token files, use the least necessary Spotify scopes, and revoke the Spotify app token when it is no longer needed. <br>
Risk: Search-based Spotify playback may use desktop automation through xdotool. <br>
Mitigation: Prefer direct Spotify URIs or the scoped Spotify API helper when possible, and review desktop automation behavior before use. <br>


## Reference(s): <br>
- [Devialet HTTP API Reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/JGM2025/devialet) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local network HTTP API calls, Spotify desktop controls, or Spotify Web API calls when the user runs the provided scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
