## Description: <br>
Data Query converts natural-language data questions into validated SQL and generates ECharts-based HTML dashboards from mounted database knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ylyuanlu](https://clawhub.ai/user/ylyuanlu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data analysts use this skill to turn business data questions into executable SQL, preview query results, and generate deployable single-chart or cockpit-style HTML dashboard pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shipped database and API credentials could grant access to external business data. <br>
Mitigation: Rotate or remove the shipped credentials before use, store secrets in environment variables or a secrets manager, and use least-privileged read-only tenant-scoped accounts. <br>
Risk: Generated HTML can execute embedded SQL through the backend and reuse browser session tokens. <br>
Mitigation: Review generated HTML and SQL before deployment, deploy only in the intended ACM environment, and restrict backend/API access. <br>
Risk: Natural-language SQL generation may produce incorrect or misleading queries or results. <br>
Mitigation: Run the skill's SQL verification flow and require human review before using results for operational or business decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ylyuanlu/data-query) <br>
- [Publisher profile](https://clawhub.ai/user/ylyuanlu) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [SQL generation rules](artifact/knowledge/shared/sql_generation_rules.md) <br>
- [ShardingSphere routing rules](artifact/database_specs/sharding/ROUTING_RULES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, HTML files] <br>
**Output Format:** [Markdown guidance with JavaScript and shell snippets, JSON query previews, and generated HTML dashboard files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated pages can embed encrypted SQL and should be reviewed and validated before deployment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
