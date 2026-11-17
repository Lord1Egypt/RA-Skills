## Description:

chundengtai-v3 is an A-share short-term technical analysis skill that uses Tencent market data, V3 quantitative scoring, qualitative stock classification, sell rules, and position controls for overnight short-term and trend-following workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinxulin8899-dotcom](https://clawhub.ai/user/jinxulin8899-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze, diagnose, or screen A-share stocks and produce short-term trading commentary. It can provide scored entries, sell triggers, and position sizing guidance for overnight short-term and trend-following scenarios.

### Deployment Geography for Use:

Global; content is focused on Chinese A-share market analysis.

## Known Risks and Mitigations:

Risk: Prescriptive short-term buy, sell, stop-loss, and position-sizing guidance may be mistaken for personalized investment advice.

Mitigation: Treat outputs as market commentary only, confirm data freshness, and require independent review before making investment decisions.

Risk: Market data retrieved from public endpoints may be stale, unavailable, or incomplete during analysis.

Mitigation: Check the output's data freshness marker and cross-check prices and signals against a trusted market data source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinxulin8899-dotcom/skills/chundengtai-v3)
- [Tencent real-time quote endpoint](https://qt.gtimg.cn/q=sh600143)
- [Tencent historical K-line endpoint](https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sh600143,day,,,60,qfq)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text with pipe-delimited tables and data freshness and quality-control notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are expected to include a data freshness marker and a quality-control footer when following the skill's output contract.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
