## Description:

桌面自动驾驶为 AI Agent 提供基于视觉的桌面 GUI 自动化指导，覆盖图像匹配、OCR 文本定位、智能等待、工作流编排、录制回放、DPI 自适应与多显示器支持。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to guide desktop GUI automation workflows such as form filling, data entry, UI regression checks, and cross-application data transfer with visual verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate destructive GUI actions such as deletes, submissions, or bulk workflows.

Mitigation: Use explicit per-task approval and avoid running destructive or bulk workflows without manual confirmation.

Risk: Operation logs may persist typed user data in plain text.

Mitigation: Treat logs as sensitive, restrict access to them, and review or redact logged data before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/desktop-autopilot)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose GUI automation actions that should be reviewed before execution.]

## Skill Version(s):

1.0.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
