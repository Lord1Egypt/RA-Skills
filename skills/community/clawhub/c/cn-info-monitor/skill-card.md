## Description: <br>
自动监控微信公众号、行业网站和 RSS 信息源，使用 AI 提炼摘要后推送到飞书、钉钉或终端。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwfqls3w-cmd](https://clawhub.ai/user/wwfqls3w-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to monitor selected Chinese information sources, filter new articles by keywords, summarize updates, and deliver daily digests to terminal, Markdown files, or Feishu webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitored source content may be sent to external LLM services or Feishu webhook destinations. <br>
Mitigation: Review monitored sources for private or proprietary content, verify the LLM base URL and webhook destination, and avoid webhook delivery for sensitive digests. <br>
Risk: LLM API keys and configuration may be stored locally during setup. <br>
Mitigation: Prefer environment variables for API keys, restrict file permissions for local configuration, and rotate keys if they were saved in plaintext. <br>
Risk: Local state and digest files can retain source URLs, summaries, and monitored content over time. <br>
Mitigation: Periodically clean ~/.cn-info-monitor and ~/info-digest, and avoid monitoring sources whose retained summaries would violate internal data-handling rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwfqls3w-cmd/cn-info-monitor) <br>
- [Skill homepage](https://clawhub.ai/skills/cn-info-monitor) <br>
- [Sources template](config/sources_template.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Terminal text, Markdown digests, and JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; optional integrations use requests, feedparser, LLM_API_KEY, LLM_API_BASE_URL, LLM_MODEL, FEISHU_WEBHOOK_URL, and INFO_MONITOR_PROXY. The skill stores local state under ~/.cn-info-monitor and digest files under ~/info-digest.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
