## Description: <br>
学术人员邮箱批量搜索工具 helps an agent search for academic email addresses from names and institutions, then write the results back to an Excel spreadsheet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to enrich spreadsheets of academic people by searching public web sources for likely email addresses from each person's name and institution. Results require manual review before reliance, especially for common names or ambiguous institutional matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes lists of people and searches for contact details, which can create privacy and permission concerns. <br>
Mitigation: Confirm that the user is allowed to process and search the people list before running the workflow. <br>
Risk: Search results can match the wrong person when names are common or institution data is incomplete. <br>
Mitigation: Manually review matches before relying on the filled addresses, with extra scrutiny for ambiguous names. <br>
Risk: The Excel write step can overwrite existing spreadsheet data. <br>
Mitigation: Run the workflow on a copy of the spreadsheet and verify the target email column before saving results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chaoliuzhu/academic-email-finder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Python code snippets and spreadsheet file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or overwrite an Excel workbook column containing found email addresses or "未找到" for missing results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
