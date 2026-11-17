## Description:

Check USDC balance on Base Mainnet for your Fluora wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chetan-guevara](https://clawhub.ai/user/chetan-guevara)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to check the USDC balance for a Fluora wallet configured on Base Mainnet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the local Fluora wallet metadata file and sends the wallet address to the Base public RPC endpoint for a read-only balance query.

Mitigation: Use it only for Fluora/Base USDC balance checks and avoid running it where exposing the wallet address to a public RPC endpoint is unacceptable.

Risk: Server security guidance notes a vulnerable transitive dependency caution.

Mitigation: Keep the package lockfile in use and update the vulnerable transitive dependency when a fixed version is available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chetan-guevara/skills/fluora-balance)
- [Base Mainnet RPC endpoint](https://mainnet.base.org)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text console output with optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports wallet address, formatted USDC balance, token symbol, and raw balance when JSON output is requested.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
