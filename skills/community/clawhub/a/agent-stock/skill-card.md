## Description: <br>
Agent Stock helps agents retrieve real-time stock data, screen candidates, analyze holdings, and produce short-term trading or quantitative decision guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anoyix](https://clawhub.ai/user/anoyix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to support stock screening, individual stock trade analysis, quantitative decision workflows, and portfolio holdings reviews. It is oriented toward short-term trading workflows that combine market data, risk checks, and markdown report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated trading recommendations may be incorrect, incomplete, or unsuitable for the user's financial situation. <br>
Mitigation: Treat outputs as decision support only, independently verify market data and risk, and consult appropriate financial expertise before acting. <br>
Risk: Holdings, balances, trading plans, or other sensitive financial details may be saved in local markdown reports under dist/. <br>
Mitigation: Avoid providing brokerage passwords, API keys, or unnecessary personal financial details, and delete or protect saved reports when they include sensitive information. <br>
Risk: The workflow depends on the external agent-stock Python package and stock command behavior. <br>
Mitigation: Install only from trusted package sources and review the package and generated commands before use in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anoyix/agent-stock) <br>
- [Stock screening workflow](references/screen.md) <br>
- [Stock trade decision workflow](references/trade.md) <br>
- [Quantitative trade decision workflow](references/quant.md) <br>
- [Quantitative scoring rules](references/quant_rule.md) <br>
- [Holdings analysis workflow](references/holdings.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown reports with stock command usage and structured decision tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local markdown reports under dist/ for screening, trade decisions, quantitative analysis, and holdings reviews.] <br>

## Skill Version(s): <br>
0.2.8 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
