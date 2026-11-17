## Description:

Multi-chain cryptocurrency wallet management. Check balances, send tokens, view transaction history across Ethereum, Solana, Bitcoin and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nvmmonkey](https://clawhub.ai/user/nvmmonkey)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage cryptocurrency wallets across supported chains, including balance checks, transaction history review, token price lookup, portfolio summaries, and confirmed token sends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect recipient addresses, chains, amounts, or fees could cause irreversible financial loss.

Mitigation: Require explicit confirmation before any send action and independently verify the recipient address, chain, token, amount, and fee details.

Risk: Exposure of seed phrases, private keys, or untrusted wallet and RPC/API endpoints could compromise funds.

Mitigation: Never provide seed phrases or private keys, and use only wallets and RPC/API endpoints the user independently trusts.

Risk: Balance, transaction, price, or portfolio information from external endpoints may be stale, incomplete, or misleading.

Mitigation: Cross-check material financial decisions with trusted wallet software, block explorers, or exchange data before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nvmmonkey/skills/crypto-wallet)
- [ClawHub publisher profile](https://clawhub.ai/user/nvmmonkey)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on curl and jq when command-line API calls are needed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
