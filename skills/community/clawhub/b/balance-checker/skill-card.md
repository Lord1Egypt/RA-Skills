## Description:

Checks AI API account balances for DeepSeek, Moonshot/Kimi, and Volcengine when an agent is asked balance-related questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyya](https://clawhub.ai/user/kyya)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to check configured AI API account balances for DeepSeek, Moonshot/Kimi, and Volcengine from an agent conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically use local API credentials and send authenticated balance requests to configured providers.

Mitigation: Configure only the providers you intend to query, prefer least-privilege credentials where available, and expect returned balances to appear in the current chat.

Risk: Installation guidance includes mutable, unpinned external code paths.

Mitigation: Prefer the reviewed ClawHub install path and review the installed files before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyya/skills/balance-checker)
- [DeepSeek user balance API](https://api-docs.deepseek.com/zh-cn/api/get-user-balance)
- [Moonshot user balance API](https://platform.moonshot.cn/docs/api-reference#user-balance)
- [Volcengine balance documentation](https://www.volcengine.com/docs/6269/1593138)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Terminal text with provider balance lines and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print account balances into the current chat and skips providers whose credentials are not configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
