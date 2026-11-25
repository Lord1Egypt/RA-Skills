## Description:

Facebook pages, posts, groups, Marketplace listings, and the Ad Library for agents — no Facebook app, review, or login of yours.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superagnt](https://clawhub.ai/user/superagnt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketing or research teams use this skill to retrieve Facebook page, post, group, Marketplace, video, and advertising data for social listening, content research, and monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: People search and location filters may return personal or location-related information.

Mitigation: Use these searches only for an appropriate, authorized purpose, keep queries focused, and avoid retaining unnecessary personal data.

Risk: The skill sends authenticated requests to an external service using an API key.

Mitigation: Keep SUPERAGNT_API_KEY in a secret store and review the service terms and account permissions before sending queries.

## Reference(s):

- [Facebook Data documentation](https://superagnt.com/r/ch-facebook-data-docs)
- [Facebook Data MCP server](https://mcp.superagnt.com/mcp/facebook)
- [MCP installation guide](https://www.superagnt.com/install?facet=facebook)
- [ClawHub listing](https://clawhub.ai/superagnt/skills/facebook-data)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [Structured JSON responses from Facebook Data endpoints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live external data; response fields and availability vary by endpoint and query.]

## Skill Version(s):

2.0.19 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
