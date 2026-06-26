## Description: <br>
COC Soul Immortality helps OpenClaw agents register on-chain identities, manage DID operations, encrypt and anchor backups to IPFS and SoulRegistry, configure guardian recovery, and restore or resurrect agent state across hosts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ngplateform](https://clawhub.ai/user/ngplateform) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve agent identity, memory, configuration, and recovery state across device loss or host migration. It provides runbooks and commands for COC testnet setup, backups, DID management, guardian recovery, and carrier-based resurrection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create wallet keys and handle recovery material for encrypted backups. <br>
Mitigation: Use dedicated testnet keys first, keep private keys and latest-recovery.json out of chat and version control, and transfer key material only through a local secure channel. <br>
Risk: Automatic backup features can send sensitive agent state to IPFS and anchor records on-chain before the operator fully understands the data scope. <br>
Mitigation: Review the backup scope, enable encryption before backup, and keep autoBackup and backupOnSessionEnd disabled until the operator accepts what leaves the host. <br>
Risk: Portable backups may include host-local credentials or policy files that should not move between machines. <br>
Mitigation: Exclude host-local API and model credentials from portable backups, preserve target-host auth settings during restore, and restore to a temporary directory before promoting any recovered state. <br>
Risk: Carrier resurrection hosts run recovered agent state and may expose sensitive data if operated without isolation. <br>
Mitigation: Use least-privilege carrier accounts, a restricted startup script, a trusted plugin allow list, and a persistent work directory with enough storage before accepting resurrection requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ngplateform/coc-soul) <br>
- [@chainofclaw/soul npm package](https://www.npmjs.com/package/@chainofclaw/soul) <br>
- [Backup and restore reference](artifact/references/backup.md) <br>
- [Configuration schema](artifact/references/config.md) <br>
- [DID identity management reference](artifact/references/did.md) <br>
- [Guardian recovery reference](artifact/references/guardian-recovery.md) <br>
- [Carrier operations reference](artifact/references/carrier.md) <br>
- [Companion claw-mem2db skill](https://clawhub.ai/ngplateform/claw-mem2db) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes safety checks for private keys, recovery packages, backup encryption modes, and restore targets.] <br>

## Skill Version(s): <br>
1.2.10 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
