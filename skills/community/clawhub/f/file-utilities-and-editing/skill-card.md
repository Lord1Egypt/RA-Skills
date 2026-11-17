## Description:

File Utilities And Editing provides AgentPMT-hosted remote file utility calls for MIME lookup, path manipulation, CSV and JSON formatting, Base64 encoding and decoding, and hash generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to call AgentPMT file utilities for MIME detection, path parsing and normalization, size formatting, CSV and JSON formatting, Base64 text transforms, and content hashing without local filesystem access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote tool inputs are processed by AgentPMT as an external service.

Mitigation: Do not send secrets, private keys, credentials, confidential documents, or unnecessary personal or business data.

Risk: Unpinned npx-based setup examples can run package code during installation.

Mitigation: Prefer the OpenClaw route, or pin and review any npx-based setup before running it.

Risk: Base64 decoding is limited to valid UTF-8 text.

Mitigation: Use a binary-safe workflow for payloads that may contain non-UTF-8 data.

## Reference(s):

- [File Utilities And Editing ClawHub Page](https://clawhub.ai/agentpmt/skills/file-utilities-and-editing)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/file-utilities-and-editing)
- [File Utilities and Editing Schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [JSON responses containing text strings, structured fields, hashes, MIME metadata, paths, or ASCII tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stateless remote calls; inputs are string-based and the skill does not read from or write to the local filesystem.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
