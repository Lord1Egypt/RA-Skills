## Description:

Fetches global AI industry news from RSS sources, filters and deduplicates items, translates English content to Chinese, and generates a daily Markdown news digest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaa2531349](https://clawhub.ai/user/aaa2531349)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to collect recent AI industry news from configured RSS feeds, filter and deduplicate articles, translate English items to Chinese, and prepare a daily digest for review or delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches RSS feeds and article pages from external sources.

Mitigation: Run it in an isolated environment and restrict outbound access to approved news and translation endpoints where possible.

Risk: Article text can be stored locally and sent to third-party translation APIs.

Mitigation: Review data-handling requirements before use, avoid sensitive feeds or articles, and configure approved translation services only.

Risk: Dependency ranges are not pinned to exact versions.

Mitigation: Pin and review dependencies before installation, then install from a trusted package mirror or locked environment.

Risk: The inspected code does not itself prove the advertised automatic OpenClaw scheduling and push behavior.

Mitigation: Treat scheduling and push as platform-dependent and validate the runtime mechanism before relying on automatic delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaa2531349/skills/ai-news-daily)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Markdown digest with source links, plus configurable local text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a configurable number of selected news items; default configuration writes the digest to data/openclaw_message.txt.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact files identify 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
