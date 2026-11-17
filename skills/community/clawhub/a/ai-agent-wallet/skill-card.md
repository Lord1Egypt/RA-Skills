## Description:

Agent-Wallet provides local wallet generation, import, balance checking, message signing, and native or ERC-20 transfer flows through Node.js scripts using encrypted local wallet files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beardkoda](https://clawhub.ai/user/beardkoda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage a local EVM wallet: create or import signer material, inspect native or ERC-20 balances, sign messages, and submit transfers with explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can decrypt local signer material and broadcast native or ERC-20 transfers.

Mitigation: Install only if comfortable with a local script-based wallet, review the configured chain before broadcasting, and require explicit send confirmation including mainnet double confirmation.

Risk: Seed phrases or private keys can be exposed if entered as command-line arguments or protected with weak local secrets.

Mitigation: Avoid passing seed phrases or private keys as command-line arguments, use a high-entropy WALLET_SECRET_KEY, and restrict access to the wallet directory.

Risk: Incorrect chain or token configuration can lead to balance checks or transfers on an unintended network or asset.

Mitigation: Validate wallet/config.json, the active chain_id and rpc_url, token addresses, and token decimals before balance checks or sends.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts emit JSON records for generate, import, balance, sign, and send actions; successful sends include transaction hashes.]

## Skill Version(s):

1.2.4 (source: server release evidence, SKILL.md frontmatter, CHANGELOG released 2026-04-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
