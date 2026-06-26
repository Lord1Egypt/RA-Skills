## Description: <br>
Runs email marketing workflows including personalized bulk sends, reply monitoring, FAQ-based draft responses, and language-aligned business replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlrlyy](https://clawhub.ai/user/zlrlyy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing and operations users use this skill to prepare personalized email campaigns, send test or bulk messages, monitor replies, draft FAQ-aligned responses, and review delivery or reply statistics for authorized recipient lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send bulk email from a configured mailbox. <br>
Mitigation: Use only a dedicated authorized mailbox, opted-in recipient lists, and an explicit confirmation step before any live bulk send. <br>
Risk: The skill can read inbox contents and retain email-derived data. <br>
Mitigation: Minimize stored message content and define a clear privacy and retention policy before deployment. <br>
Risk: The artifact disables normal TLS certificate verification for SMTP connections. <br>
Mitigation: Restore normal TLS verification before using the mail-sending scripts. <br>
Risk: The artifact intentionally alters messages to reduce spam filtering. <br>
Mitigation: Remove hidden anti-spam tag generation and follow applicable sender, consent, and platform policies. <br>


## Reference(s): <br>
- [Email Marketing ClawHub release](https://clawhub.ai/zlrlyy/email-marketing-3) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python command examples and JSON status files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send live email and read or store mailbox content when configured; review security guidance before use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
