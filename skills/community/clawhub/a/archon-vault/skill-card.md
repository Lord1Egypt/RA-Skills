## Description: <br>
Archon Vault manages encrypted Archon DID vaults for client-side encrypted backups, restores, disaster recovery, and multi-party vault access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[macterra](https://clawhub.ai/user/macterra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create and manage Archon DID vaults, add or remove vault members, and back up or restore workspace, configuration, and memory files. It is suited for encrypted distributed backup workflows that require client-side encryption and controlled sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create broad workspace, configuration, and memory backups that may include sensitive local data. <br>
Mitigation: Review the backup scope and .backup-ignore before running backup scripts, and verify restored files before merging them into a live environment. <br>
Risk: Recovery workflows depend on sensitive Archon wallet material, passphrases, and a 12-word mnemonic. <br>
Mitigation: Protect ~/.archon.env with restrictive permissions, store the mnemonic offline, and avoid passing the mnemonic directly in shell commands where it can be exposed through shell history or process listings. <br>
Risk: The scripts dynamically invoke the @didcid/keymaster package and default to a public gatekeeper URL. <br>
Mitigation: Use this skill only when the package and Archon service are trusted, and confirm ARCHON_GATEKEEPER_URL before backup or recovery operations. <br>
Risk: Temporary archives may remain in /tmp during backup verification or failed cleanup paths. <br>
Mitigation: Remove leftover temporary backup archives after verification or recovery, especially on shared systems. <br>


## Reference(s): <br>
- [Archon Vault ClawHub Page](https://clawhub.ai/macterra/archon-vault) <br>
- [Archon Gatekeeper](https://archon.technology) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local backup archives, restored files, environment variables, and Archon vault identifiers.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
