## Description:

Protects AI agents that process email by providing sender verification, content sanitization, attachment policy checks, and threat detection for common email providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivaavimusic](https://clawhub.ai/user/ivaavimusic)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add a defensive review layer before agents read, parse, or act on email content. It is intended for workflows that need sender checks, message sanitization, attachment restrictions, and prompt-injection screening across Gmail, AgentMail, Proton Mail, and generic IMAP/SMTP providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email senders may gain high-impact command authority if email-triggered actions are treated as trusted automation.

Mitigation: Require independent confirmation and provider-verified authentication before send, delete, forward, rule-changing, or other destructive actions are executed.

Risk: Sender verification can fail open or misclassify commented examples as privileged users.

Mitigation: Review authorization parsing before deployment and keep owner, admin, trusted, and blocked sender lists explicit and tested.

Risk: Full-content logging can expose sensitive raw email data.

Mitigation: Use secured evidence storage, retention controls, and limited logging for raw messages and blocked or flagged content.

## Reference(s):

- [Owner Configuration](references/owner-config.md)
- [Security Policies](references/security-policies.md)
- [Threat Patterns](references/threat-patterns.md)
- [Gmail Provider Guide](references/provider-gmail.md)
- [AgentMail Provider Guide](references/provider-agentmail.md)
- [Generic Email Provider Guide](references/provider-generic.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and JSON or YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts may emit JSON for parsed messages, sender verification results, and sanitization findings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
