## Description: <br>
Dingtalk Notify helps an agent send DingTalk work notifications, files, connectivity tests, retry requests, and status checks for a specified user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m646pxhjf4-dot](https://clawhub.ai/user/m646pxhjf4-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to route workplace notifications and files through DingTalk, including connectivity tests, failed-send retries, and service status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send message content and files to DingTalk recipients outside the local workspace. <br>
Mitigation: Review message and file contents before sending, and confirm the recipient user ID before each send. <br>
Risk: Local send records may retain sensitive workplace notification data. <br>
Mitigation: Limit access to notification logs and review retention for ~/.openclaw/backups/notifications/send-record-YYYY-MM-DD.jsonl. <br>
Risk: A broad trigger phrase could cause unintended notification sends. <br>
Mitigation: Require explicit user confirmation before executing DingTalk send or retry commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include recipient-specific DingTalk command examples and note that send records are stored locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
