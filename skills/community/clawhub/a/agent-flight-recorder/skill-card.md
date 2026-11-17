## Description:

Creates a Cryptowerk-backed, cryptographically verifiable audit trail for OpenClaw agent executions by registering SHA-256 file hashes, fetching blockchain seals, and verifying proofs with local sidecar artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptowerk-main](https://clawhub.ai/user/cryptowerk-main)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add proof-of-existence and later verification to AI workflow files, decisions, logs, and data artifacts while preserving privacy by registering hashes rather than raw content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Cryptowerk's external API for registration, seal retrieval, credential issuance, and verification.

Mitigation: Use it only in environments where outbound requests to Cryptowerk are approved and where submitted hashes and lookup metadata are acceptable for that workflow.

Risk: The bundled cwconfig.json contains credential-like values and the skill can persist credentials in the skill directory.

Mitigation: Treat bundled values as exposed, replace them with user-provided or secret-manager credentials, keep credential files out of synced or committed directories, and restrict file permissions.

Risk: Proof metadata is stored in local <file>.cwseal sidecar files.

Mitigation: Keep sidecar files with the audited artifacts, protect them from unauthorized modification, and review their contents before sharing.

## Reference(s):

- [Agent Flight Recorder on ClawHub](https://clawhub.ai/cryptowerk-main/skills/agent-flight-recorder)
- [Cryptowerk](https://www.cryptowerk.com)
- [Cryptowerk API Notes](references/cryptowerk-api-notes.md)
- [Storage and State](references/storage-and-state.md)
- [Cryptowerk Register API](https://aiagent.cryptowerk.com/platform/API/v8/register)
- [Cryptowerk Get Seal API](https://aiagent.cryptowerk.com/platform/API/v8/getseal)
- [Cryptowerk Verify Seal API](https://aiagent.cryptowerk.com/platform/API/v8/verifyseal)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python script commands and local JSON sidecar files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces retrieval IDs, seals, and verification results through Cryptowerk proof APIs; stores proof metadata in <file>.cwseal sidecar files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
