## Description:

Facilitates agent-to-agent payment workflows in IRC channels using Solana quotes, approvals, settlement records, and local payment history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vortitron](https://clawhub.ai/user/vortitron)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to coordinate quoted expert-agent work, payment approval, Solana settlement recording, and payment-history lookup for IRC-based agent interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be used in workflows involving real SOL payments, while settlement records depend on caller-provided transaction hashes and local JSONL ledgers.

Mitigation: Require human confirmation, verify wallet addresses and amounts independently, and confirm Solana transaction status through RPC before recording settlement.

Risk: Local JSONL records are described as immutable or tamper-proof but are ordinary local files.

Mitigation: Treat the JSONL ledgers as operational logs rather than tamper-proof evidence, protect them with normal host controls, and reconcile records against on-chain data.

Risk: Payment execution and IRC interaction depend on separate skills or integrations.

Mitigation: Review and pin dependencies, and validate the Solana transfer integration before enabling movement of real funds.

## Reference(s):

- [Agent Payment Protocol Skill Documentation](artifact/SKILL.md)
- [Agent Payment Protocol README](artifact/README.md)
- [ClawHub Skill Page](https://clawhub.ai/vortitron/skills/agent-payment-protocol)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and JSON-shaped records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces quote, payment, history, and statistics objects for agent workflows; settlement execution depends on a separate Solana transfer integration.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
