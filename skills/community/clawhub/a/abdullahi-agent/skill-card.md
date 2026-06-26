## Description: <br>
Billions decentralized identity for agents that helps create and manage DIDs, link agents to human identities, and verify authentication proofs using Billions ERC-8004 and Attestation Registries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Abdallah349193](https://clawhub.ai/user/Abdallah349193) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create or import local agent identities, link agent DIDs to human owners, sign identity challenges, and verify DID ownership. It is intended for decentralized identity workflows that depend on Billions Network and iden3-compatible proofs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or import identity private keys and store long-lived signing material under $HOME/.openclaw/billions. <br>
Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities, protect kms.json as sensitive material, and avoid importing valuable production Ethereum keys. <br>
Risk: Human-agent linking depends on a Billions verification URL flow that can bind an agent DID to a real human identity. <br>
Mitigation: Review the generated linking URL and use the flow only when the human identity relationship is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Abdallah349193/abdullahi-agent) <br>
- [Billions Network](https://billions.network/) <br>
- [Publisher profile](https://clawhub.ai/user/Abdallah349193) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON outputs from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and may use BILLIONS_NETWORK_MASTER_KMS_KEY to encrypt locally stored identity keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
