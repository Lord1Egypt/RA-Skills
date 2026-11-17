## Description:

Searches public Douyin videos by keyword and returns video details and engagement metrics, with optional CSV export for content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuiyunhai](https://clawhub.ai/user/cuiyunhai)

### License/Terms of Use:

MIT-0

## Use Case:

Content researchers and marketers use this skill to gather public Douyin search results for topic research, competitor monitoring, and initial creator screening. Users confirm the estimated credit charge before a collection task is submitted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default HTTP service address can expose authentication tokens in transit.

Mitigation: Configure a working HTTPS service URL before logging in; do not send credentials over the default HTTP connection.

Risk: Disabling TLS certificate checks can expose credentials to interception.

Mitigation: Keep insecure TLS disabled and use a service endpoint with a valid certificate.

Risk: A shared user-level configuration file stores authentication tokens.

Mitigation: Review the existing configuration before use and protect it from disclosure or version-control commits.

Risk: Submitting a collection task can deduct paid credits; the CLI does not enforce user approval.

Mitigation: Show the requested quantity and estimated credits, then obtain explicit user approval before every submission.

## Reference(s):

- [ClawHub dy-search release](https://clawhub.ai/cuiyunhai/skills/dy-search)

## Skill Output:

**Output Type(s):** [Text, Files, Guidance]

**Output Format:** [JSON task results and UTF-8 CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One keyword per task, up to 500 requested videos; results include video metadata, engagement counts, and credit settlement details.]

## Skill Version(s):

1.0.0 (source: release metadata, skill frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
