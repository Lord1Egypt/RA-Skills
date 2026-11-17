## Description:

用 Cue 深度分析热门赛道与 ETF，涵盖赛道全景、同类 ETF 对比、底层持仓和估值水位。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

个人 ETF 投资者、定投用户及理财专业人士可用它比较 A 股上市 ETF、分析赛道和持仓，并查看估值与相关风险，辅助研究决策。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the skill asks users to share an API key in chat, creating a credential exposure concern.

Mitigation: Do not send API keys in chat; configure credentials through a private secret store or local configuration, and rotate any key that was shared.

Risk: The security evidence reports that the skill fetches and runs remote content.

Mitigation: Review the source and downloaded code before execution, and verify the origin and changes of updates before running them.

Risk: The security evidence notes promotional prompts and behavior that does not match the stated ETF research purpose; scan coverage is partial and leaves a path-like reference unresolved.

Mitigation: Review the full skill and referenced files before use, and disregard unrelated promotional requests or actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panting09266-ai/skills/cue-sector-etf)
- [Cue research service](https://cuecue.cn)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Chinese research report in Markdown, with ETF comparison tables, valuation context, risk notes, and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers A-share-listed ETFs; does not provide buy/sell timing recommendations or intraday net asset values.]

## Skill Version(s):

1.0.11 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
