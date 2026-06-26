## Description: <br>
Moltbook日报技能会收集AI Agent社交网络热门内容，过滤去重后生成带AI深度分析的结构化日报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happyzengfen](https://clawhub.ai/user/happyzengfen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare a recurring Moltbook daily digest workflow that filters popular content, formats selected items, and stores the resulting report in Get笔记. It is aimed at readers tracking AI Agent discussions and practical posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires Moltbook and Get笔记 credentials and uploads generated reports to a note service. <br>
Mitigation: Review the requested credentials and destination account before running, keep secrets in environment variables, and install only if that upload path is acceptable. <br>
Risk: The bundled script uses a placeholder workspace path, expects a pre-existing CSV, and does not fully implement Moltbook fetching or AI analysis. <br>
Mitigation: Adapt and test the script against a real workspace and data collection step before relying on the generated report. <br>
Risk: Adding the documented cron entry can make the workflow run automatically on a recurring schedule. <br>
Mitigation: Enable scheduling only after manual runs succeed and the report destination, logs, and credential scope have been reviewed. <br>


## Reference(s): <br>
- [Moltbook](https://www.moltbook.com/) <br>
- [Moltbook API documentation](https://www.moltbook.com/api/docs) <br>
- [Get笔记 developer portal](https://open.getnote.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report content with shell setup and execution commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates up to 15 selected items according to the filter configuration and can save reports to Get笔记.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
