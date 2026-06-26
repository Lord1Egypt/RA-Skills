## Description: <br>
Canvas as an app platform. Build, store, and run rich visual apps on the OpenClaw Canvas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Knightluozichu](https://clawhub.ai/user/Knightluozichu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw agent users use this skill to build, store, serve, and run rich HTML/CSS/JavaScript apps on the OpenClaw Canvas, including dashboards, trackers, and quick visual displays. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts may stop unrelated local processes when clearing a port. <br>
Mitigation: Check the target port before opening an app, and only run close or open commands when the intended Canvas app owns the process. <br>
Risk: Unsafe or path-like app names may cause the local server to expose unintended folders. <br>
Mitigation: Use simple app names and keep sensitive files outside folders served through Canvas OS. <br>
Risk: Canvas apps can send messages back to the agent through deep links. <br>
Mitigation: Require confirmation before app-originated messages trigger consequential agent actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Knightluozichu/canvas-os-1-0-1) <br>
- [Canvas Loading Reference](CANVAS-LOADING.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and HTML/CSS/JavaScript app templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Canvas app instructions and helper commands that may start or stop local HTTP servers.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
