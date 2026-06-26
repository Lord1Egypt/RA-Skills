## Description: <br>
AWP (Agent Work Protocol) is a toolkit for agent mining on Base, Ethereum, Arbitrum, and BSC, covering onboarding, staking, allocation, worknet management, governance, and protocol queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kilb](https://clawhub.ai/user/kilb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide AWP-specific registration, wallet setup, staking, allocation, worknet lifecycle, governance, and status queries across supported EVM chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide signing and submitting AWP protocol transactions. <br>
Mitigation: Require clear user confirmation before relay, signature, staking, allocation, governance, or raw-call actions, and show transaction details before execution. <br>
Risk: The security summary flags high-impact transaction authority and an under-scoped raw call bridge. <br>
Mitigation: Use only AWP-specific contract allowlists and review contract, method, chain, and value parameters before any raw-call or wallet action. <br>
Risk: The security summary flags an unpinned remote wallet installer. <br>
Mitigation: Review any awp-wallet installation command before running it and prefer a pinned or manually verified wallet release. <br>
Risk: Wallet-backed protocol actions can affect funds or allocations. <br>
Mitigation: Keep minimal funds in the agent wallet and prefer the least privileged workflow available for the user's task. <br>


## Reference(s): <br>
- [AWP Skill ClawHub Page](https://clawhub.ai/kilb/awp) <br>
- [AWP Skill Homepage](https://github.com/awp-core/awp-skill) <br>
- [AWP Wallet](https://github.com/awp-core/awp-wallet) <br>
- [AWP Skill API Reference](artifact/references/api-reference.md) <br>
- [AWP Protocol Reference (V2)](artifact/references/protocol.md) <br>
- [AWP Staking Commands](artifact/references/commands-staking.md) <br>
- [AWP Worknet Commands](artifact/references/commands-worknet.md) <br>
- [AWP Governance Commands](artifact/references/commands-governance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and file or configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transaction previews, API query results, next commands, and wallet or protocol risk warnings.] <br>

## Skill Version(s): <br>
1.7.0 (source: SKILL.md frontmatter, CHANGELOG, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
