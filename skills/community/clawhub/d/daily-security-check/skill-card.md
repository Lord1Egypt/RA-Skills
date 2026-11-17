## Description:

OpenClaw daily security inspection skill that checks gateway loopback binding, firewall reminders, API key placement, SOUL.md security rules, authentication anomalies, identity and tool controls, then runs read-only OpenClaw audit and doctor commands to produce a concise security report with a 0-10 score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goldwish1](https://clawhub.ai/user/goldwish1)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and agents running OpenClaw use this skill to perform recurring read-only security checks, summarize security-relevant findings, and save a short Markdown report for follow-up. It supports both explicit manual checks and scheduled cron-style runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads OpenClaw configuration and summarizes security-relevant local findings into a saved report.

Mitigation: Keep generated reports private and ensure the report does not include API keys, tokens, passwords, or other secret values.

Risk: Scheduled delivery to Telegram, Feishu, or similar channels can expose security findings to the wrong destination if misconfigured.

Mitigation: Verify notification destinations and access controls before enabling scheduled report delivery.

Risk: Automatic repair commands could change local security or runtime configuration if run outside the documented posture.

Mitigation: Run only read-only checks in this skill and leave any `openclaw doctor --fix` or audit fixes for explicit manual execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goldwish1/skills/daily-security-check)
- [OpenClaw gateway security documentation](https://docs.openclaw.ai/zh-CN/gateway/security)
- [OpenClaw gateway configuration documentation](https://docs.openclaw.ai/zh-CN/gateway/configuration)
- [每日安全巡检 — 检查清单](references/CHECKLIST.md)
- [每日安全巡检报告 — 输出模板](assets/report-template.md)
- [原始参考：OpenClaw 安全配置建议（7 步）](assets/source-article-security-config.md)
- [社区与官方：额外必做 / 推荐安全配置](assets/community-official-security-extras.md)
- [OpenClaw 网关改端口 — 安全说明与操作指南](assets/gateway-port-security.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Structured Markdown security report, saved as a dated Markdown file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report is intended to be 300-600 Chinese characters and include a 0-10 security score, conclusion, and action items.]

## Skill Version(s):

1.0.0 (source: clawhub.json, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
