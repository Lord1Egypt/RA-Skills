## Description: <br>
Screens a China A-share candidate pool using Eastmoney public real-time main net inflow data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luyao-inc](https://clawhub.ai/user/luyao-inc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-analysis agents use this skill to run a bundled Python script that returns ranked China A-share candidates filtered by market capitalization, price change, and public main net inflow data. The output is for screening and reference only, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Python script makes outbound requests to Eastmoney for public stock data. <br>
Mitigation: Install and run the skill only in environments where outbound access to Eastmoney is acceptable. <br>
Risk: The stock rankings may be incomplete, approximate, or unsuitable for investment decisions. <br>
Mitigation: Treat outputs as screening information only and verify results against authoritative financial sources before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luyao-inc/china-stock-main-force) <br>
- [Eastmoney public quote API](https://push2.eastmoney.com/api/qt/clist/get) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON emitted by a Python command, with supporting Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Rows include symbols, names, price change, main net inflow, market capitalization, turnover, PE, and PB when returned by the public data source.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
