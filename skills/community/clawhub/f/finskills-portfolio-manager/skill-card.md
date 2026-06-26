## Description: <br>
Monitor and rebalance a multi-asset portfolio using real-time quotes, sector allocation, and risk metrics from the Finskills API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finskills](https://clawhub.ai/user/finskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze US equity holdings, compare portfolio performance with market benchmarks, identify concentration risks, and generate rebalancing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio details and cost basis can be sensitive financial information. <br>
Mitigation: Provide only the holdings data needed for the analysis and avoid unnecessary personally identifying financial details. <br>
Risk: The skill requires a Finskills API key for market-data lookups. <br>
Mitigation: Store FINSKILLS_API_KEY in an environment variable or secret store and avoid pasting it into chat history. <br>
Risk: Portfolio recommendations may be incomplete or unsuitable for a user's financial situation. <br>
Mitigation: Verify market data and recommendations before making investment decisions; treat the output as analysis, not automated trading. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/finskills/finskills-portfolio-manager) <br>
- [Project homepage](https://github.com/finskills/portfolio-manager) <br>
- [Finskills API](https://finskills.net) <br>
- [Finskills API registration](https://finskills.net/register) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown portfolio report with tables, metrics, risk flags, market context, and rebalancing recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided holdings and a Finskills API key; does not connect to brokerage accounts or execute trades.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
