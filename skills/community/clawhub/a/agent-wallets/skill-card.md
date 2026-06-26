## Description: <br>
Route wallet workflows for agents that need to generate or import wallets using either a seed phrase or private key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beardkoda](https://clawhub.ai/user/beardkoda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to route wallet setup, balance checks, and transaction sends with viem while keeping signer secrets hidden and requiring confirmation for sensitive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet workflows can expose seed phrases or private keys if secrets are printed, logged, or stored insecurely. <br>
Mitigation: Use an encrypted secret store or key manager, mask secret material in all outputs, and confirm that secrets were not exposed before completing wallet setup. <br>
Risk: Transaction-send workflows can move funds on the wrong chain, to the wrong recipient, or with unintended fees. <br>
Mitigation: Verify chain, recipient, amount, and fees before sending; default to read-only or testnet behavior when details are missing; require explicit confirmation before broadcast. <br>
Risk: A compromised or high-value wallet increases the impact of any mistake or agent misuse. <br>
Mitigation: Start with a new or low-value wallet, keep backups secure, and ensure keys can be rotated or deleted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/beardkoda/agent-wallets) <br>
- [Publisher Profile](https://clawhub.ai/user/beardkoda) <br>
- [Root Skill Definition](artifact/SKILL.md) <br>
- [Local Wallet Router](artifact/local-wallet/SKILL.md) <br>
- [Wallet Generation Flow](artifact/local-wallet/generate/SKILL.md) <br>
- [Balance Check Flow](artifact/local-wallet/balance/SKILL.md) <br>
- [Transaction Send Flow](artifact/local-wallet/send/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with TypeScript examples and structured wallet response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses include action, chain, address, txHash, status, and next_step fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
