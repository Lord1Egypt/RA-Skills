## Description: <br>
Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[desapetc](https://clawhub.ai/user/desapetc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to create and manage Billions Network decentralized identities, link agent DIDs to human owners, and generate or verify authentication proofs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent signing keys and may store private keys unencrypted by default. <br>
Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities, and restrict access to $HOME/.openclaw/billions. <br>
Risk: Importing an existing wallet private key can expose production credentials to the agent runtime. <br>
Mitigation: Use a newly generated identity or a non-production key dedicated to this skill. <br>
Risk: Signing challenges or linking a human to an agent can create durable identity associations. <br>
Mitigation: Require explicit user confirmation before running signing or human-agent linking commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/desapetc/agent-desapetc-123) <br>
- [Publisher Profile](https://clawhub.ai/user/desapetc) <br>
- [Billions Network](https://billions.network/) <br>
- [OpenClaw Environment Documentation](https://docs.openclaw.ai/help/environment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Node.js shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include DID strings, identity lists, signed challenge status, verification URLs, or signature verification results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
