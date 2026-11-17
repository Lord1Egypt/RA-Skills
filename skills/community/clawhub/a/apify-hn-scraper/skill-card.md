## Description:

Scrape Hacker News stories, comments, and discussions using an Apify Actor via the REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcindudekdev](https://clawhub.ai/user/marcindudekdev)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to search Hacker News, scrape stories and comment threads, monitor technical discussions, and summarize trends or export the resulting data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hacker News search parameters are sent to Apify.

Mitigation: Avoid sensitive search terms unless sharing them with Apify is acceptable.

Risk: The Apify token is used from the agent environment and may appear in command logs if commands are copied or echoed.

Mitigation: Use a narrowly scoped token and prefer Authorization headers over token query parameters before use on shared systems.

Risk: Manually interpolated search terms in shell commands can break JSON payloads or alter request behavior.

Mitigation: Build request JSON with jq or another JSON encoder when accepting arbitrary user input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marcindudekdev/skills/apify-hn-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with inline shell commands and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can summarize top stories by points, comment counts, domains, and trends; may offer JSON or CSV export.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
