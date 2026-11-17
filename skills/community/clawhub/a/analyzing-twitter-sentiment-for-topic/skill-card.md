## Description:

Analyzes public sentiment on Twitter/X for any topic, brand, or event using apidojo's Tweet scrapers on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users, PR teams, market researchers, political analysts, and social listening teams use this skill to collect public Twitter/X posts for a topic and summarize sentiment, themes, engagement-weighted signals, and volume changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The REST fallback places APIFY_TOKEN in a request URL, which can expose the token through command history, logs, or network tooling.

Mitigation: Prefer Apify MCP or a request method that sends APIFY_TOKEN in an Authorization header; keep the token out of command histories and logs.

Risk: Saved CSV or JSON outputs may persist collected tweet data locally.

Mitigation: Store exported tweet data only where appropriate for the use case and remove local files when they are no longer needed.

Risk: Lexical sentiment classification can miss sarcasm, ambiguity, and context.

Mitigation: Manually review the most engaged and top positive or negative tweets before using results for high-stakes decisions.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/apidojo-io/skills/analyzing-twitter-sentiment-for-topic)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown sentiment report with optional shell commands and JSON or CSV data collection outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes sentiment percentages, top positive and negative tweet examples, recurring themes, engagement-weighted statistics, and volume trends.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
