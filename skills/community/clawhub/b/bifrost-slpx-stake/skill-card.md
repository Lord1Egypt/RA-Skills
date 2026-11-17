## Description:

Execute liquid staking operations on Bifrost SLPx across Ethereum, Base, Optimism, and Arbitrum, including staking ETH/WETH to mint vETH, redeeming vETH, and claiming completed redemptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ark930](https://clawhub.ai/user/ark930)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare or execute Bifrost vETH staking, redemption, and claim workflows across supported EVM chains. It defaults to manual signing and also documents optional agent-side signing when users explicitly configure a wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help prepare and optionally broadcast real staking transactions that move funds.

Mitigation: Prefer manual signing or a hardware wallet or keystore workflow, preview transaction details, and require explicit confirmation before write operations.

Risk: Agent-side signing can expose a wallet private key if users configure BIFROST_PRIVATE_KEY.

Mitigation: Use a dedicated minimally funded wallet, avoid primary wallet private keys, never display keys, and delete keys after use when possible.

## Reference(s):

- [Bifrost vETH page](https://www.bifrost.io/vtoken/veth)
- [Bifrost App vETH staking](https://app.bifrost.io/vstaking/vETH)
- [Bifrost Slpx Stake on ClawHub](https://clawhub.ai/ark930/skills/bifrost-slpx-stake)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with transaction details and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include unsigned transaction fields, calldata, pre-execution checks, optional cast commands, and block explorer links.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter metadata.version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
