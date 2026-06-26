## Description: <br>
输入中文关键词后，生成中英双语关键词与文献检索结果表：中文来源知网、英文来源Google Scholar，近10年、相关性排序、按年份降序输出标准Markdown表格；优先可见浏览器人工验证。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huixiaheyu](https://clawhub.ai/user/huixiaheyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to turn Chinese research keywords into bilingual search terms and a verified literature-results table from CNKI and Google Scholar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to CNKI and Google Scholar during browser-based literature searches. <br>
Mitigation: Avoid confidential or restricted queries unless those external services are approved for the intended use. <br>
Risk: The browser workflow can leave a debug-enabled Chrome session or temporary profile on the local machine. <br>
Mitigation: Close the Chrome session and remove the temporary profile after use when local browsing state should not persist. <br>
Risk: CAPTCHAs, blocked pages, or missing metadata can make search results incomplete. <br>
Mitigation: Pause for user verification when prompted and keep unverifiable fields blank rather than filling them from assumptions. <br>


## Reference(s): <br>
- [CNKI Search](https://kns.cnki.net/kns8s/search) <br>
- [Google Scholar](https://scholar.google.com/scholar) <br>
- [ClawHub skill page](https://clawhub.ai/huixiaheyu/field-research) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown table with bilingual keyword text and optional browser workflow prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are sorted by publication year in descending order, with unknown or unverifiable fields left blank or marked with '-'.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
