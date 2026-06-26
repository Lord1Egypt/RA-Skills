## Description: <br>
USDC wallet operations for OpenClaw agents via Circle Developer-Controlled Wallets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eltontay](https://clawhub.ai/user/eltontay) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to configure Circle credentials, create developer-controlled wallets, check USDC balances, request sandbox testnet funds, and send USDC across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use production Circle credentials and initiate USDC transfers involving real funds. <br>
Mitigation: Use sandbox first and require explicit confirmation of recipient, amount, network, and funding source before allowing send operations. <br>
Risk: The skill stores API keys, entity secrets, wallet metadata, and default wallet state in a local configuration directory. <br>
Mitigation: Keep credentials out of shared logs and shells, restrict file permissions on ~/.openclaw/circle-wallet/, and back up wallet metadata before reconfiguring credentials. <br>
Risk: Setup or credential reconfiguration can remove local wallet metadata and default wallet state. <br>
Mitigation: Back up local wallet metadata before running setup or configure with new credentials. <br>


## Reference(s): <br>
- [ClawHub circle-wallet release page](https://clawhub.ai/eltontay/circle-wallet) <br>
- [Circle Developer Documentation](https://developers.circle.com) <br>
- [Circle Console](https://console.circle.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Circle API credentials and stores wallet configuration under ~/.openclaw/circle-wallet/.] <br>

## Skill Version(s): <br>
1.0.17 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
