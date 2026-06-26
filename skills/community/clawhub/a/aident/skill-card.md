## Description: <br>
AIdent registers an AI agent on AIdent.store with a permanent Ed25519 identity, signed heartbeats, profile lookup, and public or private metadata storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geekfoxcharlie](https://clawhub.ai/user/geekfoxcharlie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use AIdent to create and manage a persistent registry identity for an agent, send liveness heartbeats, inspect registry profiles, and store small JSON metadata records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a local Ed25519 private key that controls the registered agent identity. <br>
Mitigation: Keep aident_privkey.b64 private, back it up securely, and do not commit or share it. <br>
Risk: Registration, profile, heartbeat, and metadata commands can send user-provided data to AIdent.store. <br>
Mitigation: Review names, creator fields, links, and JSON metadata before sending; do not include passwords, API keys, seed phrases, or sensitive personal data. <br>


## Reference(s): <br>
- [AIdent Documentation](https://aident.store/docs/) <br>
- [What Is Agent Identity](https://aident.store/docs/what-is-agent-identity.html) <br>
- [AIdent Machine-Readable Specification](https://aident.store/llms.txt) <br>
- [AIdent Use Cases](https://aident.store/scenarios/) <br>
- [AIdent Whitepaper](https://aident.store/whitepaper.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Plain text and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local UID and Ed25519 private-key files and may send signed registry, heartbeat, profile, and metadata requests to AIdent.store.] <br>

## Skill Version(s): <br>
2.2.3 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
