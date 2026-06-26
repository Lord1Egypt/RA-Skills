## Description: <br>
Email management skill for AI assistants with real-time notifications, smart categorization (7 categories), verification code extraction, and HTML content sanitization. Supports Gmail, QQ Mail, and NetEase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanchan720](https://clawhub.ai/user/ryanchan720) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-assistant users use Email Bridge to connect local mailbox accounts, monitor new mail, receive categorized notifications, extract verification codes, and send messages through supported providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires mailbox access and stores account credentials or OAuth tokens locally. <br>
Mitigation: Install only for intended mailbox-management use, protect ~/.email-bridge, and prefer least-privilege OAuth scopes or provider app-specific passwords. <br>
Risk: Outbound email sending could send unintended or incorrect messages. <br>
Mitigation: Review every outbound email recipient, subject, and body before sending. <br>
Risk: Background monitoring and notification forwarding can expose sensitive email content, verification codes, or links. <br>
Mitigation: Disable body, link, and verification-code notifications unless needed, and stop the daemon when it is not in use. <br>
Risk: Secrets may be exposed if entered directly into chat or shell history. <br>
Mitigation: Configure accounts through the local CLI prompts and avoid putting authorization codes or passwords in shell commands. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/ryanchan720/email-bridge) <br>
- [Email Bridge on ClawHub](https://clawhub.ai/ryanchan720/email-bridge) <br>
- [Gmail setup guide](references/gmail-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-oriented guidance with command examples and structured email notification text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include categorized email summaries, verification codes, action links, sanitized body previews, and send/sync command guidance.] <br>

## Skill Version(s): <br>
0.6.3 (source: server release evidence, SKILL.md frontmatter, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
