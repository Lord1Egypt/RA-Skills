## Description:

自动监控微信公众号/行业网站/RSS信息源，AI提炼摘要后推送到飞书/钉钉/终端。解决'每天手动翻10个公众号找有用信息'的痛点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwfqls3w-cmd](https://clawhub.ai/user/wwfqls3w-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor Chinese-focused RSS feeds, webpages, and WeChat article links, filter updates by keywords, summarize new items, and send digests to terminal, Markdown files, or Feishu webhook channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured sources can make the skill fetch arbitrary URLs.

Mitigation: Use only trusted external sources; do not configure internal, localhost, cloud metadata, or other sensitive network URLs.

Risk: Collected article content or summaries may be sent to an LLM provider or Feishu webhook.

Mitigation: Review the configured LLM base URL, model, and webhook destination before enabling external integrations.

Risk: The setup flow can place an LLM API key in local plaintext configuration.

Mitigation: Prefer environment variables or a secret store, and avoid entering the key into the setup wizard until plaintext storage is fixed.

## Reference(s):

- [ClawHub skill homepage](https://clawhub.ai/skills/cn-info-monitor)
- [ClawHub release page](https://clawhub.ai/wwfqls3w-cmd/skills/cn-info-monitor)
- [Publisher profile](https://clawhub.ai/user/wwfqls3w-cmd)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text, Markdown digests, JSON configuration, and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local digest Markdown files and local monitoring state; optional integrations can send summaries to an LLM provider and Feishu webhook.]

## Skill Version(s):

1.0.0 (source: frontmatter, clawhub.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
