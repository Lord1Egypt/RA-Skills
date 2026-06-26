## Description: <br>
Query and control Databricks jobs from plain text, including run status, failures, retries, cancellations, logs, Unity Catalog exploration, and read-only SQL through the Databricks REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nerikko](https://clawhub.ai/user/Nerikko) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and data platform operators use this skill to inspect Databricks job health, diagnose failed or long-running runs, trigger or repair jobs, cancel active runs, browse Unity Catalog objects, and run bounded SQL queries from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger, retry, repair, or cancel live Databricks job runs. <br>
Mitigation: Require manual confirmation before job trigger, retry, repair, or cancellation commands and use a token limited to the smallest Databricks permissions needed. <br>
Risk: Run details, logs, notebook output, and SQL results may expose sensitive operational or data content. <br>
Mitigation: Review log and output requests before execution, avoid sharing results outside trusted contexts, and prefer CAN_VIEW or similarly scoped read permissions for routine inspection. <br>
Risk: SQL execution can modify data if DATABRICKS_ALLOW_WRITE_SQL is enabled. <br>
Mitigation: Keep DATABRICKS_ALLOW_WRITE_SQL unset for normal use, rely on the default read-only SQL guardrails, and set row and timeout limits for exploration queries. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Nerikko/databricks-helper) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands and tabular command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Databricks run output may include statuses, URLs, error snippets, logs, catalog listings, and SQL result rows; SQL output is row-limited by default.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, README changelog, script __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
