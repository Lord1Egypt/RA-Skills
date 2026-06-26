## Description: <br>
从淄博公共资源交易网站收集指定日期范围内的招标公告和中标公示，并将项目地点、项目名称和发布时间整理为 Excel 文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n1ke9yd](https://clawhub.ai/user/n1ke9yd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect public resource trading project listings from the Zibo site for a chosen date range and export the results for review or reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write Excel files locally, so an existing target file could be overwritten. <br>
Mitigation: Use a trusted output path and check whether the target file already exists before generating or overwriting the workbook. <br>
Risk: Collected listings may be incomplete or inaccurate if page navigation, loading, or date filtering is not checked. <br>
Mitigation: Review the collected project rows and publication dates before relying on the exported Excel file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/n1ke9yd/ggzy-collect) <br>
- [Zibo public resource trading site](http://ggzyjy.zibo.gov.cn:8082/) <br>
- [Zibo construction project listings](http://ggzyjy.zibo.gov.cn:8082/jyxx/002001/gonggongziyuan.html?Paging=1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, files] <br>
**Output Format:** [Markdown guidance with JavaScript/Node.js snippets and Excel workbook files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local .xlsx files to a user-specified path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
