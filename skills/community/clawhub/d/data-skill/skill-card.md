## Description: <br>
Data Skill helps agents process office CSV and spreadsheet workflows locally with Python, SQL, SQLite, chart generation, exports, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgwanai](https://clawhub.ai/user/lgwanai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, analysts, and developers use this skill to import, clean, query, join, visualize, split, merge, and export office data while keeping most processing in local files and SQLite. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local Python and SQL, create persistent SQLite databases and output files, and start a local chart-preview web server. <br>
Mitigation: Review generated commands and output paths before execution, run in a controlled workspace, and remove local databases or generated files when they are no longer needed. <br>
Risk: Map/geocoding workflows may use Baidu services or remote chart assets, which can expose sensitive addresses or business data if used with confidential inputs. <br>
Mitigation: Use remote geocoding or external assets only with explicit approval and avoid sending sensitive addresses, customer data, or confidential business records. <br>
Risk: Cleanup operations can delete SQLite tables or local outputs. <br>
Mitigation: Confirm the database path, retention window, and tables affected before running cleanup commands. <br>
Risk: The security verdict is suspicious because privacy claims are broader than the observed network, persistence, server, and cleanup behavior. <br>
Mitigation: Treat local-only and privacy claims as conditional on the exact workflow being run, and review network, persistence, and deletion behavior during deployment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/lgwanai/data-skill) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Chart prompt index](artifact/references/prompts/index.md) <br>
- [Metrics definitions](artifact/references/metrics.md) <br>
- [Baidu Maps API key guide](https://lbsyun.baidu.com/index.php?title=jspopularGL/guide/getkey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL, Python, shell commands, JSON chart configs, and generated report/file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local SQLite databases, exported CSV/XLSX files, HTML chart previews, markdown reports, and metrics definitions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
