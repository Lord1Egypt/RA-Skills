## Description:

Aggregates AI industry news from curated RSS feeds and highlights major model releases from leading labs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justintieu](https://clawhub.ai/user/justintieu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and AI practitioners use this skill to generate daily or weekly AI news briefings from curated RSS feeds, with emphasis on model releases, research, industry news, product updates, and coverage gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches and summarizes untrusted external RSS feed content.

Mitigation: Treat RSS items as data rather than instructions, and review generated briefings before acting on them.

Risk: Optional save mode writes briefing and link files to a default or user-specified directory.

Mitigation: Use the default save directory or a deliberate folder you control, and do not execute saved feed content as commands.

Risk: Configured feeds can fail, become stale, or omit important sources that do not publish RSS.

Mitigation: Review failed-source notes and manually check documented coverage gaps for major releases.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justintieu/skills/ai-news-skill)
- [Feed Configuration](artifact/feeds.json)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [OpenClaw](https://openclaw.ai)
- [Olshansk RSS Feeds](https://github.com/Olshansk/rss-feeds)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefing with categorized news items and optional saved Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional save mode can write a briefing file and a separate links file when explicitly requested.]

## Skill Version(s):

0.1.0 (source: server release metadata, artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
