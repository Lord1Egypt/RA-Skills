## Description:

Desktop Automation Hub Pro guides agents through desktop automation workflows using image recognition, multi-monitor coordination, window control, approval gates, and performance-oriented batching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation engineers, QA teams, and operations users can use this skill to plan and run GUI automation, RPA-style workflows, multi-monitor screen tasks, desktop screenshots, and guarded keyboard or mouse actions. It is not intended for tasks that require human creative judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact desktop actions across files, screens, terminals, and applications.

Mitigation: Use approval mode by default, restrict accessible files and applications, keep failsafe controls enabled, and avoid production terminals unless the action has been reviewed.

Risk: Automated clicks, typing, hotkeys, and batch operations can perform unintended actions when screen state or coordinates are wrong.

Mitigation: Require human approval for click, drag, type, and hotkey actions; prefer image confirmation before action; and keep operation logs for review.

Risk: Screen, clipboard, callback, or API content can expose sensitive data.

Mitigation: Avoid credential entry and sensitive clipboard content, disable external callbacks unless needed, use HTTPS for any integrations, and redact sensitive output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/desktop-automation-hub-pro)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include desktop automation steps, dependency setup commands, approval-mode recommendations, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
