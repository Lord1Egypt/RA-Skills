## Description:

Automates private ETH transfers on Base L2 through the Ceaser Protocol by guiding an agent through hot-wallet funding, shield, unshield, note update, and refund steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyra-v21](https://clawhub.ai/user/zyra-v21)

### License/Terms of Use:


## Use Case:

External users and developers use this skill when they need an agent-guided private ETH transfer workflow on Base L2 and explicitly want automated signing through an ephemeral hot wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the skill automates real crypto transfers.

Mitigation: Install only after review or remediation, and require explicit user confirmation for amount, recipient, fees, and funding before execution.

Risk: The workflow relies on unpinned runtime code for ceaser-mcp.

Mitigation: Pin ceaser-mcp to an audited exact version before release or deployment.

Risk: The helper signer is broader than necessary for the expected Ceaser shield transaction.

Mitigation: Narrow helpers/wallet-ops.js so it signs only the expected transaction after enforcing contract, calldata, value, and commitment checks.

Risk: Mnemonics, backup strings, and local Ceaser notes are sensitive state that may appear in the agent session.

Mitigation: Warn users before execution, show secrets only when required for recovery, avoid repeating them, and treat local notes as sensitive persistent data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zyra-v21/skills/ceaser-send)
- [Ceaser Protocol Homepage](https://ceaser.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON command outputs, and transaction links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, node, and npx; handles sensitive wallet mnemonics, backup strings, transaction hashes, and local Ceaser note state.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
