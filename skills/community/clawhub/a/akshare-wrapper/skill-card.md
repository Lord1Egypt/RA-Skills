## Description:

A股分析技能包装器，基于akshare数据源。支持实时行情、个股分析、板块轮动、资金流向等A股分析功能。使用自然语言查询A股市场数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongjiaping2010-coder](https://clawhub.ai/user/hongjiaping2010-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query A-share market data in natural language, including index行情, individual stock analysis, sector rotation, capital flows, market statistics, news, and simple portfolio-oriented prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the wrapper delegates queries to a separate local akshare-stock skill path that was not reviewed in this evidence.

Mitigation: Install only when that dependency is trusted, reviewed, and present at the expected path; use an isolated environment with pinned dependencies.

Risk: The security scan notes advertised portfolio changes without documented storage or deletion safeguards.

Mitigation: Avoid entering real holdings until storage, retention, and deletion behavior are documented and reviewed.

Risk: Financial market data may be delayed, unavailable, or affected by upstream source limits.

Mitigation: Treat outputs as research support, verify important data against authoritative market data, and avoid high-frequency querying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hongjiaping2010-coder/skills/akshare-wrapper)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-like chat text with Chinese financial data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include emoji, highlighted values, sections, timestamps, and upstream data-source delay notices.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
