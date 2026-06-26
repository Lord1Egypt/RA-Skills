## Description: <br>
Verify AI agent identity and reputation via ERC-8004 on-chain registries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SumeetChougule](https://clawhub.ai/user/SumeetChougule) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to check whether an AI agent has an ERC-8004 identity and to review on-chain reputation signals before deciding whether to trust it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional registration can spend real funds on gas, and the security review flags the current mainnet warning behavior as unsafe. <br>
Mitigation: Use read-only lookup mode with no wallet key configured when possible; before registering, use a dedicated low-balance wallet and explicitly choose a testnet unless mainnet registration is intended. <br>
Risk: Configuring a private key enables the skill's on-chain registration path. <br>
Mitigation: Avoid storing a private key for normal verification and reputation checks, and limit any registration key to a dedicated wallet. <br>


## Reference(s): <br>
- [ChaosChain Homepage](https://chaoscha.in) <br>
- [ChaosChain Documentation](https://docs.chaoscha.in) <br>
- [ERC-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004) <br>
- [8004scan.io Agent Explorer](https://8004scan.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands, configuration] <br>
**Output Format:** [Plain text or Markdown-style command responses with setup commands and JSON configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only lookups require no wallet key; optional registration can submit an on-chain transaction when a private key is configured.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
