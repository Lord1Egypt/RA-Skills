## Description:

DNS Doctor checks domain DNS and email authentication, explains findings, and provides validated DNS records for a human to review and publish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dnsdoctor](https://clawhub.ai/user/dnsdoctor)

### License/Terms of Use:

MIT-0

## Use Case:

Domain owners, email administrators, and developers use this skill to diagnose DNS and email authentication, understand domain and mail risks, and get validated DNS records to review and publish themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scans create public report pages that expose the checked domain.

Mitigation: Do not scan domains the user needs to keep private.

Risk: Email testing sends a selected message to the service, which shares a redacted excerpt with an AI provider; sensitive details may remain in the excerpt.

Mitigation: Use a non-sensitive email for testing.

Risk: Publishing a DNS record can affect mail delivery or domain policy.

Mitigation: Have the domain owner review proposed records and approve publication; use only the returned validated record.

Risk: Optional account reads use an API token, and calls past free limits may incur charges.

Mitigation: Supply a token only when account reads are wanted and authorize any paid calls.

## Reference(s):

- [DNS Doctor methodology](https://dnsdoctor.dev/methodology)
- [DNS Doctor API schema](https://dnsdoctor.dev/api/v1/openapi.json)
- [DNS Doctor MCP server](https://dnsdoctor.dev/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, DNS configuration, Guidance]

**Output Format:** [Markdown summaries with DNS findings, validated record strings, and API call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [DNS changes are presented for a human to review and publish.]

## Skill Version(s):

1.16.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
