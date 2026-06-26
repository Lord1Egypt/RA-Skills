## Description: <br>
Generates read-only SQL-based order statistics for the 久事体育 app over configurable time ranges, keywords, and supported time dimensions such as hour, day, or month. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaggerliu](https://clawhub.ai/user/jaggerliu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Data and operations analysts use this skill to query app order trends by time period and keyword, then receive a Markdown table and Chinese summary of users, orders, payments, refunds, and net sales. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can connect an agent to a real business order database. <br>
Mitigation: Install only in authorized internal environments and use a narrowly scoped read-only database account. <br>
Risk: The artifact builds SQL from user-provided dates and keywords without strong guardrails. <br>
Mitigation: Require parameterized SQL or strict validation for dates, time dimensions, and keywords before live query execution. <br>
Risk: Database credentials or connection details could be exposed through agent output or logs. <br>
Mitigation: Read secrets from environment variables, avoid broad production credentials, and never display passwords or full connection strings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jaggerliu/app-order-date-key-stats) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown table with SQL/Python execution guidance and Chinese summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python plus mysql-connector-python, pandas, and tabulate; expects authorized database environment variables for live queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
