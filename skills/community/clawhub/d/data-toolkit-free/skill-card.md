## Description: <br>
数据工具箱(免费版) guides an agent through data extraction, cleaning and transformation, exploratory analysis, and basic visualization tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business users use this skill to ask an agent for SQL queries, data cleaning steps, descriptive summaries, KPI explanations, and simple chart generation. It is aimed at everyday personal or workflow data analysis rather than advanced statistical testing, monitoring, or automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to read files, query databases or APIs, run commands, and write output files. <br>
Mitigation: Confirm allowed files, data sources, APIs, and output paths before use; prefer previews or dry runs before modifying data. <br>
Risk: Database connection strings or API tokens may be needed for data access. <br>
Mitigation: Keep credentials in environment variables and avoid hardcoding secrets in scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/data-toolkit-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL, Python, shell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce proposed queries, scripts, data summaries, chart files, and structured result payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
