## Description: <br>
Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kondifun](https://clawhub.ai/user/Kondifun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and manage Billions Network decentralized identities, link an agent DID to a human owner, and sign or verify authentication challenges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-lived private keys may be stored in plaintext when BILLIONS_NETWORK_MASTER_KMS_KEY is not set. <br>
Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities and protect the configured master key. <br>
Risk: Importing valuable wallet private keys through command-line arguments can expose them through shell history or process inspection. <br>
Mitigation: Avoid passing valuable wallet keys on the command line; prefer generating a new dedicated agent identity when possible. <br>
Risk: $HOME/.openclaw/billions contains identity data, challenges, credentials, and key material. <br>
Mitigation: Treat the directory as sensitive secret storage, restrict local access, and include it in an appropriate secure backup process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Kondifun/artefact-144794446) <br>
- [Kondifun publisher profile](https://clawhub.ai/user/Kondifun) <br>
- [Billions Network](https://billions.network/) <br>
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scripts can produce DID strings, JSON identity lists, challenge strings, verification URLs, and signature verification status messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
