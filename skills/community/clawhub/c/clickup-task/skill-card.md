## Description: <br>
Create tasks in Vision Play ClickUp lists (visionplay or inbox). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[visionplay303](https://clawhub.ai/user/visionplay303) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using Vision Play ClickUp workflows use this skill to create tasks in either the visionplay or inbox list from a chat slash command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates account-writing work to a server-side ClickUp task creation script that was not included for review. <br>
Mitigation: Install only if you control and have reviewed that script, and confirm it writes only to the intended ClickUp workspace and lists. <br>
Risk: Task titles and descriptions are routed through a shell command and may include sensitive or unexpected user text. <br>
Mitigation: Avoid placing secrets in task content, use structured arguments where possible, and sanitize or constrain user-provided text before execution. <br>
Risk: The skill requires a ClickUp token and configured list identifiers that can create tasks in an external account. <br>
Mitigation: Use the least-privileged ClickUp token available and verify CLICKUP_LIST_VISIONPLAY and CLICKUP_LIST_INBOX before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/visionplay303/clickup-task) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text] <br>
**Output Format:** [Plain text or ClickUp API response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the ClickUp API response or error text to the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
