## Description:

Enables OpenClaw agents to make FHE-encrypted x402 payments, wrap or unwrap encrypted tokens, manage escrow jobs, register identity, submit feedback, and delegate balance viewing on Ethereum Sepolia or Mainnet with Zama fhEVM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billynothack](https://clawhub.ai/user/billynothack)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to let agents perform confidential token payments, escrow workflows, identity registration, feedback, and delegated balance viewing on supported Ethereum networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend funds or change escrow, unwrap, feedback, and delegation state through irreversible on-chain actions.

Mitigation: Use Sepolia or a low-balance wallet first, review destinations and amounts before execution, and prefer supervised Ledger approval for real funds.

Risk: Configurable paid-service URLs can receive prompts, code, or other sensitive data.

Mitigation: Only point DFNS and paid-service URLs at trusted HTTPS origins and avoid passing proprietary code or secrets to review-and-rate.

Risk: Wallet credentials and signing configuration are sensitive operational inputs.

Mitigation: Install only when the publisher is trusted, configure wallet modes tightly, and protect USER_PRIVATE_KEY, DFNS, and Ledger bridge secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/billynothack/skills/confidential-agentic-payment-stack)
- [Project homepage from metadata](https://gitlab.com/bea7892046/fhex402)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON strings from command scripts, plus Markdown setup guidance and command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands report success or failure as JSON and may initiate irreversible on-chain payment, escrow, unwrap, feedback, or delegation actions.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
