## Description: <br>
Helps agents operate @metamask/gator-cli for profile setup, EIP-7702 account upgrades, ERC-7710 delegation grants, redemptions, revocations, balance checks, and delegation inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AyushBherwani1998](https://clawhub.ai/user/AyushBherwani1998) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and wallet operators use this skill to choose the correct gator CLI commands, flags, profiles, grant scopes, and redemption actions for MetaMask smart-account delegation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports high-impact crypto wallet operations, including delegation grants, redemptions, revocations, raw calls, and function-call scopes. <br>
Mitigation: Use a testnet or low-value dedicated wallet, and verify every profile, chain, address, amount, scope, function signature, and raw payload before executing commands. <br>
Risk: Gator CLI profiles may store private keys in plaintext JSON under the user's home directory. <br>
Mitigation: Protect or remove ~/.gator-cli profiles when finished, avoid accounts with significant funds, and restrict access to machines where profiles are created. <br>


## Reference(s): <br>
- [MetaMask Smart Accounts Kit documentation](https://docs.metamask.io/smart-accounts-kit) <br>
- [Gator CLI ClawHub page](https://clawhub.ai/AyushBherwani1998/gator-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include wallet addresses, chain names, profile names, grant scopes, function signatures, transaction payload fields, and local configuration paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
