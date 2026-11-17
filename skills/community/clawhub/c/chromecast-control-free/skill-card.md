## Description: <br>
Controls Chromecast-compatible devices on a local network with catt for device discovery, basic media casting, playback control, and volume adjustment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover Chromecast-compatible devices on a trusted local network, cast supported media, and issue basic playback or volume commands through catt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control Chromecast-compatible devices on the local network and includes command/write capability. <br>
Mitigation: Review before installing, use only on trusted private networks, specify the intended device name or IP address, and avoid sharing credentials or sensitive device information. <br>
Risk: The artifact contains unrelated API and file-processing boilerplate that could be mistaken for broader authorization. <br>
Mitigation: Limit use to the Chromecast control workflow described by the release evidence and security guidance, and reject unrelated API, credential, or file-processing actions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include device names, IP addresses, command results, error details, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
