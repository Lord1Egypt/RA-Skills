## Description:

Helps agents scrape, crawl, map, and search web content through a user-authorized Firecrawl connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to extract website content, discover site URLs, and research the web using a connected Firecrawl account. It also describes optional user-approved automation of these workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected URLs, prompts, and scraped results may be sent through Firecrawl and Maton, including non-public content.

Mitigation: Confirm the intended targets and avoid sending sensitive content unless the user approves the disclosure.

Risk: Large crawls and browser sessions can consume credits or interact with websites beyond passive reading.

Mitigation: Confirm crawl limits and browser actions with the user before execution.

Risk: Hosted functions and triggers may persistently forward data to a destination.

Mitigation: Review the connection, trigger scope, and destination before approval; remove unused automation and connections.

## Reference(s):

- [Firecrawl skill release](https://clawhub.ai/byungkyu/skills/firecrawl-api)
- [Firecrawl API documentation](https://docs.firecrawl.dev/api-reference/v2-introduction)
- [Maton homepage](https://maton.ai)
- [Maton API documentation](https://docs.maton.ai/api-reference/overview)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Schedule trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown with command examples and structured web results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected URLs and authorized Firecrawl connection.]

## Skill Version(s):

1.2.8 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
