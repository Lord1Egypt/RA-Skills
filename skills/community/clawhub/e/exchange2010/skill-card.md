## Description: <br>
Connect to Exchange 2010 to manage emails, calendar events, contacts, tasks, attachments, shared calendars, recurring events, and out-of-office settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pes0](https://clawhub.ai/user/pes0) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to an Exchange 2010 mailbox for email, calendar, contact, task, attachment, and out-of-office workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent delegated access to the configured Exchange account and reachable shared mailboxes. <br>
Mitigation: Use a least-privilege Exchange account and require explicit approval before sending, deleting, or modifying mailbox data. <br>
Risk: Credential handling and hardcoded organization defaults may lead to misconfiguration or unintended account access. <br>
Mitigation: Fix the credential variable mismatch, remove hardcoded organization defaults, and verify environment configuration before production use. <br>
Risk: Attachment downloads can write files to caller-provided paths. <br>
Mitigation: Restrict and sanitize attachment download paths before enabling attachment handling. <br>


## Reference(s): <br>
- [Exchange2010 ClawHub release](https://clawhub.ai/pes0/exchange2010) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent guidance and callable Python examples for Exchange mailbox operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
