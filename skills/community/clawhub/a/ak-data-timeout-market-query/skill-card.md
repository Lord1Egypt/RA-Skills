## Description: <br>
Query timeout status and market timeout ranking for any single job type on huge sharded job tables (job_a~job_d) without index changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leehoo29](https://clawhub.ai/user/leehoo29) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to investigate timeout behavior for a single AK Data job type across sharded job tables. It guides daily SQL analysis, market ranking, duration summaries, sample extraction, and chart-ready reporting without changing database indexes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The authoritative security scan marked the release suspicious and warns that related helper behavior can bypass normal sandbox controls or route diffs to external reviewer CLIs. <br>
Mitigation: Install only in trusted maintainer environments, prefer non-yolo review settings when available, and manually review moderation, PR publishing, or role-change commands before execution. <br>
Risk: The skill generates SQL for very large sharded job tables, which can be expensive or incomplete if run outside its stated single-day and single-job-type constraints. <br>
Mitigation: Keep each SQL request to one job type and one 24-hour Beijing-time window, use the specified created_at index, and merge multi-day results outside the database. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leehoo29/ak-data-timeout-market-query) <br>
- [Publisher profile](https://clawhub.ai/user/leehoo29) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with SQL code blocks, JSON-style result contracts, and chart configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are scoped to one tenant, one job type, and single-day SQL windows; recent queries are split by day and merged outside the database.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
