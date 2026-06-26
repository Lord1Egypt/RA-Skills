## Description: <br>
Billions/Iden3 authentication and identity management tools for agents to link, prove, sign, and verify decentralized identities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ijangasbar](https://clawhub.ai/user/ijangasbar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to create and manage Billions/iden3 DIDs, link human and agent identities, sign challenges, and verify ownership proofs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores identity material, including private keys, in a local plaintext key store under $HOME/.openclaw/billions. <br>
Mitigation: Use it only on a trusted single-user machine and treat kms.json and related identity files as sensitive credentials. <br>
Risk: The skill can send signed identity proofs or verification links through OpenClaw direct messages. <br>
Mitigation: Confirm the recipient, challenge, and linking intent before running signing or human-agent linking commands. <br>


## Reference(s): <br>
- [Billions Network](https://billions.network/) <br>
- [ClawHub skill page](https://clawhub.ai/ijangasbar/billionsnetwork-verified-agent-identity-0-0-2) <br>
- [Publisher profile](https://clawhub.ai/user/ijangasbar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local identity setup, DID management, signed challenge, verification-link, and signature-verification workflows for an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact package.json reports 0.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
