## Description:

Monitor competitor websites for pricing changes, new content, and keyword movements across multiple domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and growth teams use this skill to monitor public competitor pricing pages, content updates, landing pages, and search ranking changes, then produce alerts and competitive intelligence reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated monitoring may target sites where scanning is blocked or not authorized.

Mitigation: Use the skill only for authorized monitoring of public pages, prefer official APIs or permissioned feeds, and stop or reduce scanning when a site returns 403 or 429.

Risk: Monitoring targets and results may be sent to external services such as Slack, Google Sheets, SerpAPI, Browserless, or automation platforms.

Mitigation: Review configured integrations before use and avoid sending sensitive, confidential, or unauthorized data to third-party recipients.

Risk: The artifact suggests rotating User-Agent headers and residential proxies when sites block automated requests.

Mitigation: Do not use proxy or identity rotation to bypass access controls; reduce scan frequency, use permissioned feeds, or obtain authorization instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/competitor-spy-tool)
- [SerpAPI](https://serpapi.com)
- [Slack app configuration](https://api.slack.com/apps)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, alert examples, and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference environment variables for competitor domains, SerpAPI, Slack, Google Sheets, Browserless, and email alerts.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
