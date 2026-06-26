## Description: <br>
查询 Datayes/通联的宏观与行业指标数据，用于搜索并拉取 GDP、CPI、PPI、PMI、M2、社融、利率、就业、贸易、产量、价格等宏观或行业时间序列。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datayes](https://clawhub.ai/user/datayes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to answer macroeconomic or industry-data questions by searching Datayes indicators, selecting the closest time series, and retrieving recent values with a local Python helper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Datayes API token may be exposed if it is pasted into chats, printed in logs, or used in shared shell environments. <br>
Mitigation: Use a scoped and revocable DATAYES_TOKEN, avoid pasting or printing it, and rotate the token if exposure is suspected. <br>
Risk: Macro-data requests depend on a user-provided Datayes token and external Datayes-related endpoints. <br>
Mitigation: Run the helper only in environments approved for Datayes access and review requested indicators and date ranges before using the results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/datayes/datayes-macro) <br>
- [Datayes login](https://r.datayes.com/auth/login) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown summary with optional JSON output from the Python helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a DATAYES_TOKEN environment variable; the helper can print JSON when invoked with --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
