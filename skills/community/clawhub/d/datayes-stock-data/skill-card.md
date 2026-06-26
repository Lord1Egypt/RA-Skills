## Description: <br>
通过 Datayes 查询 A 股和港股的行情、分时、K 线、财务、估值、资金流向、股东持仓、分红和公司资料。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shermanxli](https://clawhub.ai/user/shermanxli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer A-share and Hong Kong stock-data questions with Datayes market, financial, valuation, fund-flow, holdings, dividend, and company-profile APIs. It helps resolve company names to tickers, inspect API parameters, run Datayes queries, and summarize returned values with units, dates, and data scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-provided Datayes token to request market and financial data. <br>
Mitigation: Use a revocable, least-privilege token, provide it through the DATAYES_TOKEN environment variable, and do not commit the token to a repository. <br>
Risk: Returned data may be proprietary or account-scoped. <br>
Mitigation: Review command output before sharing it and avoid exposing raw results outside authorized contexts. <br>


## Reference(s): <br>
- [Datayes API Catalog](references/api-catalog.md) <br>
- [Datayes Token Login](https://r.datayes.com/auth/login) <br>
- [ClawHub Skill Page](https://clawhub.ai/shermanxli/datayes-stock-data) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and DATAYES_TOKEN; command output may include Datayes market data returned by the user's account.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
