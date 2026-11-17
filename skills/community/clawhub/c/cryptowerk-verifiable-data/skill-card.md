## Description:

Use Cryptowerk to register document and data hashes, fetch seals, and verify proofs for files or append-only records while preserving source-data privacy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[holgercw](https://clawhub.ai/user/holgercw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Cryptowerk-backed proof-of-existence workflows to files or append-only records. It helps an agent register hashes, retrieve seals, and verify proofs while keeping local sidecar artifacts for audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill embeds and provisions service credentials, then stores issued credentials locally.

Mitigation: Keep the skill directory private, use protected user-supplied credentials when available, and prefer a release that removes the embedded bootstrap credential.

Risk: Credential and proof sidecar files can be written into local project trees.

Mitigation: Exclude cwconfig.json and .cwseal files from commits and backups when appropriate, and store them outside watched data trees.

Risk: The workflow sends hashes and proof requests to Cryptowerk APIs.

Mitigation: Use the skill only when external Cryptowerk API calls are acceptable for the deployment environment.

## Reference(s):

- [Cryptowerk API Notes](references/cryptowerk-api-notes.md)
- [Storage and State](references/storage-and-state.md)
- [Cryptowerk](https://www.cryptowerk.com)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Files, Text, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local .cwseal sidecar files and may create local credential state in cwconfig.json.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
