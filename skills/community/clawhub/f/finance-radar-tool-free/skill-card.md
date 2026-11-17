## Description:

股票与加密货币基础分析工具，用于查询单只标的价格、基本面、技术面、股息信息，并生成8维度评分。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this Chinese-language skill for quick, single-ticker stock or crypto screening before deeper investment research. Outputs are informational analysis and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution for finance lookups.

Mitigation: Review proposed pip install and shell commands before running them, and limit use to explicit stock or crypto analysis requests.

Risk: The skill describes broad file, automation, and export capabilities beyond its finance-analysis purpose.

Mitigation: Keep agent permissions scoped to the specific finance lookup workflow and avoid granting unrelated file or automation access.

Risk: Generated stock or crypto analysis may be mistaken for investment advice.

Mitigation: Treat outputs as informational screening only and require independent review before investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/finance-radar-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and finance-analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current-price, fundamentals, technical indicators, dividend details, and 8-dimension score summaries for a single ticker.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
