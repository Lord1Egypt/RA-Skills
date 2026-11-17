## Description:

Query the Anvil mesh network for live BSV data feeds, SPV transaction verification, and HTTP 402 micropayment service discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bsvanon](https://clawhub.ai/user/bsvanon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover Anvil mesh node capabilities, query live BSV data feeds, inspect SPV proof data, and understand HTTP 402 payment flows. Any real payment or transaction action should remain user-approved and constrained.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent toward real BSV payment and transaction workflows.

Mitigation: Require explicit user approval before creating or broadcasting any transaction, with recipient, amount, and spending-limit verification.

Risk: Returned prices, payment addresses, or proofs may come from under-protected endpoints.

Mitigation: Prefer authenticated HTTPS endpoints and verify returned payment details or proofs before relying on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bsvanon/skills/anvil-mesh)
- [Anvil GitHub Repository](https://github.com/BSVanon/Anvil)
- [anvil-mesh SDK](https://www.npmjs.com/package/anvil-mesh)
- [@SendBSV](https://x.com/SendBSV)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for command examples; no credential environment variables are declared.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
