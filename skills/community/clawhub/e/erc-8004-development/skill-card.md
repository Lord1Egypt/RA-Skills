## Description: <br>
Build with ERC-8004 Trustless Agents for on-chain agent identity, reputation, validation, and discovery on EVM chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers building EVM-based agent identity, reputation, validation, and discovery workflows use this skill to register agents, configure agent metadata, integrate Agent0 SDK calls, and reason about feedback and search flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet keys or signing credentials could be exposed or used for unintended transactions. <br>
Mitigation: Use a dedicated low-value or testnet wallet, keep production private keys out of examples, and review every transaction before signing. <br>
Risk: On-chain, IPFS, registration, and feedback data may be public and difficult to remove. <br>
Mitigation: Avoid publishing sensitive information in registration files, feedback files, endpoint metadata, or transaction payloads. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tenequm/erc-8004-development) <br>
- [Publisher Profile](https://clawhub.ai/user/tenequm) <br>
- [Homepage](https://github.com/tenequm/skills/tree/main/skills/erc-8004) <br>
- [ERC-8004 Specification](references/spec.md) <br>
- [Smart Contracts](references/contracts.md) <br>
- [Registration Guide](references/registration.md) <br>
- [Reputation Guide](references/reputation.md) <br>
- [Search and Discovery](references/search-discovery.md) <br>
- [Agent0 TypeScript SDK Reference](references/sdk-typescript.md) <br>
- [OASF Taxonomy](references/oasf-taxonomy.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with TypeScript, JSON, Solidity, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet, RPC, IPFS, and on-chain transaction examples that require user review before execution.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
