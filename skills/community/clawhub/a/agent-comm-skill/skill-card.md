## Description:

Enables DID registration, cryptographic signing, verification, relay connection, and end-to-end encryption for secure AI agent communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[404-unknow](https://clawhub.ai/user/404-unknow)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to register local agent identities, sign and verify messages, connect to relay sessions, and encrypt or decrypt shared secrets for agent communication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release under-declares network and signing capabilities.

Mitigation: Review and constrain manifest permissions and exposed actions before deployment.

Risk: Private-key signing operations can affect agent identity trust.

Mitigation: Require explicit authorization for each private-key signing operation and validate identity IDs before use.

Risk: Relay connections and local key storage may expose credentials or agent identities if used without controls.

Mitigation: Use wss:// or trusted local-only relays, protect local key storage, and update dependencies before handling real credentials or identities.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/404-unknow/skills/agent-comm-skill)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Cryptographic signatures, Configuration]

**Output Format:** [JSON action results with string identifiers, signatures, keys, ciphertext, and status values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local agent identifiers, DID strings, public keys, signatures, verification results, relay connection status, session keys, ciphertext, nonces, and decrypted payloads.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
