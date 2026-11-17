## Description:

Google search results and web page scraping via Bright Data APIs. Use when the agent needs structured search results, paginated SERP retrieval, or clean markdown from any URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhao-weijie](https://clawhub.ai/user/zhao-weijie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover Google search results through Bright Data SERP APIs and scrape public web pages into clean markdown for downstream research or extraction tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted search cursor could trigger unsafe shell behavior.

Mitigation: Use only trusted agent inputs and prefer a version that validates the cursor as a non-negative integer before invoking the search script.

Risk: Queries or scraped URLs may expose sensitive or restricted information to Bright Data services.

Mitigation: Avoid sensitive queries, private URLs, and restricted resources unless the deployment has explicitly approved that data flow.

Risk: Hand-built JSON request bodies can fail or behave unexpectedly with unusual input.

Mitigation: Prefer a version that builds outbound JSON with a real serializer before sending requests to Bright Data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhao-weijie/skills/brightdata)
- [Related ClawHub Bright Data Skill](https://clawhub.ai/meirkad/bright-data)
- [Bright Data API Request Endpoint](https://api.brightdata.com/request)
- [Publisher Profile](https://clawhub.ai/user/zhao-weijie)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command usage and JSON or markdown tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Bright Data API credentials and configured SERP and Web Unlocker zones.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
