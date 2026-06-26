## Description: <br>
Manage Fastmail mail, mailbox, identity, contact, and calendar workflows through JMAP API calls with safe batching and token hygiene. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to automate Fastmail JMAP workflows for mailbox management, message search, draft/send flows, identity settings, contacts, and calendar events with confirmation and verification around high-impact changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses token-based access to Fastmail account data, including mail, mailbox, identity, contact, and calendar workflows. <br>
Mitigation: Use the narrowest Fastmail token scope available, keep FASTMAIL_API_TOKEN out of chat, logs, shell history, and repository files, and revoke or rotate the token when access is no longer needed. <br>
Risk: Send, delete, move, identity, and bulk calendar actions can affect real communication or account state. <br>
Mitigation: Require explicit confirmation for high-impact actions, execute the smallest safe batch first, and verify the final state with targeted read calls. <br>
Risk: Local logs and snapshots in ~/fastmail-api/ can contain operational context or payload details from sensitive account workflows. <br>
Mitigation: Periodically review or delete ~/fastmail-api/ logs and snapshots, and redact addresses, subjects, and payload details before sharing outputs. <br>


## Reference(s): <br>
- [Fastmail API ClawHub release page](https://clawhub.ai/ivangdavila/fastmail-api) <br>
- [Fastmail API skill homepage](https://clawic.com/skills/fastmail-api) <br>
- [Fastmail JMAP session endpoint](https://api.fastmail.com/jmap/session) <br>
- [Fastmail JMAP API endpoint](https://api.fastmail.com/jmap/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON JMAP request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include Fastmail setup guidance, JMAP request patterns, account and mailbox identifiers, confirmation prompts, verification steps, troubleshooting notes, and redacted operation summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
