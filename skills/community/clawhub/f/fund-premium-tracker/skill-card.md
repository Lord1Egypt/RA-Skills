## Description: <br>
实时查询并分析A股场内基金（ETF/LOF/QDII）溢价率，提供价格、净值、溢价百分比及历史趋势风险提示。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cantoneyes](https://clawhub.ai/user/cantoneyes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance-focused agent users use this skill to query A-share listed fund premium or discount rates for ETF, LOF, and QDII funds. It produces current premium calculations, recent historical trends, and risk prompts for informational analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to public finance data providers when premium analysis is requested. <br>
Mitigation: Install and use it only in environments where outbound access to public finance APIs is acceptable. <br>
Risk: Premium calculations and trend prompts may be mistaken for financial advice. <br>
Mitigation: Treat results as informational market-data calculations and review them before making investment decisions. <br>
Risk: Broad finance trigger terms may activate the skill for some general finance prompts. <br>
Mitigation: Invoke it for explicit fund premium, discount, ETF, LOF, QDII, or arbitrage analysis requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cantoneyes/fund-premium-tracker) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style text with command examples and tabular CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include market price, NAV or intraday estimate, premium percentage, source labels, trend summaries, and risk prompts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
