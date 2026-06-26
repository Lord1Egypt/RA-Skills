## Description: <br>
Queries and operates Baidu Intelligent Cloud Log Service (BLS) by listing projects and logstores, inspecting index configuration, generating BLS match or SQL queries, and calling the BLS API to retrieve log results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoming23333](https://clawhub.ai/user/xiaoming23333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect Baidu Log Service resources, build correct BLS match or SQL queries, and retrieve log records for troubleshooting and analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BLS credentials may be exposed if secret keys are passed directly on the command line. <br>
Mitigation: Prefer environment variables or the configured credentials file, and use least-privilege, preferably read-only BLS credentials. <br>
Risk: Broad log queries can return secrets, personal data, or excessive log volume. <br>
Mitigation: Confirm the region, project, logstore, query, and time window before execution, and narrow searches when possible. <br>
Risk: Queries against unindexed JSON fields may be expensive or slow. <br>
Mitigation: Inspect index configuration first and enable field indexes in the BLS console before relying on broad fallback SQL extraction. <br>


## Reference(s): <br>
- [BLS API Reference](references/api_reference.md) <br>
- [BLS SQL Syntax](references/sql_syntax.md) <br>
- [BLS Match Syntax](references/match_syntax.md) <br>
- [Baidu Cloud BCE Authentication Reference](https://cloud.baidu.com/doc/Reference/s/Njwvz1wot) <br>
- [ClawHub Skill Release Page](https://clawhub.ai/xiaoming23333/bls-skill) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/xiaoming23333) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, generated BLS queries, and tabular or raw log-result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Baidu Log Service APIs and return log data from the user's selected region, project, logstore, query, and time window.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
