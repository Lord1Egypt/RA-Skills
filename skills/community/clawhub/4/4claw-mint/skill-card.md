## Description:

Mint 4Claw tokens on BSC through OpenClaw agents using an authorized signer service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyu022025](https://clawhub.ai/user/xiaoyu022025)

### License/Terms of Use:


## Use Case:

External developers and OpenClaw agent operators use this skill to mint 4Claw tokens on BSC, check mint status, and understand the token minting constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw wallet private keys can be exposed if pasted into commands, shell history, logs, or shared terminals.

Mitigation: Use purpose-limited agent wallets, avoid funded wallet keys, and pass secrets through secure local secret handling where available.

Risk: The signer service URL is security-critical because it provides authorization data and the contract address used for on-chain minting.

Mitigation: Prefer HTTPS, verify the signer operator, and pin or independently confirm the expected contract address before submitting transactions.

Risk: An unauthenticated public signer service can be abused or used to misdirect minting activity.

Mitigation: Run the signer behind authentication with durable rate limits and request body-size limits; do not expose it publicly without these controls.

## Reference(s):

- [4Claw Mint ClawHub Page](https://clawhub.ai/xiaoyu022025/skills/4claw-mint)
- [Default Signer Service Endpoint](http://43.160.201.224:3456)
- [BSC RPC Endpoint](https://bsc-dataseed1.binance.org)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BSC wallet private key, signer service URL, BNB for gas, and network access to the BSC RPC endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
