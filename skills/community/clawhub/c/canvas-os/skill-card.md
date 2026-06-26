## Description: <br>
Canvas as an app platform. Build, store, and run rich visual apps on the OpenClaw Canvas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fraction12](https://clawhub.ai/user/fraction12) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use Canvas-OS to build, serve, and display local HTML/CSS/JavaScript apps on the OpenClaw Canvas. It is suited for dashboards, trackers, quick visual displays, and agent-updated Canvas interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper scripts can stop processes on a selected local port, which may interrupt unrelated local services. <br>
Mitigation: Confirm the port and listening process before closing or replacing a server, and use dedicated Canvas app ports where possible. <br>
Risk: Local Canvas app folders or served pages may expose private data if sensitive files are placed in the app directory. <br>
Mitigation: Keep Canvas app directories scoped to intended assets and avoid storing secrets or private data in served folders. <br>
Risk: Direct HTML injection can run untrusted HTML or JavaScript inside the Canvas context. <br>
Mitigation: Use trusted app content only, review injected HTML before execution, and prefer localhost serving for reusable apps with known assets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fraction12/canvas-os) <br>
- [README](README.md) <br>
- [Canvas Loading Reference](CANVAS-LOADING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, HTML, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Canvas app setup guidance and helper command patterns; generated apps may include HTML templates and JavaScript APIs for live updates.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
