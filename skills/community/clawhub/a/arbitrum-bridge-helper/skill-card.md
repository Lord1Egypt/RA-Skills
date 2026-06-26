## Description: <br>
Execute official Arbitrum bridge tasks with a wallet found on disk: deposits, withdrawals, claims, status checks, and stuck-bridge diagnosis across Ethereum, Arbitrum One, Arbitrum Nova, and testnets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[merdikim](https://clawhub.ai/user/merdikim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent plan, execute, track, claim, or diagnose official Arbitrum bridge flows while enforcing wallet-secret handling and confirmation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs an agent to find local wallet secrets and use them for real blockchain transactions. <br>
Mitigation: Use a dedicated low-balance wallet, explicitly specify the approved wallet address and secret location, and do not allow broad disk searches. <br>
Risk: Incorrect route, amount, asset, approval, or transaction confirmation could cause financial loss or unwanted bridge activity. <br>
Mitigation: Verify every route, amount, asset, approval, and transaction before giving the final confirmation to sign or broadcast. <br>


## Reference(s): <br>
- [Routes Reference](references/routes.md) <br>
- [Trigger Reference](references/triggers.md) <br>
- [Troubleshooting Reference](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands] <br>
**Output Format:** [Markdown with concise status updates, warnings, and transaction details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public wallet addresses and transaction hashes; must not include private keys, seed phrases, raw keystore contents, RPC credentials, or full secret-bearing files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
