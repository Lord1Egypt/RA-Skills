## Description: <br>
Analyzes A-share portfolio holdings with concentration, industry and style exposure, risk indicators, attribution, and rebalancing guidance using cn-stock-data market and financial data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzswk](https://clawhub.ai/user/yzswk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to review A-share portfolio holdings, compare them with a benchmark such as CSI 300, identify concentration and exposure risks, and prepare formal or brief rebalancing recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive portfolio holdings, cost basis, and purchase timing shared in chat. <br>
Mitigation: Avoid sharing broker logins, account numbers, or unnecessary personal identifiers, and keep the analysis limited to the current conversation. <br>
Risk: Market-data behavior depends on the separate cn-stock-data helper used for quotes, financial metrics, and benchmark data. <br>
Mitigation: Review the cn-stock-data helper before relying on its market-data behavior. <br>


## Reference(s): <br>
- [portfolio-guide.md](references/portfolio-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/yzswk/a-share-portfolio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown portfolio analysis with tables, risk notes, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports formal institutional reports and brief personal holding reviews.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
