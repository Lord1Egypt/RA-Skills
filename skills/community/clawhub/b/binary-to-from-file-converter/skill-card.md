## Description:

Converts data between base64, hexadecimal, and binary representations, and converts files to and from base64 through AgentPMT-hosted tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to encode or decode payloads, inspect binary content, and create temporary downloadable files from base64 data in AgentPMT workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File contents may be sent to the AgentPMT remote service for conversion.

Mitigation: Use the skill only for content intended for AgentPMT processing, and avoid private documents, credentials, customer data, or proprietary files unless that transfer is approved.

Risk: Decoded files may be stored in cloud storage and returned through signed URLs.

Mitigation: Use the shortest practical expiration period and treat signed URLs as temporary secrets.

Risk: The setup path may include unpinned npx commands.

Mitigation: Review or pin the install source before using npx-based setup in production environments.

## Reference(s):

- [Generated action schema](artifact/schema.md)
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/binary-to-from-file-converter)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/binary-to-from-file-converter)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [Guidance, Text, Files, Configuration]

**Output Format:** [Markdown guidance for tool calls and JSON responses from the hosted converter]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote results can include converted strings, byte counts, file IDs, MIME types, and signed download URLs; inline file-to-base64 output is limited to 10 MB.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
