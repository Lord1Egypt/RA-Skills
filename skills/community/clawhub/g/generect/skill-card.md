## Description:

Search B2B leads and companies, find and validate business emails, and support prospecting and enrichment workflows via the Generect Live API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vokaplok](https://clawhub.ai/user/vokaplok)

### License/Terms of Use:


## Use Case:

Developers and go-to-market operators use this skill to search leads and companies by ICP, retrieve enriched profiles, generate likely business emails from names and domains, and validate email addresses through Generect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends contact, prospecting, and email-address data to the third-party Generect API.

Mitigation: Use only data you are allowed to send to Generect and require user confirmation before submitting personal or prospecting data.

Risk: The artifact references using an unpinned npm package for the optional MCP server.

Mitigation: Prefer pinned and reviewed package versions over @latest before enabling MCP usage.

Risk: The Generect API key could be exposed if broad environment secrets are available to the integration.

Mitigation: Expose only the required GENERECT_API_KEY secret to the process and avoid passing unrelated environment variables.

## Reference(s):

- [Generect Live API Documentation](https://liveapi.generect.com)
- [Generect API Filter Reference](references/api-filters.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GENERECT_API_KEY; responses depend on Generect API availability, account permissions, and rate limits.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
