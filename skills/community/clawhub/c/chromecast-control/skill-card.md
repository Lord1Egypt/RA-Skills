## Description: <br>
Control Chromecast devices on your local network - discover, cast media, control playback, manage queues, and save/restore states. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morozRed](https://clawhub.ai/user/morozRed) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and users with local Chromecast or Google Cast devices use this skill to discover devices, cast media, control playback and volume, manage YouTube queues, and save or restore playback state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can affect Chromecast or Google Cast devices on the local network, including shared devices. <br>
Mitigation: Use explicit device selection with `-d <device>` and confirm the target before casting, changing volume, or stopping playback. <br>
Risk: `catt save` and `catt restore` can preserve or replay prior playback state. <br>
Mitigation: Use state save and restore only when prior media and playback position are acceptable to expose or replay. <br>
Risk: Local file casting requires open TCP ports on the host. <br>
Mitigation: Use local file casting only on trusted networks and keep host firewall rules limited to the required casting ports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/morozRed/chromecast-control) <br>
- [catt project](https://github.com/skorokithakis/catt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the catt command-line tool and access to the same local network as the target Cast device.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
