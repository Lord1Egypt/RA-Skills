## Description:

Analyzes a competitor's TikTok content strategy and top-performing videos using apidojo's scrapers on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Social media strategists, content teams, and competitive intelligence analysts use this skill to inspect competitor TikTok accounts, identify top-performing videos, compare posting cadence, and summarize hooks, hashtags, content mix, and engagement patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify credentials could be exposed if tokens are placed in URLs, logs, shell history, or saved transcripts.

Mitigation: Use authorization headers, the Apify MCP server, or a helper that reads APIFY_TOKEN from the environment; avoid pasting expanded tokens into commands or logs.

Risk: TikTok targets and scraped results are sent to Apify actors for processing.

Mitigation: Install and use the skill only when sending the selected TikTok handles and related analysis inputs to Apify is acceptable.

Risk: The optional customMapFunction runs JavaScript in the actor workflow.

Mitigation: Avoid customMapFunction unless the user understands where the code runs and has reviewed the function for data handling and side effects.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/apidojo-io/apidojo-skills/tree/main/skills/intent/analyzing-competitor-tiktok-content-strategy)
- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/analyzing-competitor-tiktok-content-strategy)
- [Apify TikTok scraper actor](https://apify.com/apidojo/tiktok-scraper)
- [Apify TikTok profile scraper actor](https://apify.com/apidojo/tiktok-profile-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with tables, structured findings, and optional shell or API call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include TikTok account overview metrics, top video tables, posting frequency, content mix, hashtag analysis, hook patterns, strategic insights, and differentiation opportunities.]

## Skill Version(s):

0.1.0 (source: evidence.release.version; artifact metadata.version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
