## Description: <br>
Helps an agent connect to a configured DingTalk mailbox MCP service through mcporter to list mailboxes, search messages, read message details, and send email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackeylee007](https://clawhub.ai/user/jackeylee007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure mailbox access and operate DingTalk email workflows, including querying mail, reading messages, drafting replies, and sending messages through an approved MCP connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured DingTalk mailbox MCP URL can grant mailbox access and should be treated like a credential. <br>
Mitigation: Keep the URL scoped to the intended account, store it in the local mcporter configuration, and avoid sharing it in prompts, logs, or public files. <br>
Risk: The skill can send email, including bulk messages, through the configured mailbox. <br>
Mitigation: Require preview and explicit approval of sender, recipients, subject, body, and CC fields before any send_email call. <br>
Risk: Mailbox search and message retrieval can expose sensitive email contents. <br>
Mitigation: Limit searches to the necessary mailbox and query scope, and avoid copying sensitive message content into unrelated tools or outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackeylee007/dingtalk-mailbox) <br>
- [DingTalk Mailbox MCP service documentation](https://help.aliyun.com/document_detail/2925708.html) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>
- [mcporter documentation](https://mcpmarket.com/zh/tools/skills/mcporter) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and MCP call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided DingTalk mailbox MCP URL and mcporter configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
