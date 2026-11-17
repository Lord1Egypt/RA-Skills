## Description:

CTlogs MCP connects an assistant to the hosted CTlogs.io Model Context Protocol server for read-only Certificate Transparency lookups of domains, hostnames, certificate history, fingerprints, index status, and account quota.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abtdomain](https://clawhub.ai/user/abtdomain)

### License/Terms of Use:

MIT-0

## Use Case:

Security, infrastructure, and brand-protection teams use this skill to let an assistant query public Certificate Transparency records for subdomain discovery, certificate history, issuer details, fingerprint lookup, hostname search, index freshness, and remaining account quota.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries use the connected CTlogs account allowance even though the tools are read-only.

Mitigation: Review the CTlogs plan, OAuth approval screen, and client MCP settings before connecting an assistant.

Risk: Certificate Transparency records show certificate issuance metadata, not whether a host is currently live or what it serves.

Mitigation: Treat CT lookup results as leads for security or brand-protection review and verify conclusions with additional operational checks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abtdomain/skills/certificate-transparency)
- [CTlogs.io](https://ctlogs.io)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [CTlogs API Documentation](https://ctlogs.io/docs)
- [What Certificate Transparency Actually Tells You](https://ctlogs.io/blog/what-certificate-transparency-actually-tells-you)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline bash and JSON configuration examples; connected MCP tools return read-only Certificate Transparency lookup results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CTlogs account with an active plan and OAuth approval in the MCP client.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
