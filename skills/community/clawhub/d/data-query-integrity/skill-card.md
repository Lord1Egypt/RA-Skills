## Description: <br>
Enforces completeness checks for API-backed data queries and summaries, including pagination, source tracing, and verified date/time conversions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiyinli811-crypto](https://clawhub.ai/user/xiyinli811-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when agents query APIs, summarize returned records, or convert returned dates and timestamps. It helps agents paginate fully, identify incomplete data, trace output fields to source records, and disclose query completeness to users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may summarize incomplete API results if pagination, errors, or unexpectedly small result sets are not checked. <br>
Mitigation: Check has_more, continue pagination until completion, retry or narrow failed queries, and disclose any incomplete ranges before summarizing. <br>
Risk: An agent may introduce unsupported facts by filling gaps in API responses from assumptions. <br>
Mitigation: Trace each key output field to the raw API response and omit or mark records whose required fields are missing. <br>
Risk: Manual date, weekday, timezone, or timestamp conversion can produce wrong results even when source data is valid. <br>
Mitigation: Verify conversions with a local date/time command or preserve the original timestamp with its format. <br>


## Reference(s): <br>
- [Detailed workflow](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should disclose API query count, pagination status, and any incomplete data ranges when applicable.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
