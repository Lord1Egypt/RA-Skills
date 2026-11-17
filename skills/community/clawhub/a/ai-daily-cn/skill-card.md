## Description:

AI 日报 - 自动抓取 LLM/Agent 领域热点信息，生成结构化中文简报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanhe](https://clawhub.ai/user/yanhe)

### License/Terms of Use:

MIT

## Use Case:

Developers, AI practitioners, and operations teams use this skill to generate Chinese daily briefings on LLM, agent, AI-industry, KOL, and arXiv developments from configured external sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External feed and API requests include unsafe networking behavior, including disabled TLS verification.

Mitigation: Restore certificate and hostname verification before using authenticated APIs or running on untrusted networks.

Risk: The DingTalk push helper can send report content to a hard-coded group destination.

Mitigation: Do not use the push helper until the destination is configurable and explicitly verified.

Risk: Installation guidance includes root-level systemd setup for scheduled execution.

Mitigation: Prefer manual execution, user-level cron, or other least-privilege scheduling.

Risk: Setup guidance stores API keys in shell startup files and suggests a curl-to-bash pyenv install path.

Mitigation: Use a scoped secret store or runtime environment variables, and install Python through a trusted package manager or reviewed script.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yanhe/skills/ai-daily-cn)
- [Publisher Profile](https://clawhub.ai/user/yanhe)
- [OpenClaw Project Homepage](https://github.com/openclaw/openclaw)
- [Tavily API Console](https://app.tavily.com)
- [Alibaba Cloud DashScope Console](https://dashscope.console.aliyun.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report files with terminal preview output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates dated reports under output/AI-Daily-YYYY-MM-DD.md; content depends on external sources and optional API keys.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact frontmatter and changelog list earlier versions)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
