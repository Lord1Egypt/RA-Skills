## Description: <br>
Feishu Integration helps agents work with Feishu Open Platform APIs for document and wiki operations, file uploads, Markdown imports, message parsing, OCR, token handling, and group welcome workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moxunjinmu](https://clawhub.ai/user/moxunjinmu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to configure Feishu app credentials, call Feishu document, wiki, drive, import, messaging, and OCR APIs, and generate reusable shell or Python workflows for Feishu automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact ships with an exposed Feishu app secret. <br>
Mitigation: Replace bundled credentials with your own Feishu app credentials before use and rotate any secret that was copied from the artifact. <br>
Risk: The skill can perform live Feishu document writes, uploads, message sends, chat creation, and chat deletion. <br>
Mitigation: Restrict the Feishu app to least-privilege scopes and require explicit confirmation before executing write, upload, messaging, chat creation, or chat deletion actions. <br>
Risk: The group welcome workflow can send recurring automated messages if installed as a scheduled job. <br>
Mitigation: Only enable the cron welcome bot for chats where recurring automated messages are intended, and review its schedule, cooldown, and quiet-hour settings before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moxunjinmu/feishu-integration) <br>
- [Feishu API reference](references/api-reference.md) <br>
- [Token management](references/token-management.md) <br>
- [Markdown import workflow](references/import-workflow.md) <br>
- [Message parsing guide](references/message-parsing.md) <br>
- [Feishu Open Platform documentation](https://open.feishu.cn/document/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell, Python, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Feishu API calls that read, write, upload, import, send messages, create chats, delete chats, or run recurring welcome automation when executed with valid credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
