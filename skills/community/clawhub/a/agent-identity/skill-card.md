## Description: <br>
Cryptographic identity for AI agents that can register on-chain identities, sign messages, verify other agents, link platform accounts, and stake USDC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosepuppy](https://clawhub.ai/user/rosepuppy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to give agents a cryptographic identity, sign and verify messages, connect platform accounts, and inspect on-chain identity records. It also supports USDC staking actions for registration and vouching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and uses a durable local private key for signing and blockchain transactions. <br>
Mitigation: Use a fresh low-value key dedicated to this skill, protect the key file, and avoid importing a primary wallet key. <br>
Risk: Registration, linking, and vouching can approve or stake USDC and submit on-chain transactions. <br>
Mitigation: Require manual review before running transaction scripts, verify the registry contract and REGISTRY_ADDRESS, and do not allow these commands to run automatically. <br>
Risk: Identity and reputation outputs depend on registry data and linked account claims. <br>
Mitigation: Treat lookup and verification results as identity signals rather than absolute trust decisions, and corroborate high-impact actions through independent checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rosepuppy/agent-identity) <br>
- [Project homepage](https://github.com/g1itchbot8888-del/agent-identity) <br>
- [Publisher profile](https://clawhub.ai/user/rosepuppy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local key file and may submit blockchain transactions when transaction scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
