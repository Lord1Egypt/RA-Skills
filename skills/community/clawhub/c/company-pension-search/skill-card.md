## Description: <br>
智能查询企业年金及职业年金，自动识别单位性质和年金类型，多渠道验证并输出带来源链接的标准调查报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanwenzhe](https://clawhub.ai/user/yanwenzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, job candidates, benefits researchers, and analysts use this skill to investigate whether Chinese companies or public institutions offer enterprise annuities or occupational annuities, including likely annuity type, pension account bank roles, confidence, and source links. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Report and log file paths may include unsanitized company names. <br>
Mitigation: Do not run the skill with company names or batch entries containing slashes, '..', or other path-like characters; review generated paths before keeping or sharing files. <br>
Risk: Queries may disclose sensitive or confidential target names to the configured search provider. <br>
Mitigation: Use the skill only for public-source company pension research and avoid sensitive target names unless the configured search provider is trusted. <br>
Risk: Generated reports may contain incomplete or unverified conclusions. <br>
Mitigation: Treat reports as templates requiring manual verification of source links, confidence levels, and final conclusions. <br>
Risk: Saved reports, logs, or cache can persist investigation details locally. <br>
Mitigation: Clear saved reports, logs, and cache when the investigation should not persist. <br>


## Reference(s): <br>
- [企业年金调查方法全指南](artifact/references/search-methods.md) <br>
- [企业年金信息查询渠道拓展分析](artifact/references/advanced-search-channels.md) <br>
- [ClawHub skill page](https://clawhub.ai/yanwenzhe/company-pension-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, text summaries, JSON search output, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local report and log files; uses curl and jq, with optional Tavily API or SearXNG search configuration.] <br>

## Skill Version(s): <br>
3.2.1 (source: server release metadata; artifact frontmatter reports 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
