## Description: <br>
Build and test Solidity smart contracts with the Foundry toolkit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to build, test, debug, configure, and deploy Ethereum/EVM smart contracts with Foundry tools such as forge, cast, anvil, and chisel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deployment and transaction examples can spend real funds when used with broadcast, forge create, cast send, live RPC endpoints, or funded deployer wallets. <br>
Mitigation: Use testnets or limited deployer wallets, dry-run first, confirm chain ID, RPC endpoint, account, and balance, and require explicit approval before signing or broadcasting transactions. <br>
Risk: The skill references private keys, RPC URLs, and explorer API keys that could be exposed in terminals, shell history, or CI logs. <br>
Mitigation: Use secret storage for credentials, avoid pasting seed phrases or main-wallet keys, and review CI output and command history for accidental disclosure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/foundry-solidity) <br>
- [Skill homepage](https://github.com/tenequm/skills/tree/main/skills/foundry-solidity) <br>
- [Foundry Testing Guide](references/testing.md) <br>
- [forge-std API Reference](references/forge-std-api.md) <br>
- [Modern Solidity (0.8.30)](references/solidity-modern.md) <br>
- [Foundry Deployment Guide](references/deployment.md) <br>
- [Foundry Configuration Reference](references/configuration.md) <br>
- [Solidity Gas Optimization Guide](references/gas-optimization.md) <br>
- [Solidity Patterns and Idioms](references/patterns.md) <br>
- [Solidity Security and Audit Patterns](references/security.md) <br>
- [Foundry and Solidity Resources](references/resources.md) <br>
- [Debugging Workflows](references/debugging.md) <br>
- [Dependency Management](references/dependencies.md) <br>
- [CI/CD Integration](references/cicd.md) <br>
- [Chisel REPL](references/chisel.md) <br>
- [Cast Advanced Usage](references/cast-advanced.md) <br>
- [Anvil Advanced Usage](references/anvil-advanced.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Solidity, TOML, YAML, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Foundry command examples, smart contract snippets, deployment scripts, and configuration guidance.] <br>

## Skill Version(s): <br>
0.2.2 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
