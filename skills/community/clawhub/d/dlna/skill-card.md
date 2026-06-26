## Description: <br>
Helps agents discover and control DLNA/UPnP media renderers such as smart TVs and speakers on a local network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxsdyhm](https://clawhub.ai/user/dxsdyhm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to help an agent build or operate DLNA/UPnP workflows for finding local media renderers, sending playable media URLs, controlling playback, querying status, and selecting default devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can discover and control DLNA/UPnP TVs or speakers on a local network. <br>
Mitigation: Use it only on networks and devices the operator is authorized to manage, and confirm the target device before sending playback, volume, or transport commands. <br>
Risk: Playback actions can send media URLs to local devices and change their current playback state. <br>
Mitigation: Verify the media URL, device identity, and expected playback effect before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dxsdyhm/dlna) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python, TOML, and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local network device discovery guidance and DLNA playback control code using async_upnp_client.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
