## Description:

Audits Hacker News activity or RSS subscriptions, classifies reading items, and generates reports with category breakdowns and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tkuehnl](https://clawhub.ai/user/tkuehnl)

### License/Terms of Use:

MIT

## Use Case:

Developers and individual readers use this skill to analyze Hacker News or OPML/RSS reading patterns, classify content, and generate Markdown audit or digest reports with recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch URLs from OPML feed files, including private or internal feed URLs supplied by a user.

Mitigation: Use only trusted OPML files and avoid internal or private feed URLs unless they are intended to be fetched.

Risk: Reading item titles and URLs may be sent to an LLM provider when an LLM tool or API key is available.

Mitigation: Use local keyword classification or unset LLM API keys when analyzing sensitive subscriptions or work-related links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tkuehnl/skills/feed-diet)
- [Publisher profile](https://clawhub.ai/user/tkuehnl)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown reports with category tables, ASCII charts, recommendations, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write reports to stdout or a file; classification may use an LLM provider when configured or keyword fallback otherwise.]

## Skill Version(s):

0.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
