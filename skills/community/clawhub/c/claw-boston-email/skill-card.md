## Description: <br>
Gives an OpenClaw agent a @claw.boston mailbox for sending, receiving, searching, and reading email with attachment and webhook support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mastalie](https://clawhub.ai/user/Mastalie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to create and operate a hosted @claw.boston email address from their agent, including setup, sending mail, checking and reading inbox messages, replying, searching, and viewing account usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and send mailbox content through a third-party hosted email service. <br>
Mitigation: Install only after deciding to trust claw.boston, and require explicit confirmation before reading full messages, sending replies, forwarding content, or attaching files. <br>
Risk: The local API key grants mailbox access if copied, synced, or exposed. <br>
Mitigation: Keep ~/.openclaw/skills/claw-boston-email/config.json private and exclude it from shared folders, logs, backups, and source control. <br>
Risk: Mailbox messages and attachments may contain sensitive data or prompt-injection content. <br>
Mitigation: Avoid sensitive mail until the provider's privacy, retention, and revocation policies are understood, and review suspicious messages or attachments before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mastalie/claw-boston-email) <br>
- [Publisher profile](https://clawhub.ai/user/Mastalie) <br>
- [claw.boston website](https://claw.boston) <br>
- [claw.boston API base](https://api.claw.boston) <br>
- [claw.boston pricing](https://claw.boston/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown text with email summaries, confirmations, account details, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or read local configuration containing an API key and may exchange mailbox content, attachments, and webhook notifications with the hosted claw.boston service.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
