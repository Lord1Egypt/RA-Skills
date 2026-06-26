## Description: <br>
Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kinetosgr](https://clawhub.ai/user/Kinetosgr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create and manage Billions Network decentralized identities, link an agent DID to a human owner, and sign or verify identity challenges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles identity and key material, including a private-key-backed DID and files under $HOME/.openclaw/billions. <br>
Mitigation: Use a dedicated agent identity, set BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities, and protect the local identity directory. <br>
Risk: The reviewed artifact describes Node.js scripts for identity operations, but those scripts were not included in the artifact. <br>
Mitigation: Only run referenced scripts when the installed package includes reviewable source and dependencies from a trusted source. <br>
Risk: Using an Ethereum private key that controls assets could expose funds or other authority during identity creation. <br>
Mitigation: Do not pass a wallet key that controls assets; use a dedicated key for the agent identity. <br>


## Reference(s): <br>
- [Billions Network](https://billions.network/) <br>
- [ClawHub skill page](https://clawhub.ai/Kinetosgr/agent156) <br>
- [Publisher profile: Kinetosgr](https://clawhub.ai/user/Kinetosgr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local identity files under $HOME/.openclaw/billions and Node.js scripts when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
