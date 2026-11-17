## Description:

ClawMate helps agents manage local projects through file search and preview links, feedback handling, project initialization, and phased planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[updatedb](https://clawhub.ai/user/updatedb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use ClawMate to search and preview managed project files, handle feedback loops, initialize project workspaces, and maintain phase-based planning documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable ClawMate service URL could send project paths, notes, or selected file content outside the intended local environment.

Mitigation: Use only a trusted local ClawMate service by default and keep CLAWMATE_URL on localhost unless remote transmission is intentional and approved.

Risk: Unsafe shell command templates can run unintended commands when project data or feedback content is interpolated without proper encoding.

Mitigation: Construct requests with proper JSON and URL serialization, and review generated shell commands before execution.

Risk: Initialization and feedback-handling workflows can modify files, directories, and Git state.

Mitigation: Require clear user confirmation before init or do operations and show the target paths before making changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/updatedb/skills/clawmate)
- [ClawHub publisher profile](https://clawhub.ai/user/updatedb)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, local API request examples, project document templates, and preview links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce file paths, project plans, feedback summaries, and local-service request examples.]

## Skill Version(s):

2.9.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
