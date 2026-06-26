## Description: <br>
Exfer helps agents operate a wallet on the Exfer proof-of-work blockchain for payments, balances, mining, and contract flows such as HTLCs and escrow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahuman-exfer](https://clawhub.ai/user/ahuman-exfer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Exfer to create wallets, query balances, send EXFER payments, mine blocks, and coordinate machine-to-machine settlement patterns including HTLCs, multisig, vaults, escrow, and delegation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can initiate wallet, payment, mining, or contract actions involving EXFER funds. <br>
Mitigation: Use a dedicated low-balance wallet and require explicit human approval for each transfer or contract action. <br>
Risk: The skill requires sensitive wallet passphrase handling through EXFER_PASS and wallet backup files. <br>
Mitigation: Protect EXFER_PASS and wallet backups; avoid sharing them with untrusted agents or environments. <br>
Risk: The release was flagged as suspicious because it grants real wallet/payment authority and needs careful install and safety review. <br>
Mitigation: Verify downloaded binaries before running them, prefer a trusted RPC node, and review the skill before deployment. <br>


## Reference(s): <br>
- [ClawHub Exfer listing](https://clawhub.ai/ahuman-exfer/exfer) <br>
- [Exfer source repository](https://github.com/ahuman-exfer/exfer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EXFER_PASS for passphrase-based automation and may guide agents through wallet, payment, mining, and contract actions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
