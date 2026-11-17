## Description:

智能 Web UI 测试工作台，支持 MCP 直接驱动和 Python 脚本驱动双模式，三种测试模式，强制人工确认，安全可控。

This skill is ready for commercial/non-commercial use.

## Publisher:

[millerallen98](https://clawhub.ai/user/millerallen98)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to plan and run Web UI tests through MCP-driven browser control or generated Python Playwright scripts. It supports exploratory, requirement-driven, and test-case-driven workflows with user confirmation before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests filesystem, terminal, and browser-control access that can affect local files and visited web applications.

Mitigation: Grant access only in an isolated workspace, use disposable browser sessions, and review generated scripts before approving execution.

Risk: Automated login handling and test reports may expose credentials, session data, screenshots, or page content.

Mitigation: Use disposable test accounts, avoid real passwords, and review generated scripts, screenshots, logs, and reports before sharing or committing them.

Risk: The README configures Playwright MCP with a floating latest dependency, which may change behavior over time.

Mitigation: Pin the Playwright MCP dependency to a reviewed version before use in controlled or production-like environments.

## Reference(s):

- [Flexible Web Tester ClawHub Listing](https://clawhub.ai/millerallen98/skills/flexible-web-tester)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, Python code, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated test plans, Python scripts, screenshots, logs, and Markdown reports to the working directory.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
