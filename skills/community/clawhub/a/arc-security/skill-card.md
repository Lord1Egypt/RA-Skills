## Description: <br>
Chain-agnostic security infrastructure for ClawHub/OpenClaw skills that checks skill trust, supports USDC-backed bonding, paid skill access, malicious-skill reporting, governance voting, and auditor earnings withdrawal on Arc and supported testnet chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shaivpidadi](https://clawhub.ai/user/Shaivpidadi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, auditors, and ClawHub users use this skill to inspect a skill's on-chain trust status, pay for verified skill access, stake USDC to vouch for skill safety, submit malicious-skill claims, vote in governance, and withdraw auditor earnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for raw wallet signing authority and can automatically spend funds through approval, payment, bonding, reporting, voting, claim, and withdrawal flows. <br>
Mitigation: Use only a dedicated low-value wallet or testnet key, and run transaction-producing commands only after confirming the chain, contract, recipient, amount, and action. <br>
Risk: The x402 use flow can download and extract remote ZIP packages after payment. <br>
Mitigation: Treat downloaded packages as untrusted until independently verified, and do not run extracted code before review and scanning. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Shaivpidadi/arc-security) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill manifest](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [CLI text output, transaction status strings, JSON-like result dictionaries, and downloaded skill package files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate wallet-signed blockchain transactions and may write or extract downloaded skill package files during paid skill use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact/skill.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
