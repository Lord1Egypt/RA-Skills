## Description: <br>
AI-powered smart contract generator, analyzer, and deployer for BNB Chain (BSC/opBNB) that helps generate Solidity, run security analysis, compile and deploy contracts, verify source on BscScan/opBNBScan, interact with deployed contracts, or run a full generate-analyze-deploy-verify pipeline across BSC and opBNB chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sufnoobzac](https://clawhub.ai/user/sufnoobzac) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to drive smart contract workflows on BNB Chain from an agent: generate Solidity, analyze it, deploy to testnet or mainnet when explicitly configured, verify source, and interact with deployed contracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can use wallet keys to make automatic blockchain deployments and transactions. <br>
Mitigation: Use a dedicated low-value testnet wallet first, avoid production .env files, and require manual review before deploy, full, mainnet, or state-changing interact commands. <br>
Risk: Mainnet deployment proceeds automatically after a warning when a funded key is present and a mainnet chain is explicitly selected. <br>
Mitigation: Keep the default bsc-testnet chain for initial use and require explicit human approval before selecting bsc-mainnet or opbnb-mainnet. <br>
Risk: The full workflow can automatically modify generated contract source while attempting to fix high-severity findings before deployment. <br>
Mitigation: Use --skip-fix to disable automatic fixes or --skip-deploy to review the final source and analysis before any on-chain action. <br>
Risk: The skill requires API keys and may require a private key for deployment workflows. <br>
Mitigation: Provide scoped credentials only for the intended environment and verify which private-key variable the CLI actually reads before use. <br>


## Reference(s): <br>
- [ClawContract command reference](references/commands.md) <br>
- [ClawHub release page](https://clawhub.ai/sufnoobzac/clawcontract) <br>
- [Project homepage declared by skill](https://github.com/cvpfus/clawcontract) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; CLI workflows may produce Solidity source files and JSON deployment metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default chain is bsc-testnet; deploy and full workflows require user-provided credentials and can create on-chain transactions.] <br>

## Skill Version(s): <br>
1.0.8 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
