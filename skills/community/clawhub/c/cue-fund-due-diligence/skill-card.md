## Description:

用 Cue 为 A 股公募权益基金生成涵盖基金经理、业绩归因、风格、风险、持仓、费率与规模的尽调报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

个人投资者、基金投顾与研究人员可用它检查 A 股公募权益基金的经理记录、历史业绩归因、风格稳定性、风险和成本，为研究与申赎决策提供参考。它不覆盖债券、货币或私募基金，也不预测未来表现或提供择时建议。

### Deployment Geography for Use:

China (A-share public equity funds)

## Known Risks and Mitigations:

Risk: The security review reports that the skill asks users to share an API key in chat.

Mitigation: Do not send API keys in chat; configure credentials through a trusted local secret store or environment variable, and verify the service before use.

Risk: The security review identifies promotional prompts unrelated to fund analysis.

Mitigation: Ignore reward, purchase, and sharing prompts; keep the interaction limited to the user's requested fund research.

Risk: The security review says setup and conversion behavior does not match the stated fund-analysis purpose, and notes that the scan was partial.

Mitigation: Inspect and verify the service and runner behavior before execution, and do not rely on the partial scan as proof that all behavior was reviewed.

## Reference(s):

- [Cue platform](https://cuecue.cn)
- [ClawHub release page](https://clawhub.ai/panting09266-ai/skills/cue-fund-due-diligence)
- [天天基金](https://fund.eastmoney.com)
- [晨星中国](https://www.morningstar.cn)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Structured Markdown fund due diligence report with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fund-specific assessment; completeness and timeliness depend on public disclosures and Cue service availability.]

## Skill Version(s):

1.0.14 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
