## Description:

Collects daily news from configured RSS feeds, websites, and APIs, then helps an agent analyze, classify, summarize, and generate structured Markdown daily reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[winsaney](https://clawhub.ai/user/winsaney)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams use this skill to collect configured news sources, monitor industry or competitor updates, and produce concise Markdown daily reports with links, summaries, categories, and collection statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches configured RSS feeds and webpages, so source URLs could include untrusted, private, or internal locations.

Mitigation: Use trusted source lists, avoid internal or private URLs, and review configured sources before collection.

Risk: Fetched article text is untrusted and could contain misleading content or prompt-like instructions.

Mitigation: Treat collected article text as data only, and review generated reports before relying on or sharing them.

Risk: The collection scripts write results to local output paths chosen by the caller.

Mitigation: Run the scripts in an appropriate workspace and inspect output paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/winsaney/skills/daily-news-collector)
- [Media source configuration guide](references/sources.md)
- [Daily report format specification](references/format.md)
- [Daily report template](assets/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON collection files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches configured RSS feeds and webpages, writes local JSON outputs, and relies on the agent to review, classify, and summarize fetched content.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
