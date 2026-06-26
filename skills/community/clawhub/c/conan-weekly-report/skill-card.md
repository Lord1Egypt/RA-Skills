## Description: <br>
名侦探柯南动画周报技能。每周自动收集并整理柯南最新剧情进展，包括主线剧情、特别篇、角色动态等。使用 DuckDuckGo HTML 搜索获取真实网页数据。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[HubertSing](https://clawhub.ai/user/HubertSing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External anime viewers and Conan fans use this skill to collect public web search results about recent Detective Conan episodes, main-plot developments, specials, character updates, and production news into a weekly report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs public web searches, so report completeness and accuracy depend on network access and the availability of public search results. <br>
Mitigation: Review generated reports and source links against official or trusted information channels before relying on the summary. <br>
Risk: If REPORT_WEBHOOK_URL is set, the generated report is sent to that configured endpoint. <br>
Mitigation: Leave REPORT_WEBHOOK_URL unset unless webhook delivery is required; use HTTPS and avoid internal or untrusted webhook destinations. <br>
Risk: The skill writes generated report files to the local reports directory. <br>
Mitigation: Run it in a workspace where generated report files are expected and can be reviewed or cleaned up. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HubertSing/conan-weekly-report) <br>
- [README](README.md) <br>
- [Skill documentation](SKILL.md) <br>
- [Bilibili Detective Conan media page](https://www.bilibili.com/bangumi/media/md2819) <br>
- [Baidu Baike Detective Conan page](https://baike.baidu.com/item/名侦探柯南/3469662) <br>
- [Wikipedia Detective Conan page](https://zh.wikipedia.org/wiki/名侦探柯南) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, files] <br>
**Output Format:** [Markdown report saved as conan-report-YYYY-MM-DD.md, console text, and optional JSON webhook body containing the report text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are written under reports/; optional webhook delivery is controlled by REPORT_WEBHOOK_URL.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
