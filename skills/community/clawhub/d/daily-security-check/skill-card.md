## Description: <br>
每日安全巡检 is an OpenClaw skill that runs a read-only daily security checklist, executes OpenClaw audit and doctor commands, and produces a concise security score report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goldwish1](https://clawhub.ai/user/goldwish1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and agents use this skill to perform scheduled or manually requested security checks across gateway binding, firewall reminders, credential placement, SOUL.md safety rules, access control, tool sandboxing, audit output, and doctor output. It is intended to produce a short Simplified Chinese report without changing configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated security report may reveal where sensitive configuration weaknesses exist, even when secret values are redacted. <br>
Mitigation: Keep reports private and forward them only to trusted Telegram, Feishu, or similar channels. <br>
Risk: The skill inspects OpenClaw configuration, logs, and security state. <br>
Mitigation: Install and run it only in workspaces where the agent is authorized to inspect security configuration and operational logs. <br>
Risk: Audit or doctor output may mention credential fields or file locations. <br>
Mitigation: Report only paths, field names, summaries, and recommended actions; do not include API keys, tokens, passwords, or other secret values. <br>


## Reference(s): <br>
- [Daily Security Checklist](references/CHECKLIST.md) <br>
- [Daily Security Report Template](assets/report-template.md) <br>
- [Source Security Configuration Notes](assets/source-article-security-config.md) <br>
- [Community and Official Security Extras](assets/community-official-security-extras.md) <br>
- [Gateway Port Security Notes](assets/gateway-port-security.md) <br>
- [OpenClaw Gateway Security Documentation](https://docs.openclaw.ai/zh-CN/gateway/security) <br>
- [OpenClaw Gateway Configuration Documentation](https://docs.openclaw.ai/zh-CN/gateway/configuration) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Simplified Chinese Markdown report saved as a local Markdown file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [300-600 words; includes a 0-10 security score, conclusion, and todo list; secret values are redacted.] <br>

## Skill Version(s): <br>
1.0.0 (source: clawhub.json and CHANGELOG.md, released 2026-03-08) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
