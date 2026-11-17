## Description:

AIBase-News-Get scrapes recent AI news from AIBase and stores structured article data for collection, aggregation, monitoring, and downstream summary preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiahuishao](https://clawhub.ai/user/jiahuishao)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to collect recent AIBase news, deduplicate article URLs, and save titles, links, publish times, source names, and extracted article content for news briefs or monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted page links can drive outbound HTTP requests to arbitrary URLs.

Mitigation: Run the skill with outbound HTTP restricted to expected AIBase domains and review collected URLs before processing them further.

Risk: Scraped titles and article bodies are untrusted text that may contain instructions for a downstream agent.

Mitigation: Treat scraped content as data only and do not allow summarizing or analysis agents to follow instructions found inside articles.

Risk: The skill writes output files under a News directory in the current working directory.

Mitigation: Run it in a workspace where that write behavior is acceptable and inspect generated files before reuse.

Risk: The documentation overstates automatic summarization behavior.

Mitigation: Use the generated JSON as source data and rely on a reviewed downstream summarization step when summaries are required.

## Reference(s):

- [ClawHub skill release: AIBase-News-Get](https://clawhub.ai/jiahuishao/skills/aibase-news-get)
- [AIBase news source](https://www.aibase.com/zh/news)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON files]

**Output Format:** [Markdown guidance with shell and Python snippets; runtime output is JSON news records and console text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes news_latest.json under a News directory in the selected workspace; article titles and bodies are untrusted scraped text.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
