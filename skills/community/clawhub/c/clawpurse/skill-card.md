## Description: <br>
ClawPurse is a local Neutaro chain wallet for managing NTMPI tokens, including balance checks, transfers, transaction history, staking, and allowlist enforcement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mhue-ai](https://clawhub.ai/user/mhue-ai) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Agents, automation developers, and wallet operators use ClawPurse to initialize and manage local Neutaro wallets, check balances, send or receive NTMPI, stake tokens, and apply transaction guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-facing wallet operations can move or stake real funds. <br>
Mitigation: Use low-balance wallets, review transactions before execution, and restrict automation to controlled payment and staking workflows. <br>
Risk: Confirmation and allowlist bypass flags can reduce transaction guardrails. <br>
Mitigation: Avoid --override-allowlist and --yes except in tightly controlled automation, and prefer enforced destination allowlists with per-address limits. <br>
Risk: Wallet secrets and local receipts can expose sensitive operational data on shared or backed-up machines. <br>
Mitigation: Keep mnemonics out of environment variables and command history, protect keystore access, and review plaintext receipt storage policies. <br>


## Reference(s): <br>
- [ClawPurse ClawHub release page](https://clawhub.ai/mhue-ai/clawpurse) <br>
- [Agent integration guide](SKILL.md) <br>
- [Operator guide](docs/OPERATOR-GUIDE.md) <br>
- [Trust model](docs/TRUST-MODEL.md) <br>
- [Allowlist guide](docs/ALLOWLIST.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, TypeScript examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes wallet setup, transaction operations, staking workflows, allowlist configuration, and security practices.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
