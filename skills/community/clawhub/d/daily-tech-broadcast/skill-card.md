## Description:

Fetches daily technology headlines from configurable public sources such as Sina Tech and IT Home, then prints a short Chinese-language digest without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyaok1](https://clawhub.ai/user/wangyaok1)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to generate a daily technology-news digest for cron delivery or manual agent-triggered broadcasts. It is suited for Chinese-language channel updates where a concise headline list is enough.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runtime performs outbound requests to Sina Tech and IT Home.

Mitigation: Deploy only where outbound web requests to those sources are acceptable, and review the configured NEWS_SOURCES before use.

Risk: Optional publishing documentation includes token-based command examples that may expose credentials in sensitive environments.

Mitigation: Use a pinned, trusted ClawHub CLI and avoid passing tokens directly on the command line.

Risk: Scraped headline output can be incomplete or unavailable if source pages change or network access fails.

Mitigation: Treat the digest as a convenience broadcast, monitor cron output, and rely on the built-in fallback message when source fetching fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyaok1/skills/daily-tech-broadcast)
- [Publisher profile](https://clawhub.ai/user/wangyaok1)
- [Sina Tech](https://tech.sina.com.cn/)
- [IT Home](https://www.ithome.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style Chinese text digest printed to stdout, with setup and cron guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python 3.11 standard library modules, requires no API key, fetches public pages from Sina Tech and IT Home, and emits fallback text if all sources fail.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
