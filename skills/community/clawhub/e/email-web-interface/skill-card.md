## Description: <br>
Web interface guidance for agent email communication with inbox viewing, draft creation, editing, and sending via Gmail and Gog CLI integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stefanferreira](https://clawhub.ai/user/stefanferreira) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up or choose a web interface for controlled access to agent email inboxes, drafts, and outbound mail. It is intended for mailbox owners who can secure Gmail credentials and deployment settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The examples can expose a Gmail mailbox and email-sending ability if deployed without strong protections. <br>
Mitigation: Bind services to localhost unless intentional exposure is required, require authentication and HTTPS, and use a dedicated mailbox or revocable app password. <br>
Risk: Example custom server behavior includes broad network binding, debug mode, and disabled TLS peer verification. <br>
Mitigation: Disable Flask debug mode, keep TLS verification enabled, and harden deployment settings before using the guidance with real mailboxes. <br>
Risk: Mailbox credentials and app passwords may be mishandled during setup. <br>
Mitigation: Store credentials in a secret manager and install only when the operator controls the mailbox. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/stefanferreira/email-web-interface) <br>
- [Publisher Profile](https://clawhub.ai/user/stefanferreira) <br>
- [Roundcube](https://roundcube.net) <br>
- [Gmail IMAP Documentation](https://support.google.com/mail/answer/7126229) <br>
- [Gog CLI](https://github.com/openclaw/gog) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell, PHP, Python, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides setup guidance and example snippets; it does not generate a deployed email service by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
