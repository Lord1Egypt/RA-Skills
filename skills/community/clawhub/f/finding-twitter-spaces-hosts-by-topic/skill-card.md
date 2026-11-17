## Description:

Finds Twitter Spaces hosts in a selected topic area using apidojo Twitter scrapers and returns host handles, topic focus, frequency signals, co-host networks, and audience size indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as thought leaders, PR professionals, and community builders use this skill to discover active Twitter Spaces hosts in a topic area and prepare outreach or collaboration lists. Agents use it to run the apidojo tweet scraper, classify host activity, score relevance, and summarize likely hosts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify tokens can be exposed when REST examples place tokens in query strings.

Mitigation: Use header-based authentication or the MCP/helper path when it protects secrets, keep tokens narrowly scoped, and rotate any token already used in query-string commands.

Risk: Broad scraping controls may collect sensitive or unnecessary Twitter/X data.

Mitigation: Use the skill only for non-sensitive Twitter/X research and review configured filters before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-twitter-spaces-hosts-by-topic)
- [Publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify actor: apidojo/tweet-scraper](https://apify.com/apidojo/tweet-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown report with a results table and summary, with optional CSV or JSON files when saved through the actor helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include host classifications, relevance scores, frequency signals, co-host networks, and audience size indicators.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
