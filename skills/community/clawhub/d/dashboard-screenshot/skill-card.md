## Description: <br>
Captures a full-page screenshot of a local OpenClaw dashboard and returns a concise status report for robots, task activity, token usage, and gateway health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzh19701008](https://clawhub.ai/user/zzh19701008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw operators use this skill to check a local dashboard, capture the complete dashboard view, and share a status summary through the configured QQBot channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically capture and send a full-page local dashboard image to a fixed QQBot destination. <br>
Mitigation: Use only when the QQBot target is intended and the dashboard does not expose secrets or sensitive operational data. <br>
Risk: The skill may start the local dashboard service, take screenshots, and send images externally without an explicit confirmation step. <br>
Mitigation: Prefer review or confirmation before starting services, capturing screenshots, or sending dashboard images outside the local environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zzh19701008/dashboard-screenshot) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Tool Notes](artifact/TOOLS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown status summary with a dashboard screenshot attachment] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start a local dashboard service, open a browser, capture a full-page PNG screenshot, and send it through the configured QQBot channel.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
