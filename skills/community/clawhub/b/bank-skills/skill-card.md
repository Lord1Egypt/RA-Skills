## Description:

Traditional banking via Wise API + on-chain token swaps on Base.

This skill is for research and development only.

## Publisher:

[singularityhacker](https://clawhub.ai/user/singularityhacker)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can give agents controlled access to Wise balance, receive-detail, transfer, wallet, token-swap, and token-transfer workflows. Use only in controlled R&D settings with minimal funds and human confirmation for value-moving actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move real banking or crypto funds.

Mitigation: Use minimal funds, a least-privileged Wise token, and a separate human confirmation process before transfers or swaps.

Risk: Weak wallet passwords or private-key export can compromise the wallet.

Mitigation: Set a strong CLAWBANK_WALLET_PASSWORD before creating any wallet; avoid wallets created with the default password and treat exported, copied, logged, or shared private keys as compromised.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/singularityhacker/skills/bank-skills)
- [Publisher Profile](https://clawhub.ai/user/singularityhacker)
- [Wise API Reference](https://docs.wise.com/api-reference)
- [NPM Package](https://www.npmjs.com/package/@singularityhacker/bank-skill)
- [Base Mainnet RPC](https://mainnet.base.org)

## Skill Output:

**Output Type(s):** [JSON, API calls, Shell commands, Configuration]

**Output Format:** [JSON responses over stdin/stdout, with documented shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WISE_API_TOKEN for banking actions; optional WISE_PROFILE_ID, CLAWBANK_WALLET_PASSWORD, and BASE_RPC_URL configure profile and Base wallet behavior.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact files report 0.1.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
