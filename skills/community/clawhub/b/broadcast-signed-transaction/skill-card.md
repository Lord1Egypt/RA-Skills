## Description:

Broadcasts an already-signed transaction hex to a blockchain through the OKX Web3 broadcast API without requiring a private key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangchengming666](https://clawhub.ai/user/wangchengming666)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to validate required broadcast inputs, call the bundled broadcast script, and return transaction broadcast results for already-signed blockchain transactions. It is intended for cases where the transaction has already been signed elsewhere and no wallet private key should be handled by the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles OKX Web3 API credentials needed to submit broadcast requests.

Mitigation: Use environment variables or a secret manager, avoid command-line credential flags, and prefer narrowly scoped OKX Web3 API keys.

Risk: Broadcasting a signed blockchain transaction is irreversible after submission.

Mitigation: Confirm the signed transaction payload, chain index, sender address, and intended effects before broadcasting.

Risk: Unpinned dependencies or environment drift can affect script behavior.

Mitigation: Install dependencies in a pinned virtual environment before using the skill with valuable transactions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangchengming666/skills/broadcast-signed-transaction)
- [Publisher profile](https://clawhub.ai/user/wangchengming666)
- [OKX Web3 API](https://web3.okx.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON broadcast results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include order ID, transaction hash, chain name, block explorer URL, MEV flag status, and error details returned by the broadcast script.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
