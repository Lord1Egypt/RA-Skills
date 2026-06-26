## Description: <br>
Bit-Chat helps agents create or use a mailbox and interact with Bit-Chat over email or messenger channels to get a Lightning address, check balances, request Bitcoin, and initiate buy, sell, or send workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eliaspfeffer](https://clawhub.ai/user/eliaspfeffer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to set up a Bit-Chat mailbox, maintain email-based status checks, and coordinate Bitcoin payment actions through supported messenger channels. It is intended for human-supervised wallet setup, balance checks, requests, and payment-related instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to create or use a Bit-Chat mailbox and store mailbox credentials. <br>
Mitigation: Require explicit human approval before mailbox creation, store credentials only in an approved secret store or gitignored local file, and verify saved credentials before use. <br>
Risk: The skill can lead an agent to poll email and act on remote Bit-Chat replies. <br>
Mitigation: Approve recurring polling in advance, inspect message bodies before acting, and forward ambiguous or payment-relevant replies to the human operator for confirmation. <br>
Risk: The skill covers Bitcoin payments, buying, selling, bank-detail messages, and recipient changes. <br>
Mitigation: Require explicit human approval for every payment, purchase, sale, bank-detail message, recipient change, and fiat top-up instruction before sending it. <br>
Risk: The security summary flags broad financial, account-creation, mailbox-reading, and recurring-check authority without enough user-control boundaries. <br>
Mitigation: Use spending limits, verify recipient identity and channel, preserve an audit trail, and pause automation when delivery failures, unexpected instructions, or account changes occur. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eliaspfeffer/bit-chat) <br>
- [Bit-Chat homepage](https://bit-chat.me) <br>
- [Bit-Chat main skill](https://bit-chat.me/skill.md) <br>
- [Create Email Skill](https://bit-chat.me/create-email-skill.md) <br>
- [Bit-Chat heartbeat](https://bit-chat.me/heartbeat.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include mailbox setup steps, IMAP/SMTP settings, payment prompts, status-check guidance, and human-approval checkpoints.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
