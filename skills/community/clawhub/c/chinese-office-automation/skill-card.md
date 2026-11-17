## Description:

中文办公自动化 - 专为中文用户设计的办公自动化技能套件。集成中文文档处理、拼音转换、节假日判断、农历支持等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijie298](https://clawhub.ai/user/lijie298)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking employees, external users, and developers use this skill to guide office automation workflows for Chinese document processing, date handling, pinyin conversion, financial formatting, and common office templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python dependency versions for zhdate, pypinyin, and opencc may affect behavior or introduce dependency risk.

Mitigation: Install dependencies in an isolated environment and pin reviewed versions before operational use.

Risk: Locale settings may make the agent assume simplified Chinese output, Asia/Shanghai time, and mainland China holiday calendars.

Mitigation: Review the TOOLS.md locale settings before applying them to workflows for other regions, scripts, or calendar policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijie298/skills/chinese-office-automation)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are oriented toward simplified Chinese office automation workflows using Python 3 and optional Chinese-language processing dependencies.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
