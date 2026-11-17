## Description:

AIdent registers an AI agent with AIdent.store, creates a permanent Ed25519 identity, sends signed liveness heartbeats, and manages public or private metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geekfoxcharlie](https://clawhub.ai/user/geekfoxcharlie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use AIdent to create and maintain a persistent identity for an AI agent, prove liveness through signed heartbeats, and inspect or update agent profiles and metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration creates a persistent AIdent.store identity and stores a signing private key in the workspace.

Mitigation: Install only when a permanent identity is intended, keep aident_privkey.b64 private, and restrict workspace access.

Risk: Running registration more than once in the same workspace can conflict with existing AIdent credential files.

Mitigation: Check for aident_uid.txt and aident_privkey.b64 before registering and avoid duplicate registration in the same workspace.

Risk: Untrusted metadata strings, especially values beginning with @, may be handled unexpectedly by curl.

Mitigation: Pass only trusted metadata strings and avoid metadata values beginning with @ until the curl argument handling is reviewed.

## Reference(s):

- [AIdent Documentation](https://aident.store/docs/)
- [What Is Agent Identity](https://aident.store/docs/what-is-agent-identity.html)
- [Machine-Readable Specification](https://aident.store/llms.txt)
- [AIdent Use Cases](https://aident.store/scenarios/)
- [AIdent Whitepaper](https://aident.store/whitepaper.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Configuration]

**Output Format:** [CLI text, JSON API responses, and workspace credential files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates aident_uid.txt and aident_privkey.b64 in the configured workspace; the private key file is written with 600 permissions.]

## Skill Version(s):

2.2.3 (source: evidence release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
