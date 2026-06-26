## Description: <br>
数据分析技能包 - 自动抓取、清洗、可视化、生成报告。适合数据分析师、运营人员，告别 Excel 手工操作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gdp6539](https://clawhub.ai/user/gdp6539) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Data analysts, operations teams, market researchers, product managers, and finance users use this skill to fetch data, clean datasets, create visualizations, and generate analysis reports from common web, API, database, CSV, JSON, and Excel sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch data from web, API, and database sources that may require credentials or authorization. <br>
Mitigation: Use only authorized data sources and keep API tokens, database passwords, and other secrets in environment variables or a secret manager instead of hardcoding them in configuration. <br>
Risk: Generated analysis reports may include sensitive data or conclusions that need human review. <br>
Mitigation: Review generated reports before sharing them and confirm that the underlying data, charts, and conclusions are appropriate for the audience. <br>
Risk: PDF export calls an external command-line tool. <br>
Mitigation: Use PDF export only in a reviewed local environment and confirm the external tool and output paths before generating or distributing PDF reports. <br>


## Reference(s): <br>
- [Artifact README](artifact/README.md) <br>
- [ClawHub Release Page](https://clawhub.ai/gdp6539/data-analysis-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/gdp6539) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript command examples, JSON configuration examples, generated charts, and Markdown, HTML, or PDF reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes cleaned datasets, visualization files, and reports to local output paths selected by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
