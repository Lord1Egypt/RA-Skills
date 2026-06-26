## Description: <br>
Capture frames or clips from RTSP/ONVIF cameras. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xspeter](https://clawhub.ai/user/0xspeter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate camsnap setup and command guidance for discovering RTSP/ONVIF cameras and capturing snapshots, short clips, or motion events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks this release as suspicious and recommends trusted-workspace installation. <br>
Mitigation: Install only in a trusted maintainer workspace, review behavior before use, and prefer sandboxed or non-yolo execution when possible. <br>
Risk: Camera hostnames, credentials, snapshots, and clips can expose sensitive environments. <br>
Mitigation: Use scoped camera credentials, protect the config file, and run a short test capture before longer recordings. <br>


## Reference(s): <br>
- [Camsnap homepage](https://camsnap.ai) <br>
- [Camsnap ClawHub release](https://clawhub.ai/0xspeter/camsnap-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands assume the camsnap binary and ffmpeg are available on PATH.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
