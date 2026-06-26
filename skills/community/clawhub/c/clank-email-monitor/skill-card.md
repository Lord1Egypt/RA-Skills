## Description: <br>
Monitor email inboxes for important messages and get alerts. Works with AgentMail, Gmail, and any IMAP inbox. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[t3mr0i](https://clawhub.ai/user/t3mr0i) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor AgentMail, Gmail, or IMAP inboxes, configure keyword alerts, receive digests, and optionally prepare urgent-message auto-replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ongoing mailbox access can expose sensitive email content or broad IMAP credentials. <br>
Mitigation: Use a dedicated least-privilege mailbox or app password, avoid broad IMAP credentials where possible, and verify the publisher and executable before installing. <br>
Risk: Background monitoring and auto-reply behavior may operate without clear stop, logging, approval, or credential-protection controls. <br>
Mitigation: Keep background monitoring and auto-reply disabled until controls for stopping, logging, approvals, and credential protection are confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/t3mr0i/clank-email-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe email-monitor CLI actions, alert keywords, inbox configuration, digest settings, and notification setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
