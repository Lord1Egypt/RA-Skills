## Description: <br>
Search Feishu contacts by name/pinyin/department. Use when you need to find a person's open_id, email, or department info before sending messages or emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guyun94](https://clawhub.ai/user/guyun94) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and agent operators use this skill to locate Feishu users and departments before sending messages, emails, or department-wide communications. It helps resolve names to open_id, email, department, and membership details through a local cache and live Feishu API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles and stores broad employee directory data in a local cache. <br>
Mitigation: Use only with an authorized Feishu app, confirm that local storage of employee directory data is acceptable, and document how the cache is stored, reviewed, and deleted. <br>
Risk: The required Feishu permissions can expose user, detailed user, and department information. <br>
Mitigation: Scope the Feishu app to the minimum directory access needed and review the configured permissions before installation. <br>
Risk: Command output may print personal contact details such as email, mobile number, open_id, and department membership. <br>
Mitigation: Review outputs before sharing them and avoid pasting contact details into channels that are not approved for employee directory data. <br>


## Reference(s): <br>
- [Feishu Open API](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown guidance with shell commands and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results can include employee names, open_id values, emails, departments, phone numbers, and local cache metadata.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
