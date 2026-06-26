## Description: <br>
Billions/Iden3 authentication and identity management tools for agents that create, link, sign, and verify decentralized identities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ian4jpg](https://clawhub.ai/user/ian4jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and manage Billions Network DIDs, link an agent identity to a human owner, and verify DID ownership through signed challenges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or import identity keys and stores agent private keys locally in plaintext. <br>
Mitigation: Use a dedicated low-value identity, avoid passing private keys through chat or shared command history, and restrict access to $HOME/.openclaw/billions. <br>
Risk: The skill can send signed identity proofs or verification links through OpenClaw messages. <br>
Mitigation: Verify the recipient and challenge before running sign or link commands, and stop if any script reports an error. <br>
Risk: Identity and challenge files persist outside the workspace. <br>
Mitigation: Review local retention requirements and remove unused identities or challenges when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ian4jpg/billionsnetwork-verified-agent-identity) <br>
- [Billions Network](https://billions.network/) <br>
- [Billions Wallet](https://wallet.billions.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; script outputs are plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write identity and challenge data under $HOME/.openclaw/billions and may send OpenClaw messages when linking or signing.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
