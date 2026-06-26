## Description: <br>
用于抓取并总结指定城市（如上海、北京）在特定领域（如人工智能、大模型、算法）的岗位信息。当用户询问某地的某类职位招聘情况时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[batiger](https://clawhub.ai/user/batiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers or agents supporting job seekers use this skill to collect BOSS Zhipin AI job listings for a selected city, compare them with prior collections, and produce summaries that highlight new openings, salary ranges, company context, and application priorities. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks the agent to control a logged-in browser session for BOSS Zhipin job collection. <br>
Mitigation: Use a dedicated Chrome profile or account for this workflow, keep no unrelated sessions in that browser profile, and review browser automation before execution. <br>
Risk: The workflow may install Python dependencies and change the local execution environment. <br>
Mitigation: Approve Python and package installation manually, preferably in an isolated virtual environment. <br>
Risk: Collected job data, generated reports, and historical comparisons may contain personal job-search context or sensitive local files. <br>
Mitigation: Restrict outputs and historical comparisons to a dedicated folder and review generated CSV, text, HTML, and optional image files before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/batiger/extract-boss-job) <br>
- [BOSS Zhipin job search URL used by the crawler](https://www.zhipin.com/web/geek/jobs?query=%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%B7%A5%E7%A8%8B%E5%B8%88&city=101020100) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell/Python execution steps plus generated CSV or Excel data, text summaries, and HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May optionally generate image outputs from the HTML report when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
