## Description: <br>
Auto-detect and enable OpenClaw Browser Relay Chrome extension when disconnected. Uses native mouse control to click the extension icon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevinZhj](https://clawhub.ai/user/kevinZhj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users on Windows use this skill to reconnect the OpenClaw Browser Relay Chrome extension by running a PowerShell workflow that checks connection status and clicks a calibrated extension icon coordinate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to move and click the real mouse, which can interfere with active desktop work or click the wrong target if coordinates are stale. <br>
Mitigation: Use it only when intentional, verify coordinates with TestMode first, and avoid unattended execution unless the browser state is controlled. <br>
Risk: The release references a PowerShell script that is missing from the packaged artifact. <br>
Mitigation: Verify the expected script is present and reviewed before running any command that invokes it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kevinZhj/browser-extension-enabler) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with PowerShell command examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-only workflow; extension icon coordinates require calibration before real mouse control is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
