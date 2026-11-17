## Description:

跨市场交易终端 helps agents provide Chinese-language guidance for cryptocurrency cross-market trading analysis, multi-account workflows, API-key setup, market data review, and structured trading-related outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill for Chinese-language cryptocurrency trading analysis, cross-market workflow planning, API setup guidance, and structured outputs for market, account, and risk-review tasks. Because the release describes live trading and account/API-key use, users should treat outputs as guidance unless they have intentionally configured safe trading controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes live cross-market trading and account/API-key use without enough guardrails for financial actions.

Mitigation: Review before installing, prefer paper-trading or read-only API keys, restrict key permissions, and require explicit confirmation before any order placement or account-changing action.

Risk: Secrets such as exchange or broker API keys may be exposed if pasted into chats, logs, or broad configuration contexts.

Mitigation: Keep secrets out of chat transcripts and logs, store them in environment variables or a secret manager, and rotate keys if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cross-market)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)
- [Skill homepage from artifact metadata](https://skillhub.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON snippets with occasional shell commands or configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading-analysis reports, risk-control suggestions, API setup steps, and structured success/error payloads.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
