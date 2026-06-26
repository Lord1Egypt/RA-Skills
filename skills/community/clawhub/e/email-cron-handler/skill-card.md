## Description: <br>
Email Cron Handler monitors a configured mailbox through IMAP/SMTP, filters allowed senders, and helps an agent process email-delivered commands and reply with execution results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PebblerWon](https://clawhub.ai/user/PebblerWon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let a scheduled agent check an inbox, process commands from an allowed sender, and send success, failure, or timeout feedback by email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email messages can trigger agent actions and send results back without strong controls. <br>
Mitigation: Use a dedicated low-privilege mailbox, require a non-empty sender allowlist, add stronger authentication where possible, and restrict which commands the agent may run. <br>
Risk: Mailbox credentials and cron payloads may expose sensitive access details. <br>
Mitigation: Keep real credentials out of prompts and shared payloads, store secrets in protected configuration, and redact sensitive content from email replies. <br>
Risk: A scheduled email automation loop can continue acting after misconfiguration or compromise. <br>
Mitigation: Define and test a simple way to disable the cron jobs before enabling the workflow. <br>


## Reference(s): <br>
- [Email Cron Handler configuration template](references/01-config-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/PebblerWon/email-cron-handler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and Python helper script usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow can produce email replies containing command execution status and results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
