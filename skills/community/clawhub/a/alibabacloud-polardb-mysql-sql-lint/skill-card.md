## Description: <br>
Pre-release SQL assessment and optimization for PolarDB MySQL, combining static SQL lint rules with Alibaba Cloud DAS dynamic diagnosis to detect query, schema, and indexing issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database engineers, and reviewers use this skill to assess PolarDB MySQL SQL before release, identify static lint violations, and optionally request DAS-backed execution-plan and index recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full DAS mode uses cloud credentials and cloud API permissions. <br>
Mitigation: Run full DAS mode only in an isolated environment with least-privilege, short-lived Alibaba Cloud credentials. <br>
Risk: Setup instructions include a curl-to-bash installer path. <br>
Mitigation: Use reviewed package-manager or manual installation steps instead of piping remote installer output directly to a shell. <br>
Risk: Broad extended RAM permissions can increase cloud-permission exposure. <br>
Mitigation: Prefer the minimal documented RAM policy and avoid broad extended permissions unless separately reviewed. <br>
Risk: The security guidance identifies a shell-command construction bug affecting untrusted SQL. <br>
Mitigation: Require the shell-command construction issue to be fixed before running the skill on untrusted SQL. <br>
Risk: Optimization recommendations may be incorrect or incomplete without human context. <br>
Mitigation: Treat findings as advisory, review all SQL and index recommendations manually, and avoid direct database execution by the agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-polardb-mysql-sql-lint) <br>
- [Publisher profile](https://clawhub.ai/user/sdk-team) <br>
- [SQL Linting Rules Reference](references/sql-lint-rules.md) <br>
- [Output Format Specification](references/output-format.md) <br>
- [RAM Policies for SQL Linting Skill](references/ram-policies.md) <br>
- [Safety Guidelines](references/safety-guidelines.md) <br>
- [Workflow Examples](references/workflow-examples.md) <br>
- [Implementation Notes and Known Issues](references/implementation-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with optional JSON report output and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes static lint findings, optional DAS diagnosis details, index recommendations, SQL rewrite guidance, and a notice that recommendations require user review.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
