## Description: <br>
Enables DID registration, Ed25519 signing and verification, relay connection, and end-to-end encryption for secure AI agent communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[404-UNKNOW](https://clawhub.ai/user/404-UNKNOW) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to give agents local identities, sign and verify messages, connect to relay servers, and encrypt or decrypt shared secrets for coordinated agent communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles relay networking and persistent signing keys. <br>
Mitigation: Install only from trusted publishers, use trusted wss:// relay endpoints, and control which agents can invoke networking and signing actions. <br>
Risk: Signing keys stored under data/keystore can impersonate local agent identities if exposed. <br>
Mitigation: Protect or remove the data/keystore directory when no longer needed, and keep alias and localId values constrained. <br>
Risk: Broadcasting sensitive plaintext could expose confidential data through the relay path. <br>
Mitigation: Encrypt sensitive payloads before broadcast and avoid sending plaintext secrets through relay updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/404-UNKNOW/agent-comm-skill) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Configuration] <br>
**Output Format:** [Structured JSON action results containing identifiers, signatures, verification status, connection status, keys, ciphertext, nonce, or decrypted payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions include agent.register, message.sign, message.verify, network.connect, network.broadcast, secret.genKey, secret.encrypt, and secret.decrypt.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
