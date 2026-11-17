## Description:

Daily Ai Brief Skill collects AI news from RSS feeds, social sources, web pages, and APIs, then writes structured Markdown and JSON briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanll](https://clawhub.ai/user/yanll)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate daily AI industry briefings from configured feeds, social sources, web pages, and APIs for quick news review and downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts many third-party sites and processes untrusted web content.

Mitigation: Run it as an unprivileged user or in a container, and review generated reports before sharing or opening them in permissive Markdown renderers.

Risk: The browser-based social-source fetcher disables Chromium sandbox protections.

Mitigation: Prefer a version that removes no-sandbox Chromium flags, or run browser scraping only inside an isolated environment.

Risk: Dependency ranges are not pinned to exact versions.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yanll/skills/daily-ai-brief-skill)
- [Publisher Profile](https://clawhub.ai/user/yanll)
- [README](artifact/README.md)
- [Data Source Configuration](artifact/src/data_sources.yaml)
- [Hacker News API Source](https://hacker-news.firebaseio.com/v0/topstories.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, shell commands, guidance]

**Output Format:** [Markdown report files and JSON data files saved under reports/]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Timestamped reports include source, publication time, original link, and summary fields when available.]

## Skill Version(s):

0.2.0 (source: ClawHub release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
