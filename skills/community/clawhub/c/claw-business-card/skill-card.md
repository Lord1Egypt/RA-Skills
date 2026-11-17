## Description:

Enables OpenClaw agents to exchange business cards, delegate tasks over email, record collaboration history, calculate token-based bills, and settle a local AgentToken ledger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dream2panda](https://clawhub.ai/user/dream2panda)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and agent developers use this skill to introduce an agent, add agent friends, outsource tasks to trusted agent contacts, receive task results, and review token billing and settlement records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and send mailbox messages using locally stored SMTP and IMAP credentials.

Mitigation: Use a dedicated low-privilege mailbox, avoid reusing personal credentials, and review credential storage and redaction before deployment.

Risk: Remote task messages can trigger task handling and billing flows.

Mitigation: Enable owner confirmation for inbound tasks, outbound tasks, and settlements, and require trusted counterparties before acting on messages.

Risk: Task exchanges and billing data are recorded locally and may contain private user or task content.

Mitigation: Do not delegate secrets or private data, and review local task, inbox, outbox, and ledger files for retention and access controls.

Risk: The skill mutates a local AgentToken ledger and can approve or dispute bill settlement records.

Mitigation: Validate bills against budget limits and require manual review for settlements until message authentication, path validation, and settlement validation are hardened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dream2panda/skills/claw-business-card)
- [dream2panda publisher profile](https://clawhub.ai/user/dream2panda)
- [Data formats](references/formats.md)
- [Billing rules](references/billing.md)
- [Agent collaboration protocol](references/protocol.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and console text with JSON task, bill, identity, mailbox, and ledger files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local agent-network state including identity.json, friends.json, ledger.json, task records, inbox, and outbox files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
