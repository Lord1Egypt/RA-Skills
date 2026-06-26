## Description: <br>
Chance Dlt Predictor helps agents analyze China Sports Lottery Da Le Tou data with frequency, omission, trend, parity, range, span, and Monte Carlo methods to produce rational number-selection guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gechengling](https://clawhub.ai/user/gechengling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to analyze Da Le Tou lottery history, generate filtered candidate number sets, and format responsible lottery analysis reports. Outputs are for entertainment reference and rational budgeting, not financial advice or a winning strategy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may misread historical lottery analysis as financial advice or a winning strategy. <br>
Mitigation: State that lottery outcomes are random, outputs are entertainment reference only, and users should set fixed budgets and avoid chasing losses. <br>
Risk: Broad lottery-related trigger wording may activate the skill when the conversation is only loosely related. <br>
Mitigation: Confirm that the user wants Da Le Tou lottery analysis before producing recommendations or candidate number sets. <br>
Risk: Generated examples may rely on stale or unavailable draw history. <br>
Mitigation: Prefer user-provided draw data or clearly identify the data cutoff and fallback sample data when current history cannot be fetched. <br>


## Reference(s): <br>
- [DLT Algorithm Python Reference](references/dlt_algorithm_python.md) <br>
- [DLT Data Templates](references/dlt_data_templates.md) <br>
- [DLT Strategy Guide](references/dlt_strategy_guide.md) <br>
- [China Sports Lottery History API](https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports with candidate number sets, analysis tables, and optional Python or shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Lottery outputs should be framed as entertainment reference only and should include responsible betting guidance.] <br>

## Skill Version(s): <br>
4.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
