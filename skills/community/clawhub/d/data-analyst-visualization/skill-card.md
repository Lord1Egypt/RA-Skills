## Description: <br>
LLM-powered intelligent data analysis assistant supporting natural language queries, SQL generation, visualization, and multi-turn conversation for business analysis, report automation, and data exploration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, business analysts, and developers use this skill to query files or connected databases in natural language, generate read-only SQL, summarize results, and produce Markdown summaries plus HTML charts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read selected local files or query configured databases. <br>
Mitigation: Use read-only, least-privilege database accounts and only provide files or database connections appropriate for agent analysis. <br>
Risk: Generated SQL or analysis may be incorrect or broader than intended. <br>
Mitigation: Review generated SQL before execution and use table whitelists, limits, or time ranges for large datasets. <br>
Risk: Generated HTML chart files may contain sensitive query results. <br>
Mitigation: Delete generated chart files when they contain sensitive results and avoid sharing them outside the intended audience. <br>
Risk: Database credentials may be exposed if pasted directly into chat. <br>
Mitigation: Avoid pasting long-lived production passwords directly into chat. <br>


## Reference(s): <br>
- [Data Source Configuration & Connection](references/data-sources.md) <br>
- [HTML Visualization Page Template](references/visualization-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/openlark/data-analyst-visualization) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance, files] <br>
**Output Format:** [Markdown summaries with SQL snippets and optional standalone HTML chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask clarifying questions, mask privacy fields, prompt for limits on large datasets, and report generated chart file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
