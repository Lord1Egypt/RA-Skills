## Description:

当用户想判断一个 AI 交易员在 Binance 上是否配拿到交易执照、该拿到哪一级、为什么会被降级时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[richard7463](https://clawhub.ai/user/richard7463)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to evaluate whether an AI trading agent should be allowed to touch a Binance account, what license level it should receive, and what risk controls should apply. It focuses on governance of trading permissions rather than finding trade opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading strategies, candidate symbols, loss streaks, sleep level, FOMO level, and state notes may be sent to a third-party service.

Mitigation: Ask for clear user intent before invoking the service and avoid sending API keys, account identifiers, wallet addresses, contact details, or private financial information.

Risk: The skill allows implicit invocation, which can make disclosure to the third-party service less obvious in trading conversations.

Mitigation: Confirm invocation before calling the API when the request contains personal, financial, behavioral, or account-related details.

Risk: Generated license results and share-image links may expose the agent name and assessment summary.

Mitigation: Treat license results and share-image URLs as shareable public artifacts and redact sensitive names or details before generating them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richard7463/skills/binance-agent-license-bureau)
- [License bureau API](https://binance-agent-license-bureau.vercel.app/api/license-bureau)
- [License bureau share-image API](https://binance-agent-license-bureau.vercel.app/api/license-bureau/share-image?payload=...)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or concise text summarizing the license level, board decision, candidate-asset pools, shadow exam results, human gate, runtime rules, ledger, and optional share-image link.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include a curl command for the public API and a Binance Square-ready Chinese draft when requested.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
