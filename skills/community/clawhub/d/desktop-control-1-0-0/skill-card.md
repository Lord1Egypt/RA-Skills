## Description:

Advanced desktop automation with mouse, keyboard, and screen control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpegley](https://clawhub.ai/user/wpegley)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to let an agent control a desktop through mouse and keyboard actions, screenshots, clipboard operations, window management, and simple autonomous workflows such as drawing, app launch, and text entry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control the live desktop, including clicks, typing, window activation, and other actions that may affect active applications.

Mitigation: Use it in a non-admin session, keep failsafe enabled, enable approval mode for sensitive workflows, and manually review irreversible submissions before execution.

Risk: The skill can capture screen content and read or write clipboard text.

Mitigation: Avoid sensitive screens and clipboard contents, do not use it for passwords, and clear or isolate sensitive data before running automation.

Risk: The security evidence says the approval and safety controls are incomplete.

Mitigation: Run the skill only when you can monitor actions, prefer a constrained desktop session, and stop execution immediately if behavior diverges from the intended task.

Risk: The documented install flow uses desktop automation dependencies whose installed versions may vary by environment.

Mitigation: Install in an isolated virtual environment and pin dependencies before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpegley/skills/desktop-control-1-0-0)
- [Desktop Control Skill documentation](artifact/SKILL.md)
- [AI Desktop Agent guide](artifact/AI_AGENT_GUIDE.md)
- [Desktop Control quick reference](artifact/QUICK_REFERENCE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke live desktop actions and collect screenshots or clipboard text when used in an enabled desktop environment.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
