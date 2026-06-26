## Description: <br>
通过111通讯录按机构路径和职位名称查询人员信息，并在用户确认输入后返回匹配人员的联系字段。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blockcloud](https://clawhub.ai/user/blockcloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized employees or agents use this skill to query the 111 OA address book by organization path and position title after confirming the requested inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can return employee contact details from an internal address book. <br>
Mitigation: Install and use it only when authorized to access the 111 OA directory, keep results within approved internal channels, and review returned fields before sharing. <br>
Risk: Broad or imprecise organization and position inputs can return irrelevant or unintended people records. <br>
Mitigation: Use precise organization paths and position names, and confirm the requested inputs before querying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blockcloud/111-111-contacts-org-pos-finding) <br>
- [111 OA address book login](https://oa.paas.111china.com/address-book/login) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown text with comma-separated result rows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Rows may include organization, position, employee number, 111ID, name, desk phone, and mobile phone when authorized results are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
