## Description: <br>
Checks AI API provider balances for DeepSeek, Moonshot/Kimi, and Volcengine when users ask balance-related questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyya](https://clawhub.ai/user/kyya) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to check and summarize configured AI provider account balances from an agent conversation. It supports DeepSeek, Moonshot/Kimi, and Volcengine accounts using locally configured API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses configured provider API keys to read billing balance information. <br>
Mitigation: Configure only providers you use and prefer billing-read-only or least-privilege keys where available. <br>
Risk: The optional Volcengine setup installs an unpinned Python SDK dependency. <br>
Mitigation: Review the setup script and dependency before running it in managed or production environments. <br>


## Reference(s): <br>
- [Balance Checker on ClawHub](https://clawhub.ai/kyya/balance-checker) <br>
- [DeepSeek User Balance API](https://api-docs.deepseek.com/zh-cn/api/get-user-balance) <br>
- [Moonshot User Balance API](https://platform.moonshot.cn/docs/api-reference#user-balance) <br>
- [Volcengine Billing Balance Documentation](https://www.volcengine.com/docs/6269/1593138) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text balance summary with setup and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured local provider credentials; skips providers whose credentials are not configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
