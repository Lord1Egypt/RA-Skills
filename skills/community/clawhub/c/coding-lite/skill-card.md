## Description:

轻量级编码助手，支持 Python 脚本生成与执行、Excel/WPS 函数自动化、小程序代码生成、SQL 查询助手。快速响应，不占用过多 context。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill for quick, lightweight code generation and automation support in Python, Excel/WPS formulas, mini program scaffolding, and SQL queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scripts or shell commands may modify files, install packages, or run in an unsafe local environment.

Mitigation: Review commands before execution, run unfamiliar code in a sandbox or virtual environment, and back up data before file operations.

Risk: SQL UPDATE, DELETE, macro, or spreadsheet automation guidance can change or delete user data.

Mitigation: Inspect generated statements and macros, require explicit confirmation for destructive actions, and test against copies or transactions first.

Risk: Generated scraping or API examples may be inappropriate for a target service or data source.

Mitigation: Check service terms, credentials handling, rate limits, and data permissions before running generated scraping or API code.

## Reference(s):

- [Coding Lite ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/coding-lite)
- [cp3d1455926-svg publisher profile](https://clawhub.ai/user/cp3d1455926-svg)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated code, SQL, macros, and commands should be reviewed before execution; production-critical use requires separate testing.]

## Skill Version(s):

1.0.0 (source: server release metadata and README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
