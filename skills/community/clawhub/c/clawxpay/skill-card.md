## Description:

clawxpay is a pay-per-call API gateway that lets agents access market data, on-chain data, Web3 funding intelligence, China A-share data, and AI inference providers through x402 payments using a Base USDC wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biggggtreee-rgb](https://clawhub.ai/user/biggggtreee-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill when they need paid per-call access to professional market, on-chain, funding, A-share, and AI inference APIs without managing separate provider accounts or API keys. Agents should use it only after confirming the endpoint, estimated cost, wallet balance, and per-task budget with the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned npm package that creates a wallet during installation.

Mitigation: Verify the npm package provenance and exact version before installing or running examples.

Risk: The generated wallet private key is stored locally as plaintext.

Mitigation: Use a dedicated low-balance wallet, keep the key out of backups and logs, and do not let agents read or display ~/.clawxpay/wallet.key.

Risk: Paid API calls can spend USDC from the configured Base wallet.

Mitigation: Require explicit user approval before each paid call, check wallet balance first, set a per-task budget cap, and report spending after the task.

## Reference(s):

- [clawxpay homepage](https://clawxpay.com)
- [clawxpay API documentation](https://clawxpay.com/docs)
- [Base bridge](https://bridge.base.org)
- [BaseScan address lookup](https://basescan.org/address/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include paid API call plans, wallet balance checks, budget settings, and endpoint usage examples.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
