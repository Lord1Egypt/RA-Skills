## Description: <br>
Submit a leave request through Feishu (Lark). Use when the user wants to request time off, submit a leave application, or mentions taking leave. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeidyz](https://clawhub.ai/user/baofeidyz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees use this skill to prepare and submit Feishu leave requests after confirming the date, duration, leave type, and reason. It guides the agent through desktop Feishu navigation, form completion, submission, and post-submission verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may submit a real leave request with incorrect dates, duration, leave type, or reason. <br>
Mitigation: Require explicit user confirmation of all leave details before navigating Feishu or submitting the request. <br>
Risk: The request could be submitted from the wrong Feishu workplace account. <br>
Mitigation: Use the skill only while signed into the correct Feishu workplace account and verify the account before submission. <br>
Risk: Feishu desktop navigation or form labels may differ from the documented flow. <br>
Mitigation: Pause on navigation errors, ask for a screenshot when fields do not match, and report validation or submission failures back to the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baofeidyz/feishu-leave-request) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text] <br>
**Output Format:** [Markdown or conversational instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow for collecting confirmed leave details and guiding Feishu desktop app submission.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
