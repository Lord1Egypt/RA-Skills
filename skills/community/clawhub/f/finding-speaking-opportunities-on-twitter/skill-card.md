## Description:

Finds speaking opportunities and event organizer contacts on Twitter using apidojo's Twitter scrapers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as startup founders, executives, coaches, and consultants use this skill to find Twitter/X posts about speaking, podcast guest, summit, panel, and workshop opportunities. The skill helps build a speaking opportunity pipeline by returning organizer handles, topic focus, deadline signals, event size, submission links, classifications, and relevance scores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback REST API commands place the Apify token in request URLs, which can expose the credential in logs or process output.

Mitigation: Prefer the MCP path or a helper that keeps the token in protected environment handling, use a narrowly scoped Apify token, and avoid logging commands that contain credentials.

Risk: Saved JSON or CSV outputs can persist scraped tweet data locally.

Mitigation: Store result files only where needed, limit sharing, and remove locally persisted scraped data when it is no longer required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/apidojo-io/skills/finding-speaking-opportunities-on-twitter)
- [API Dojo Publisher Profile](https://clawhub.ai/user/apidojo-io)
- [Apify Actor: apidojo/tweet-scraper](https://apify.com/apidojo/tweet-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables and summaries with optional shell commands, JSON, or CSV result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include locally saved scraped tweet data when the user requests JSON or CSV output.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
