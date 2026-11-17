## Description:

Operate ClawTime - webchat widgets, task panel, and avatar creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youngkent](https://clawhub.ai/user/youngkent)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to operate ClawTime, including service checks, widget response markup, task panel maintenance, and Three.js avatar creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to restart a user-level ClawTime service and modify persistent ClawTime task, config, and avatar files.

Mitigation: Review proposed service commands and file changes before execution, and limit writes to intended ClawTime paths.

Risk: Custom avatar JavaScript can affect the ClawTime frontend when installed.

Mitigation: Review custom avatar JavaScript before use.

Risk: The skill lists credential and session file paths that may contain sensitive local data.

Mitigation: Do not inspect credential or session files unless the user explicitly intends that access.

## Reference(s):

- [ClawTime ClawHub skill page](https://clawhub.ai/youngkent/skills/clawtime)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with widget markup, code blocks, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local ClawTime service commands and persistent ClawTime configuration, task, and avatar files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
