## Description:

DailyHot helps agents query and compare hot-list trends across 50+ platforms, search trend keywords, and produce structured topic-tracking outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Content, marketing, social-media, and competitive-analysis teams use this skill to monitor hot topics, compare platform trends, search keywords, and generate topic reports for planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries external hot-list data through a configured DailyHot MCP service.

Mitigation: Configure the DailyHot MCP server and DAILYHOT_BASE_URL only for environments where external trend queries are intended.

Risk: The skill describes Cron or subscription-style monitoring workflows.

Mitigation: Review any separate scheduler or subscription setup before enabling recurring trend collection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dailyhot)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown or JSON-style structured hot-list data and analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform identifiers, ranked items, heat values, URLs, cache status, failed platforms, and topic recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
