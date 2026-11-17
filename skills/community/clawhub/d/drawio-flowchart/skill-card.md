## Description:

Generate draw.io (.drawio) flowchart XML files for flowcharts, process diagrams, workflow diagrams, and visual diagrams in diagrams.net format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiningo](https://clawhub.ai/user/zhiningo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill when they need an agent to create clean, structured draw.io flowchart files with swimlane containers, text hierarchy, color coding, and orthogonal arrow routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes local .drawio files, so an unintended filename or path could place output in the wrong location.

Mitigation: Review the requested output path before saving and keep generated files in the workspace or an explicit user-selected path.

Risk: Some artifact examples use Chinese labels and instructions, which may not match every user's expected language.

Mitigation: Use the user's requested language for diagram labels and response text, or ask for a preferred language when it is unclear.

## Reference(s):

- [XML Template](references/template.md)
- [diagrams.net](https://app.diagrams.net)
- [ClawHub skill page](https://clawhub.ai/zhiningo/skills/drawio-flowchart)
- [AgentSkills](https://agentskills.io)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Guidance]

**Output Format:** [Markdown guidance with draw.io XML saved as a .drawio file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local .drawio XML files and opening instructions for diagrams.net-compatible tools.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
