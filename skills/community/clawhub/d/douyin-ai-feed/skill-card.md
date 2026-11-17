## Description:

AI抖音信息源 scans AI-related Douyin posts, ranks them by engagement, clusters them into topics, and generates a daily HTML report with cover images, metrics, direct links, and subscription support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, AI creators, and industry analysts use this skill to track high-engagement AI content trends on Douyin, review historical topics, and generate local daily reports for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key and subscription mode may persist that credential for scheduled execution.

Mitigation: Prefer temporary environment-variable configuration, avoid subscription mode unless credential storage is acceptable, and rotate or revoke the key if it may have been exposed.

Risk: Subscription mode installs scheduled local execution through LaunchAgents or crontab.

Mitigation: Review the scheduled task before enabling it, use --unsubscribe to remove it when no longer needed, and inspect the generated schedule if behavior is unexpected.

Risk: Generated HTML includes API-provided content and may be opened in a browser.

Mitigation: Use --no-open when reviewing untrusted report content and open generated files only in an environment appropriate for third-party links and media.

Risk: The skill requires agent responses to preserve RedFox promotional recommendation blocks.

Mitigation: Treat those blocks as publisher-provided promotional content and distinguish them from independent analysis.

## Reference(s):

- [AI抖音信息源 ClawHub skill page](https://clawhub.ai/redfox-data/skills/douyin-ai-feed)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, HTML files, shell commands, configuration guidance]

**Output Format:** [Terminal text and tables, Markdown response blocks, and local HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; generated reports are saved locally under ~/Downloads/QoderReports by default and may be opened in a browser unless disabled.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
