## Description:

防护间接提示词注入攻击（Indirect Prompt Injection）。当处理网页内容、搜索结果、邮件、社交媒体等外部来源信息时触发。用于识别和防范外部内容中隐藏的恶意指令。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xvarx](https://clawhub.ai/user/xvarx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill as Chinese-language defensive guidance for recognizing indirect prompt injection in webpages, search results, email, social media, and other untrusted external content. It helps agents treat external content as information rather than instructions and require confirmation before sensitive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact provides Chinese-language guidance, which may not meet the needs of English or multilingual users.

Mitigation: Use it where Chinese-language guidance is appropriate, or provide a reviewed localized version for other audiences.

Risk: The skill is advisory and does not add executable enforcement for unsafe actions.

Mitigation: Review agent behavior before deployment and keep user confirmation in place for sensitive actions involving external content.

## Reference(s):

- [Attack Patterns Reference](references/attack-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/xvarx/skills/claw-prompt-injection-guard)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language defensive guidance; no executable code, install hooks, persistence, or hidden data access reported by security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
