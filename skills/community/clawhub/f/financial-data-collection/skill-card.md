## Description: <br>
中国财政部财政收支数据采集与分析，负责运行财政部官网财政数据采集 pipeline，并对采集结果、导出数据和爬取异常进行结构化分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cy7533](https://clawhub.ai/user/cy7533) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect China Ministry of Finance fiscal revenue and expenditure announcements, transform cumulative values into monthly metrics, calculate fiscal deficit indicators, and generate structured fiscal data outputs for analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches financial data from network sources and writes generated files into the workspace. <br>
Mitigation: Run it in an isolated environment, review the configured source URL and output directory before execution, and avoid using sensitive workspaces for initial runs. <br>
Risk: Python dependencies and scraping behavior may change or introduce operational risk over time. <br>
Mitigation: Pin and audit dependencies before deployment, and review the crawler, parser, and exporter behavior when updating the environment. <br>
Risk: Source page structure or fiscal text formats may change, causing parse failures, missing prior-period data, duplicate records, or unit mismatches. <br>
Mitigation: Review warning logs, compare generated data against source announcements, and update parsing or transformation rules before relying on affected outputs. <br>


## Reference(s): <br>
- [China Ministry of Finance fiscal data releases](https://www.mof.gov.cn/gkml/caizhengshuju/) <br>
- [ClawHub skill page](https://clawhub.ai/cy7533/financial-data-collection) <br>
- [Publisher profile](https://clawhub.ai/user/cy7533) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands and generated Excel, Markdown, CSV, or chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files are organized under the workspace output directory, including raw documents, extracted metrics, derived metrics, monthly summaries, run reports, and optional analysis artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
