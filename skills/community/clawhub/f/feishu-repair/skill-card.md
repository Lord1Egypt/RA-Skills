## Description: <br>
Diagnoses and repairs OpenClaw Feishu gateway, permission configuration, and message delivery issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amd5](https://clawhub.ai/user/amd5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw administrators use this skill to diagnose Feishu gateway status, restore Feishu allowlists from local configuration or backups, restart the gateway, verify configuration and logs, and send Feishu test messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically change OpenClaw Feishu settings and restart the gateway. <br>
Mitigation: Run it only in an administered OpenClaw Feishu environment, review the affected configuration first, and prefer requiring an explicit repair flag before changes are applied. <br>
Risk: The skill can use Feishu app credentials to send verification messages to all configured users and chats. <br>
Mitigation: Limit test recipients when possible, confirm the recipient lists before execution, and avoid exposing app credentials in logs or prompts. <br>
Risk: Repairs are not read-only and can affect live message delivery. <br>
Mitigation: Use a dry-run or wrapper for diagnosis-only operation where available, and schedule repair runs during an acceptable maintenance window. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amd5/feishu-repair) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/amd5) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Plain text diagnostic report, or structured JSON when invoked with --json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update Feishu allowlists, restart the OpenClaw gateway, and send Feishu verification messages when repairs are triggered.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence, SKILL.md frontmatter, and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
