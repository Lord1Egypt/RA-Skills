## Description:

Searches Bing News for current news results and is not intended for general Bing web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a news-search request into a Dataify Bing News API call and return concise, source-linked Bing News results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Dataify API tokens through channels that may expose credentials.

Mitigation: Use session-scoped DATAIFY_API_TOKEN setup, avoid placing tokens in chat or command-line arguments, and rotate any token previously pasted into prompts or stored in shell profiles.

Risk: Security evidence flags insecure setup guidance in the release.

Mitigation: Review credential setup guidance before installation and prefer temporary secret configuration for this workflow.

## Reference(s):

- [Dataify Bing News API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-bing-news)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with source links, optional raw JSON or HTML, and command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include counts or truncation notes; raw JSON or HTML is returned only when explicitly requested.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
