## Description: <br>
A-share quantitative trading backtesting using AKQuant and AKShare data for testing and comparing double-MA, RSI, and custom A-share strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lamtest556-blip](https://clawhub.ai/user/lamtest556-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run historical backtests for Chinese A-share trading ideas, compare strategy parameters, and interpret reported returns and trade counts. It is for backtesting workflows, not for live trading or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the package includes unrelated personal-looking portfolio data in config/holdings.yaml. <br>
Mitigation: Review or remove config/holdings.yaml before use, especially before sharing the installed skill or running it in a managed environment. <br>
Risk: The security guidance notes unpinned Python package installation, AKShare market-data fetching, and optional local CSV cache behavior. <br>
Mitigation: Install dependencies in a controlled virtual environment, pin package versions where possible, and confirm network and local-data behavior before running backtests. <br>
Risk: Backtest results can be misleading if treated as investment advice or as evidence of future returns. <br>
Mitigation: Use outputs as historical simulations only, validate assumptions independently, and apply appropriate financial review before making decisions. <br>


## Reference(s): <br>
- [AKQuant Cheat Sheet](references/akquant_cheatsheet.md) <br>
- [AKShare Documentation](https://www.akshare.xyz/) <br>
- [AKQuant GitHub](https://github.com/akfamily/akquant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks plus backtest result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Backtest outputs depend on AKShare data availability and any local CSV cache; results are informational and should not be treated as investment advice.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
