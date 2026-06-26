## Description: <br>
执行邮件营销任务，包括 AI 智能生成 HTML、个性化群发、自动化回信监控、FAQ 知识库智能匹配、多语种自动对齐。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlrlyy](https://clawhub.ai/user/zlrlyy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing and business users use this skill to generate HTML email content, send personalized bulk messages from recipient lists, monitor replies, and prepare FAQ-grounded responses for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send bulk email at scale. <br>
Mitigation: Use only consented recipient lists, test with a small batch first, and apply clear send limits before any full campaign. <br>
Risk: The skill can read inbox content and store email-related data locally. <br>
Mitigation: Use a dedicated mailbox with revocable app-specific credentials, avoid printing secrets, and regularly protect or delete local JSON files that may contain private email content. <br>
Risk: Security evidence identifies deliberate spam-filter evasion behavior. <br>
Mitigation: Review and remove anti-spam interference behavior before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlrlyy/email-marketing-faq) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands plus generated HTML email content and local JSON status files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included scripts can send email, read inbox content, and write local status or reply data when executed.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
