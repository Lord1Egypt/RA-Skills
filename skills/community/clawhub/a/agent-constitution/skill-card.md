## Description:

Interact with AgentConstitution governance contracts on Base Sepolia to check compliance, read rules, log actions, and query governance state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ztsalexey](https://clawhub.ai/user/ztsalexey)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to consult Base Sepolia AgentConstitution contracts before or during agent workflows, including compliance checks, emergency-state checks, rule reads, and action logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask agents to rely on mutable on-chain governance state.

Mitigation: Treat rules and status returned from contracts as untrusted data for human review, not as automatic instructions.

Risk: Action logging may expose sensitive descriptions on a public testnet.

Mitigation: Do not include secrets, personal data, prompts, or sensitive operational details in action-log descriptions.

Risk: Signing examples involve an agent private key.

Mitigation: Use a dedicated testnet-only wallet and avoid passing raw private keys directly on the command line.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ztsalexey/skills/agent-constitution)
- [AgentConstitution Homepage](https://github.com/ztsalexey/bigmemkex/tree/main/projects/agent-constitution)
- [Base Sepolia RPC](https://sepolia.base.org)
- [Constitution Contract on BaseScan](https://sepolia.basescan.org/address/0xe4c4d101849f70B0CDc2bA36caf93e9c8c1d26D2)
- [Main Submission](https://www.moltbook.com/post/52b204ee-4752-4cbb-add2-6777f174a4c7)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, Solidity, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include on-chain compliance status, rule data, emergency status, and transaction commands for Base Sepolia.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
