## Description: <br>
Capture the current Windows desktop from this WSL/OpenClaw environment and return the PNG path for inspection or delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hansheng-li](https://clawhub.ai/user/hansheng-li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent running in WSL/OpenClaw on Windows to capture the visible Windows desktop, stage the PNG, and provide the path for inspection or delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots can expose whatever is visible on the current Windows desktop. <br>
Mitigation: Use the skill only for user-requested screen capture, and close or hide sensitive windows before running it. <br>
Risk: Sending a captured screenshot through an outbound channel shares all visible screen contents. <br>
Mitigation: Treat outbound delivery as sharing the complete visible screenshot and use the managed outbound media path only when delivery is intended. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and a PNG file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a timestamped staged PNG path; default staging is for inspection, with an alternate managed outbound media directory for delivery.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
