## Description: <br>
Mint 4Claw tokens on BSC through OpenClaw agents, including mint execution, mint status checks, and token information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xiaoyu022025](https://clawhub.ai/user/Xiaoyu022025) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users and agent operators use this skill to request signer authorizations and submit BSC transactions that mint 4Claw tokens or check mint status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a wallet private key to mint tokens, and passing a main wallet key to a command-line script can expose funds if the environment is compromised. <br>
Mitigation: Use only a fresh low-balance wallet funded with minimal gas and avoid using a primary wallet private key. <br>
Risk: The default signer service is a remote HTTP endpoint that participates in authorizing blockchain transactions. <br>
Mitigation: Prefer a trusted HTTPS endpoint or a self-hosted signer service with authenticated access and a fixed allowlisted contract. <br>
Risk: A signer or configuration mismatch could direct a mint attempt at an unexpected contract. <br>
Mitigation: Verify the exact BSC contract address before every transaction and review the transaction details before execution. <br>


## Reference(s): <br>
- [4Claw Mint ClawHub Release](https://clawhub.ai/Xiaoyu022025/4claw-mint) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Console text and JSON status output, with Markdown usage guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Mint output can include transaction hash, confirmed block, wallet balance, remaining public mint amount, cooldown details, or error text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
