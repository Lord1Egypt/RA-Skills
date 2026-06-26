## Description: <br>
Chat Logger records Feishu and Dingtalk direct-message prompts and returns daily, personal, or full chat-log summaries for trigger commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bjmfjoy](https://clawhub.ai/user/bjmfjoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or operators using Feishu or Dingtalk agents can use this skill to log direct user prompts and retrieve daily, personal, or full chat-log summaries. Administrators should deploy it only where message logging is disclosed and access to summaries is controlled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores private direct-message content in local chat-log files. <br>
Mitigation: Install only where affected users have explicit notice or consent, and define retention and deletion controls before production use. <br>
Risk: Global chat-log summaries may expose multiple users' logs without clear authorization checks. <br>
Mitigation: Restrict full-summary commands to authorized administrators and ensure personal-record commands return only the requester's own logs. <br>
Risk: Loose trigger handling could cause unintended summary disclosure. <br>
Mitigation: Use exact command matching for supported triggers and avoid routing unrelated messages into summary handlers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bjmfjoy/chat-logger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text and Markdown-style chat summary reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns summaries or status strings; writes per-user daily Markdown log files when invoked in an agent environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
