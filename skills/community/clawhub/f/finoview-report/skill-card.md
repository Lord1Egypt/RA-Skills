## Description:

Fetches Finoview futures weekly research reports by date and optional futures category, including report titles, authors, summaries, and PDF links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finoview](https://clawhub.ai/user/finoview)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Finoview futures research reports for market analysis, report summaries, and intelligence gathering by report date or futures category.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation includes examples that print full API credentials, which could expose secrets in logs, screenshots, or chat history.

Mitigation: Use presence-only credential checks, avoid printing secret values, and rotate any credentials that may have been exposed.

Risk: The skill sends configured API credentials to the Finoview report API endpoint.

Mitigation: Install only when Finoview report access is needed and store credentials in environment variables or a managed secret store.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/finoview/skills/finoview-report)
- [Finoview website](https://www.finoview.com.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON report data and Markdown report summaries or tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FINOVIEW_API_KEY and FINOVIEW_API_SECRET environment variables to call the Finoview API.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
