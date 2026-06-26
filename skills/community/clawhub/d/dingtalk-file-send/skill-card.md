## Description: <br>
Upload and send files to DingTalk users. Auto-detects account from current session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenriou](https://clawhub.ai/user/kenriou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to upload a local file to DingTalk and send it to a specified DingTalk user through a configured account binding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A selected local file could be sent to the wrong DingTalk recipient or from the wrong configured account. <br>
Mitigation: Before each use, confirm the exact file path, DingTalk account binding, and recipient user ID. <br>
Risk: Confidential documents could be uploaded to DingTalk if the requested file is sensitive. <br>
Mitigation: Review the file path and document sensitivity before allowing the upload and send workflow to proceed. <br>
Risk: The workflow depends on local DingTalk credentials and OpenClaw binding data. <br>
Mitigation: Install and use only when the local OpenClaw DingTalk configuration is expected, current, and authorized for the target recipient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenriou/dingtalk-file-send) <br>
- [Publisher profile](https://clawhub.ai/user/kenriou) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces DingTalk API command guidance for file upload, message send, and delivery-status checks.] <br>

## Skill Version(s): <br>
1.2.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
