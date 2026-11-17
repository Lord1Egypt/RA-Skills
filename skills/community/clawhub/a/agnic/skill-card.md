## Description:

Complete AI agent wallet with payments, trading, email, and on-chain identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent manage wallet status, payments, token trades, email, on-chain identity, and AI gateway requests through the Agnic CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate wallet, payment, trading, token transfer, email, and identity actions that may be sensitive or irreversible.

Mitigation: Require explicit confirmation before any payment, trade, token transfer, email send, or email reply.

Risk: The skill uses an unpinned remote command package with broad command access.

Mitigation: Use only if the Agnic npm package and publisher are trusted, and prefer a pinned, reviewed version with narrow command permissions.

Risk: The CLI environment may expose unrelated credentials or private files.

Mitigation: Run the skill with only the credentials and files needed for the requested task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agnicpay-prog/skills/agnic)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON-producing CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return JSON from CLI calls and may produce requested image files through the AI gateway.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
