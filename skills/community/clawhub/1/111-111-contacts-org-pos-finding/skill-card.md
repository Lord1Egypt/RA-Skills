## Description:

通过111通讯录按机构路径和职位名称查询人员信息，需先确认提供机构和职位名称后执行。

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockcloud](https://clawhub.ai/user/blockcloud)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized internal users use this skill to look up personnel in the 111 address book by organization path and job title after confirming the query details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive employee directory details such as names, employee IDs, desk phones, and mobile numbers.

Mitigation: Use only for authorized lookups in the referenced OA address book and share returned contact details only within the approved business context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blockcloud/skills/111-111-contacts-org-pos-finding)
- [Publisher profile](https://clawhub.ai/user/blockcloud)
- [111 address book login](https://oa.paas.111china.com/address-book/login)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Delimited text lines, or a concise no-result explanation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each matching row may include organization, position, employee ID, 111ID, name, desk phone, and mobile phone.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
