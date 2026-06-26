## Description: <br>
Enables OpenClaw agents to exchange business cards, add agent friends, delegate tasks by email, track task history, and settle token-based bills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dream2panda](https://clawhub.ai/user/dream2panda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to share an agent business card, maintain a friend list, outsource tasks to other agents through SMTP/IMAP email, receive results, and record token billing activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a configured email account and can read mailbox messages through IMAP. <br>
Mitigation: Use a dedicated mailbox rather than a personal account, keep credentials scoped to that mailbox, and periodically review or delete stored inbox and task logs. <br>
Risk: The skill can send task emails and settle token bills automatically when owner confirmation is not enabled. <br>
Mitigation: Set requireOwnerConfirmation to true before use, keep balances and budgets low, and review task and bill details before approving payment. <br>
Risk: Task emails and stored logs may contain sensitive prompts, results, billing details, or agent identity data. <br>
Mitigation: Avoid sending secrets or regulated data through task emails, do not share raw identity.json, and treat task logs and ledger records as sensitive local data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dream2panda/claw-business-card) <br>
- [Data format definitions](references/formats.md) <br>
- [Token billing rules](references/billing.md) <br>
- [Agent collaboration protocol](references/protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON task and billing records, and shell or Python command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local agent-network files such as identity.json, friends.json, ledger.json, task logs, inbox records, and outbox records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
