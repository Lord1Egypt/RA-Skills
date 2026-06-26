## Description: <br>
Billions decentralized identity for agents that links agents to human identities using Billions ERC-8004 and Attestation Registries, and verifies or generates authentication proofs based on the iden3 self-sovereign identity protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kondifun](https://clawhub.ai/user/Kondifun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and manage agent DIDs, sign identity challenges, link agent identities to human owners, and verify DID ownership proofs on the Billions Network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable agent signing keys may be stored locally in plaintext if encryption is not configured. <br>
Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities and protect $HOME/.openclaw/billions from backups or other users. <br>
Risk: Using valuable existing private keys on the command line can expose sensitive key material through local shell or process history. <br>
Mitigation: Prefer generated agent-specific identities or use a controlled secret-handling process when importing keys. <br>
Risk: DID creation, linking, and verification may contact Billions and Privado resolver services. <br>
Mitigation: Deploy only where these network interactions are expected and acceptable for the agent identity workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Kondifun/artefact-144794444) <br>
- [Publisher profile](https://clawhub.ai/user/Kondifun) <br>
- [Billions Network](https://billions.network/) <br>
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON or string script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and stores DID identity state under $HOME/.openclaw/billions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
