## Description:

AIMPACT retrieves AI morning and evening reports, 24-hour hot-news rankings, and curated AI content from configured ME News APIs, ranks items by AI score, and can optionally send reports through an existing OpenClaw message channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamesmenews](https://clawhub.ai/user/jamesmenews)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch and format Chinese AI news briefings, hot-news rankings, and curated AI content from ME News sources. Teams can also configure recurring local scheduling when they want routine delivery through their existing OpenClaw message setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring scheduled runs may repeatedly post AI news reports through an already configured OpenClaw message channel.

Mitigation: Configure cron or Windows scheduled tasks only when recurring delivery is intended, and review the selected message channel and OpenClaw permissions before enabling scheduled runs.

Risk: The skill retrieves external ME News API content and turns it into AI news reports.

Mitigation: Review generated reports and their source links before relying on or redistributing the information.

## Reference(s):

- [AIMPACT ClawHub Skill Page](https://clawhub.ai/jamesmenews/skills/aimpact)
- [Publisher Profile](https://clawhub.ai/user/jamesmenews)
- [ME News Sources Configuration](artifact/sources.md)
- [Output Format Template](artifact/format.md)
- [MetaEra AI Flash API](https://agent.me.news/skill/flash/list?page=1&size=20&category=ai)
- [AIMPACT AI News API](https://agent.me.news/skill/aimpact/articles?page=1&size=20&category=ai)
- [AIMPACT OpenClaw News API](https://agent.me.news/skill/aimpact/articles?page=1&size=20&category=openclaw)
- [AIMPACT Events API](https://agent.me.news/skill/aimpact/events)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown news report with source links, plus optional shell command examples for scheduling.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for ME News API retrieval; can optionally use web_fetch as a fallback and message for delivery when configured.]

## Skill Version(s):

0.8.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
