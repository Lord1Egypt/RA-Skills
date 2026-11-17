## Description:

Axelrod lets OpenClaw agents query Base-chain data and submit spot trades or automated trading strategy requests through AIxVC AI Automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aixvcteam](https://clawhub.ai/user/aixvcteam)

### License/Terms of Use:


## Use Case:

External users and developers use Axelrod to let OpenClaw agents check balances, prices, token information, and orders, and to request Base-chain spot trades or automated strategies through AIxVC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move funds through a third-party trading API.

Mitigation: Use a dedicated low-balance trading account and require manual confirmation for every trade, including small orders.

Risk: Prompts and account-related requests are sent to AIxVC for real-time trading and query execution.

Mitigation: Avoid sending unrelated sensitive information and review each request before invoking the API.

Risk: Weak command-invocation boundaries could expose user text to unsafe shell interpolation.

Mitigation: Invoke scripts/axelrod_chat.py with structured arguments rather than interpolating user text into a shell command.

## Reference(s):

- [Axelrod API Reference](references/api.md)
- [Axelrod ClawHub Listing](https://clawhub.ai/aixvcteam/skills/axelrod)
- [AIxVC AI Automation](https://aixvc.io/chat)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or Markdown returned from a Python CLI, with optional JSON debug output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confirmation keys, balances, prices, order status, transaction details, and API error messages.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
