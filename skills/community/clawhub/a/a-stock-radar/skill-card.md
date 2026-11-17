## Description:

A Stock Radar monitors Chinese A-share indices, sectors, macro indicators, core companies, limit-up/limit-down pools, and short-term sentiment to produce market snapshots and non-binding position guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gold3bear](https://clawhub.ai/user/gold3bear)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer A-share market questions, summarize index and sector movement, inspect selected large-cap companies, assess macro and short-term sentiment signals, and produce research-only trading posture suggestions.

### Deployment Geography for Use:

Global, with market coverage focused on Chinese A-shares

## Known Risks and Mitigations:

Risk: Position guidance may be based on failed or stale sentiment data.

Mitigation: Treat trading posture suggestions as research references only and verify them against current market data before acting.

Risk: The skill contacts public market-data providers for quotes, sectors, macro data, and sentiment inputs.

Mitigation: Install and run it only in environments where outbound access to those public finance data sources is acceptable.

Risk: Unpinned dependencies and provider-side API changes can alter or break results.

Mitigation: Use a controlled environment with reviewed dependency versions and monitor failures or empty data before trusting summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gold3bear/skills/a-stock-radar)
- [Eastmoney quote center](https://quote.eastmoney.com/center/gridlist.html)
- [Sina Finance](http://finance.sina.com.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style Chinese market summaries with numeric snapshots, position guidance, and risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are non-binding research references and depend on public market-data providers that may fail or return stale data.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
