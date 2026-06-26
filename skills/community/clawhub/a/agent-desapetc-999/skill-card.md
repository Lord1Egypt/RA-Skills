## Description: <br>
Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[desapetc](https://clawhub.ai/user/desapetc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and manage Billions Network decentralized identities, sign identity challenges, verify signatures, and link an agent DID to a human owner. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may maintain long-lived private keys for a Billions identity. <br>
Mitigation: Install it only when persistent agent identity is intended, and configure BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing an identity. <br>
Risk: Private keys can be passed with --key and may be exposed on shared or logged systems. <br>
Mitigation: Avoid passing private keys on the command line in shared environments; prefer generated identities or a protected setup path. <br>
Risk: Signing and linking flows can bind an agent identity to a human identity or verification flow. <br>
Mitigation: Approve signing or linking only after confirming who requested it and where the resulting wallet verification flow will go. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/desapetc/agent-desapetc-999) <br>
- [Publisher Profile](https://clawhub.ai/user/desapetc) <br>
- [Billions Network](https://billions.network/) <br>
- [OpenClaw Environment Documentation](https://docs.openclaw.ai/help/environment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or read persistent DID, challenge, credential, and key files under $HOME/.openclaw/billions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
