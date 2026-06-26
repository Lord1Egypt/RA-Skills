## Description: <br>
Generate semantic YAML files from databases or Excel workbooks for semantic models, topic configurations, and table structure definitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asksqlai](https://clawhub.ai/user/asksqlai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to discover database tables or Excel sheets, select relevant sources, and generate OSI-style semantic YAML for AskSQL and text-to-SQL workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database samples and spreadsheet contents may be sent to AskSQL or another configured API endpoint. <br>
Mitigation: Use only data the user is allowed to send, prefer redacted test databases or non-sensitive spreadsheets, and confirm the endpoint before generation. <br>
Risk: Database connection strings may contain credentials that can appear in chat, shell history, or logs. <br>
Mitigation: Use short-lived or least-privilege credentials and avoid placing real secrets directly in prompts, saved commands, or shared logs. <br>
Risk: The database upload path prints the table payload before calling the API, which may expose sampled data in terminal output. <br>
Mitigation: Disable or remove that print before handling sensitive data, or run only with sanitized samples in a controlled terminal. <br>


## Reference(s): <br>
- [Open Semantic Interchange Field Specification](references/open_semantic_interchange_description.md) <br>
- [AskSQL](https://www.asksql.ai) <br>
- [ClawHub skill page](https://clawhub.ai/asksqlai/database-semantic-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [YAML files plus JSON command status and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates one topic YAML file per run after a discover, select, and generate workflow; selected tables or sheets can limit scope.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
