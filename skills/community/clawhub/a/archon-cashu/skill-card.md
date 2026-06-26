## Description: <br>
Cashu ecash operations integrated with Archon DID for P2PK-locked tokens. Send and receive sats using DID-derived pubkeys, backup wallets to vault. Use for Cashu token operations, DID-locked payments, or ecash wallet management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[macterra](https://clawhub.ai/user/macterra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Cashu ecash wallets, mint and send tokens, create DID-locked payments, receive tokens from dmail, and configure wallet backup or npub.cash workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet backup can expose sensitive wallet data by uploading an unencrypted archive to IPFS while describing it as encrypted vault backup. <br>
Mitigation: Do not run backup.sh for a real wallet unless client-side encryption is added first or IPFS upload is disabled. <br>
Risk: Fund-moving commands depend on local configuration, npx package execution, and wallet paths. <br>
Mitigation: Use small funds until the scripts, package sources, and config file paths have been reviewed in the target environment. <br>


## Reference(s): <br>
- [Nutshell Cashu CLI](https://github.com/cashubtc/nutshell) <br>
- [Archon](https://github.com/ArcHive-tech/archon) <br>
- [LNbits](https://lnbits.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce fund-moving command guidance that depends on local Archon, Cashu, npx, curl, jq, and node setup.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
