## Description:

Quick start templates for OpenClaw agents, including boilerplate for research bots, content generators, task automation, and related starter projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to list and create starter OpenClaw agent projects for research, content generation, and task automation. It produces files and setup guidance that can be customized before running the generated agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated research bot uses shell commands with research topics supplied by the user.

Mitigation: Review before installing, avoid untrusted research topics, and update the generated research helper to pass arguments without shell interpolation.

Risk: The generated research bot automatically saves research topics to memory.

Mitigation: Require user confirmation before saving research topics and run the skill only in a disposable or intended new project directory.

Risk: Installing with an unpinned package command can change behavior over time.

Mitigation: Prefer a version-pinned install command for reproducible installation.

## Reference(s):

- [Agent Quick Start ClawHub listing](https://clawhub.ai/yang1002378395-cmyk/skills/agent-quick-start)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Generated project files with Markdown instructions and JavaScript helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Template selection and target project path determine the generated files.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
