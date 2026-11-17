## Description:

Tracks time-sensitive topics, monitors public URL updates, aggregates third-party news hotspots, and produces Markdown briefs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[changsheng0804](https://clawhub.ai/user/changsheng0804)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content or research teams use this skill to track industry news, monitor public web pages for changes, and generate recurring Markdown briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches public web/news content and creates local Markdown briefs.

Mitigation: Confirm this behavior is acceptable before installing and review generated briefs against the original sources.

Risk: The artifact declares a topic_tracking dependency but does not include that dependency's implementation.

Mitigation: Review and scan the topic_tracking dependency separately before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown briefs with source links, summaries, and timeliness notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes briefs under ./我的追踪/{yyyy_mm_dd}/{话题名称}.md when tracking produces results.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
