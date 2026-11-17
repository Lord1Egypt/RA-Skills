## Description:

从自然语言描述生成 Excel 公式并诊断常见表格错误，包括 VLOOKUP、条件求和和日期处理等函数问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Personal users, developers, and business teams can use this skill to turn spreadsheet requests into Excel formulas and receive formula debugging, function conversion, and common table-processing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution and broad read access for a task that is primarily formula assistance.

Mitigation: Install only in an agent environment where tool access can be reviewed, restricted, and approved for spreadsheet-related work.

Risk: The artifact describes file, API, and command behavior beyond ordinary Excel formula generation.

Mitigation: Review requested actions before execution and avoid granting unnecessary filesystem, network, or shell permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/excel-formula-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks, Excel formula examples, and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include formula snippets, troubleshooting steps, configuration examples, and command suggestions when the agent has tool access.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
