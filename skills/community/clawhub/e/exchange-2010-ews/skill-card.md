## Description: <br>
Provides Exchange 2010 EWS access for managing emails, folders, attachments, calendar events, contacts, tasks, and out-of-office settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pes0](https://clawhub.ai/user/pes0) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents that administer Exchange 2010 mailboxes use this skill to read and search mail, manage calendars, contacts, tasks, attachments, and out-of-office settings, and send or modify Exchange data through EWS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad live Exchange mailbox authority with weak guardrails. <br>
Mitigation: Use least-privilege Exchange credentials and require explicit confirmation before sending mail or changing or deleting Exchange data. <br>
Risk: Credentials and organization-specific defaults may be misconfigured or exposed. <br>
Mitigation: Verify the PICARD_PASSWORD versus EXCHANGE_PASSWORD mismatch before use, remove organization-specific defaults, and protect the credentials file. <br>
Risk: Attachment downloads can write files from mailbox content to disk. <br>
Mitigation: Restrict attachment downloads to a safe directory and sanitize filenames before writing files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pes0/exchange-2010-ews) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Python return values and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform live Exchange mailbox, calendar, contact, task, attachment, and out-of-office actions when called with credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
