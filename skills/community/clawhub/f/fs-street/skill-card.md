## Description:

Fetches articles from Farnam Street RSS. Use when asking about decision-making, mental models, learning, or wisdom from Farnam Street blog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjw21century](https://clawhub.ai/user/hjw21century)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve Farnam Street RSS articles by relative date, absolute date, date range, or topic keyword, then present the results for decision-making, mental-model, learning, and leadership queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script fetches article content from an external RSS feed.

Mitigation: Treat fetched RSS article content as external website content before relying on or redistributing it.

Risk: Runtime dependencies are installed separately and may change over time.

Mitigation: Install dependencies in an isolated environment and consider pinning versions before use.

Risk: Premium member-only articles may return only teaser content.

Mitigation: Surface member-only or unavailable-content states clearly instead of presenting partial RSS content as complete.

## Reference(s):

- [Output Format Reference](references/output-format.md)
- [Farnam Street RSS Feed](https://fs.blog/feed/)
- [ClawHub Skill Page](https://clawhub.ai/hjw21century/skills/fs-street)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown article summaries and JSON from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [RSS article lookups may return premium-member teasers or no result when the requested date is unavailable.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
