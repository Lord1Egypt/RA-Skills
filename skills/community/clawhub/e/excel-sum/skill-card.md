## Description:

计算 Excel 文件第一列数值的总和，并在用户请求 Excel 第一列求和或统计时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujialin1517-source](https://clawhub.ai/user/liujialin1517-source)

### License/Terms of Use:

MIT-0

## Use Case:

外部用户和开发者可在需要快速汇总 Excel 工作簿第一列数值时使用此技能；代理会请求文件路径并返回总和、参与求和的单元格数量以及跳过的非数值单元格数量。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The openpyxl dependency is not pinned in the artifact, which can make dependency review and repeatable installation harder.

Mitigation: Install the skill in a virtual environment and pin openpyxl to a reviewed version before deployment.

Risk: The instructions and script output are Chinese-only, which can reduce reviewer comprehension for users who do not read Chinese.

Mitigation: Have a Chinese-reading reviewer or trusted translation review the behavior before use in non-Chinese-language workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liujialin1517-source/skills/excel-sum)
- [Publisher profile](https://clawhub.ai/user/liujialin1517-source)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with an optional shell command and numeric result summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the first-column sum, count of numeric cells included, and count of skipped cells.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
