## Description: <br>
Captures the primary screen, copies the screenshot into the workspace, and sends it to Feishu when requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TOOTW](https://clawhub.ai/user/TOOTW) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or agent users use this skill to share their current screen in Feishu without manually capturing, moving, and attaching the image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture the entire primary screen, including sensitive windows. <br>
Mitigation: Close or hide sensitive content before use and only invoke the skill when a full-screen capture is intended. <br>
Risk: The skill can send a screenshot to Feishu from broad screenshot requests without an explicit confirmation step or destination control. <br>
Mitigation: Require confirmation before sending and make the Feishu recipient or channel explicit. <br>
Risk: The screenshot is stored locally and copied into the workspace before delivery. <br>
Mitigation: Delete the local and workspace screenshot files after sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TOOTW/feishu-screenshot) <br>
- [Publisher profile](https://clawhub.ai/user/TOOTW) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions that create a screenshot file and send it through a Feishu file action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
