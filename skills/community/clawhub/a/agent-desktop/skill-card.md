## Description:

Guides agents in observing and operating macOS and Windows desktop applications through accessibility-based desktop commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lahfir](https://clawhub.ai/user/lahfir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other desktop users use this skill to guide an agent through observing interfaces and completing tasks in macOS or Windows applications, including forms, navigation, and window management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad desktop control can change applications or documents unintentionally.

Mitigation: Scope tasks to named applications or windows and verify the interface after each action.

Risk: Screenshots and UI inspection can expose passwords or private content.

Mitigation: Avoid sensitive screens and grant operating-system access only when needed.

Risk: Recorded screenshots and desktop traces may persist after a task.

Mitigation: End sessions and clean up traces when finished, especially when screenshots were recorded.

## Reference(s):

- [agent-desktop on ClawHub](https://clawhub.ai/lahfir/skills/agent-desktop)
- [Observation commands](references/commands-observation.md)
- [Interaction commands](references/commands-interaction.md)
- [System commands](references/commands-system.md)
- [Common workflows](references/workflows.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline commands and structured UI observations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include accessibility snapshots, action results, and screenshots when requested.]

## Skill Version(s):

0.1.33 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
