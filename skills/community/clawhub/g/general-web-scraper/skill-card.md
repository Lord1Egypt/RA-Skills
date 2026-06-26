## Description: <br>
通用网页数据抓取工具 — 支持CSS选择器抓取链接、表格数据提取，输出CSV/JSON格式。无需配置，开箱即用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuxiangfacai](https://clawhub.ai/user/wuxiangfacai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to collect links or HTML table data from authorized webpages with CSS selectors, then export the results as CSV or JSON for research, monitoring, or content aggregation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Collecting data from websites or pages without authorization. <br>
Mitigation: Confirm permission to collect from each configured source before running the scraper. <br>
Risk: Exported CSV or JSON files may contain private, sensitive, or regulated data. <br>
Mitigation: Review collected data before sharing it and store exports in a controlled location. <br>
Risk: Scheduled or repeated scraping can run beyond the intended scope. <br>
Mitigation: Review automation settings so the skill only runs against expected sources and at expected times. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuxiangfacai/general-web-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text] <br>
**Output Format:** [CSV or JSON files with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output.csv by default or output.json when JSON export is requested; accepts a target URL, optional CSS selector, and table mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
