## Description: <br>
Check USDC balance on Base Mainnet for your Fluora wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chetan-guevara](https://clawhub.ai/user/chetan-guevara) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to check the USDC balance for a Fluora wallet configured in their local Fluora wallet file. The skill supports human-readable output and JSON output for programmatic parsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill prints a wallet address and USDC balance, which may be sensitive if shared publicly. <br>
Mitigation: Avoid posting terminal output or JSON output in public channels unless the wallet address and balance are intended to be disclosed. <br>
Risk: The script installs and runs Node dependencies before querying Base Mainnet. <br>
Mitigation: Run npm install only from the included scripts directory and use the provided lockfile. <br>
Risk: Balance lookup depends on Base Mainnet RPC availability and the local Fluora wallet file. <br>
Mitigation: Retry transient network failures and confirm ~/.fluora/wallets.json contains the expected USDC_BASE_MAINNET.address entry. <br>


## Reference(s): <br>
- [Fluora Balance on ClawHub](https://clawhub.ai/chetan-guevara/fluora-balance) <br>
- [Base Mainnet RPC](https://mainnet.base.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text balance output with optional JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a local Fluora wallet address and queries Base Mainnet through ethers.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
