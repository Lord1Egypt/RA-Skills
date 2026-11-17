## Description:

Technical SEO audit with GEO-specific checks for crawlability, indexability, security, performance, server-side rendering, and AI crawler access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

SEO practitioners, developers, and site owners use this skill to audit a website's crawlability, indexability, mobile readiness, performance, security headers, server-rendered content, and AI crawler access for GEO readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to make shell-based web requests against unvalidated user-supplied URLs.

Mitigation: Use the skill only for controlled or clearly trusted sites, validate URLs before requests, block private/link-local/metadata addresses and unsafe redirects, quote curl arguments safely, and prefer WebFetch where practical.

Risk: The skill writes an audit file after collecting website evidence.

Mitigation: Confirm the intended output path before creating GEO-TECHNICAL-AUDIT.md.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/geo-technical)
- [Publisher profile](https://clawhub.ai/user/asale-ai)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown audit report with tables, findings, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces GEO-TECHNICAL-AUDIT.md for a supplied website URL set.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
