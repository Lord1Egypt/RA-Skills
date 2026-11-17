## Description:

Fetches AI news from smol.ai RSS. Use when user asks about AI news or daily tech updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjw21century](https://clawhub.ai/user/hjw21century)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve dated AI industry news from the smol.ai RSS feed, inspect available dates, and format results for daily update requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on network access to a fixed public RSS feed, so requests can fail or return no content.

Mitigation: Install dependencies in a virtual environment, keep normal network failure handling enabled, and use date range queries to find available content.

Risk: Fetched RSS content is third-party content and may be unsafe if rendered directly as HTML.

Mitigation: Treat feed content as untrusted and sanitize or escape it before using it in generated HTML.

## Reference(s):

- [Output Format](references/output-format.md)
- [HTML Theme Prompts](references/html-themes.md)
- [smol.ai RSS feed](https://news.smol.ai/rss.xml)
- [smol.ai issue example](https://news.smol.ai/issues/26-01-13-not-much/)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Guidance]

**Output Format:** [JSON from the fetch script, with agent-facing Markdown guidance and formatted news summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses relative dates, absolute YYYY-MM-DD dates, or date range queries; no API keys are required.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
