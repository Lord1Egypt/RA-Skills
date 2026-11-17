## Description:

Provides read-only analytics for a site's first-party traffic and AI-engine visibility, including visitor/session metrics, engine answer sampling, cited pages, source attribution, conversions, realtime activity, and data-quality views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gt-oliver](https://clawhub.ai/user/gt-oliver)

### License/Terms of Use:

MIT-0

## Use Case:

External site owners, marketers, analysts, and developers use this skill to query authorized Vtag GEO Analytics data, explain first-party traffic and AI-engine visibility metrics, and avoid unsupported attribution claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private site analytics and a long-lived bearer token.

Mitigation: Install only when authorized, keep the credential path private, treat the token as a secret, and revoke it in the service console if exposure is suspected.

Risk: Raw visitor, session, realtime, or conversion data may reveal sensitive business activity.

Mitigation: Share analytics only with users authorized to view the selected site and avoid exporting raw data unless necessary.

Risk: AI-engine visibility samples and site traffic can be misread as direct causation.

Mitigation: Report engine-side and site-side metrics separately, preserve source-unknown buckets, and avoid converting citations or mentions into inferred visitors or conversions.

## Reference(s):

- [Endpoint Reference](artifact/references/endpoints.md)
- [Metrics Formulas and Boundaries](artifact/references/metrics.md)
- [ClawHub Skill Page](https://clawhub.ai/gt-oliver/skills/geo-analytics)
- [Geo Analytics Service](https://geo-analytics.info)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional shell command snippets and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only outputs depend on the authorized site, selected report endpoint, and date range.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
