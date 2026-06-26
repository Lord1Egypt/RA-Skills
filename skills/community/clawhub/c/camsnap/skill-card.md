## Description: <br>
Capture frames or clips from RTSP/ONVIF cameras. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and camera administrators use Camsnap to discover cameras, configure access, and capture snapshots, clips, or motion-triggered events from RTSP/ONVIF cameras. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Camera endpoints and credentials may be exposed while configuring RTSP/ONVIF access. <br>
Mitigation: Store camera credentials carefully, limit credential scope, and avoid sharing configuration files or command histories that contain secrets. <br>
Risk: Motion watch action hooks can execute broad or destructive commands. <br>
Mitigation: Require explicit user intent before enabling watch mode and review each action command before execution. <br>
Risk: Snapshots and clips may write sensitive captured media to shared locations. <br>
Mitigation: Choose output paths deliberately and run a short test capture before longer clips or shared storage writes. <br>


## Reference(s): <br>
- [Camsnap ClawHub listing](https://clawhub.ai/steipete/camsnap) <br>
- [Camsnap homepage](https://camsnap.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local camera names, credentialed endpoints, output file paths, and watch-mode action hooks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
