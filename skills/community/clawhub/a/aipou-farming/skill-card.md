## Description:

Record meaningful AI-assisted work as privacy-preserving AIPOU receipts and claim accumulated AIPOU rewards on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xddneto](https://clawhub.ai/user/0xddneto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to record meaningful AI-assisted work as privacy-preserving receipts, inspect or estimate pending AIPOU rewards, and explicitly claim eligible rewards through the configured MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate reward settlement workflows that submit onchain transactions.

Mitigation: Require an explicit user request before settlement and review wallet transaction confirmations before approval.

Risk: Using an untrusted or misconfigured AIPOU MCP server could expose users to incorrect receipt, reward, or settlement results.

Mitigation: Confirm trust in the configured AIPOU MCP server before installation and rely only on server-returned tool results.

Risk: AIPOU rewards, estimates, and token value are experimental.

Mitigation: Label estimates as non-final and avoid representing token value or liquidity as guaranteed.

Risk: Wallet or prompt privacy could be harmed if sensitive material is passed into tool arguments or chat responses.

Mitigation: Use a dedicated farming wallet and keep private keys, raw prompts, model outputs, and private file contents out of tool arguments and responses.

## Reference(s):

- [AIPOU Protocol Reference](references/protocol.md)
- [AIPOU Farming on ClawHub](https://clawhub.ai/0xddneto/skills/aipou-farming)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown status summaries with MCP tool results and transaction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports receipt IDs, trust tiers, estimated rewards, settlement status, claim details, and skipped receipts when supplied by the MCP server.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
