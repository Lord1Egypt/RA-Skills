## Description:

Reads uptime, response time, outages and recent checks for sites a user monitors with Corrie (uptime and keyword monitoring for small teams, every outage double-checked from a second location), and runs Corrie's free, read-only HTTPS and security header check on any public site. Use when the user asks 'is my site up', 'what was my uptime today', 'when did my site go down', 'is my site secure' or 'check the headers on example.com'. No account is needed for the site check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greg-holman](https://clawhub.ai/user/greg-holman)

### License/Terms of Use:

MIT-0

## Use Case:

Small teams using Corrie can review uptime, response time, outages and certificate expiry for their monitored sites. Anyone can also request a read-only HTTPS, certificate and security-header check for a public website, with suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The URL sent for a website check may contain secret or sensitive query parameters.

Mitigation: Check a public URL without credentials or sensitive query parameters.

Risk: A Corrie API token could be exposed if pasted into chat or logs.

Mitigation: Keep the token in an environment variable and out of chat logs.

Risk: The HTTPS and header check may be mistaken for a full security audit.

Mitigation: Treat it as a narrow check of one public page's headers and certificate, not a security audit or penetration test.

## Reference(s):

- [Corrie API documentation](https://corrie.io/resources/api)
- [Corrie API OpenAPI specification](https://corrie.io/openapi.json)
- [Corrie MCP endpoint](https://corrie.io/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries with status data, findings and suggested fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports account-backed uptime data or read-only public-site HTTPS and header findings.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
