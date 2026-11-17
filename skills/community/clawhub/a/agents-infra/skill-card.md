## Description:

Infrastructure for AI agents covering phone, email, social accounts, compute, domains, voice calling, wallets, and skill catalog access with USDC payment via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xartex](https://clawhub.ai/user/0xartex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to provision and manage AgentOS infrastructure such as phone numbers, encrypted email inboxes, VPS instances, domains, DNS records, wallets, voice calls, and webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide paid purchases and recurring infrastructure actions.

Mitigation: Require explicit approval before any purchase, paid endpoint call, server deployment, resize, domain registration, or wallet action.

Risk: The skill covers communications workflows including SMS, email, voice calls, call recording, attachments, and webhooks.

Mitigation: Verify recipients, inbox IDs, phone numbers, call IDs, webhook targets, and recording intent before executing communication or recording actions.

Risk: The skill includes destructive or externally visible infrastructure actions such as server deletion and DNS updates.

Mitigation: Confirm target resource IDs and desired DNS/server state before delete, update, transfer, or deployment operations.

Risk: The email decrypt helper reads a local Solana keypair.

Mitigation: Run the helper only on a trusted machine with a keypair you intend to expose to that local process.

Risk: The documentation allows npx or latest package execution.

Mitigation: Prefer pinned or reviewed package versions instead of ad hoc npx/latest installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xartex/skills/agents-infra)
- [AgentOS API docs](https://agntos.dev/docs)
- [AgentOS API base](https://agntos.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with inline bash commands, API endpoint tables, and a JavaScript helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide paid purchases, communications actions, infrastructure changes, DNS updates, wallet operations, and local email decryption.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
