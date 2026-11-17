## Description:

Daily Game News collects and categorizes daily game news from multiple gaming media sites, then generates report messages and archived documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[czwfelix](https://clawhub.ai/user/czwfelix)

### License/Terms of Use:


## Use Case:

Game industry readers, analysts, and operators use this skill to collect daily news from configured gaming media sources and receive categorized reports. It supports scheduled daily runs and manual report retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install persistent scheduled execution through cron.

Mitigation: Preserve the existing crontab before installation and review or disable the scheduled job unless daily execution is intended.

Risk: The crawler fetches web pages from configured URLs and may be too broadly scoped.

Mitigation: Restrict configuration to trusted public game-news domains and avoid sensitive, internal, or private URLs.

Risk: Some fetching behavior may use the r.jina.ai proxy.

Mitigation: Disable proxy use or explicitly approve it before running the crawler.

Risk: Security evidence calls out TLS verification and dependency pinning issues.

Mitigation: Enable TLS verification where disabled and pin runtime dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/czwfelix/skills/daily-game-news)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown report text, Feishu message text, Word (.docx) files, and plain text archive files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports group articles by category and include source, time, title, link, and optional summary fields.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
