## Description:

One-click AI product launch monitoring pipeline — RSS monitoring, product info search, screenshot capture, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and market analysts use this skill to monitor configured AI product launch feeds, enrich launches with search context, capture landing page screenshots, and produce a trend report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pipeline can browse and screenshot externally supplied links from configured feeds without URL safety checks.

Mitigation: Run the skill in a sandbox or network-controlled environment, and use trusted feeds or an allowlist before enabling automated browsing and screenshot capture.

## Reference(s):

- [Configured AI product monitoring feeds](references/feeds.yaml)
- [OpenAI Blog RSS](https://openai.com/blog/rss.xml)
- [Google AI Blog RSS](https://blog.google/technology/ai/rss/)
- [Anthropic News Feed](https://www.anthropic.com/feed.xml)
- [Meta AI Blog RSS](https://ai.meta.com/blog/rss/)
- [Hugging Face Blog RSS](https://huggingface.co/blog/feed.xml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus generated JSON files, PNG screenshots, and a Markdown trend report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes pipeline outputs under data/: raw_launches.json, enriched_launches.json, screenshots/, and trend_report.md.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
