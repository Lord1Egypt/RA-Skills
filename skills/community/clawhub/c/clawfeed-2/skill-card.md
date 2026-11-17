## Description:

AI-powered tool generating structured news summaries from Twitter and RSS feeds with digest options for 4H, daily, weekly, and monthly intervals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[94w666](https://clawhub.ai/user/94w666)

### License/Terms of Use:


## Use Case:

Developers and operators use Clawfeed to run a news digest service that summarizes Twitter and RSS feeds, exposes digest and configuration APIs, and provides a dashboard for browsing digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation is inconsistent about whether state-changing API endpoints require authentication.

Mitigation: Keep the API bound to localhost or behind trusted access control, and require authentication or an API key for all POST, PUT, DELETE, and configuration endpoints before deploying beyond a private environment.

## Reference(s):

- [Clawfeed ClawHub page](https://clawhub.ai/94w666/skills/clawfeed-2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with setup commands, environment variable tables, API endpoint tables, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents a local API server, optional Google OAuth credentials, API key configuration, SQLite storage, and static dashboard serving.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
