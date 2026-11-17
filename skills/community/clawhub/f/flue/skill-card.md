## Description:

Let agents control software, including Adobe Photoshop, Illustrator, After Effects, Premiere, Autodesk 3DS Max, Blender, Unity, Houdini, and Microsoft Office.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sfkislev](https://clawhub.ai/user/sfkislev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Flue to let an agent inspect live state and make bounded, user-directed edits inside supported desktop applications. It is intended for creative, technical, game-development, and office-document workflows where the user has explicitly requested work in a specific application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flue can execute user-provided scripts inside professional desktop applications, so unintended or destructive changes could affect open documents, scenes, or projects.

Mitigation: Use Flue only for explicit, user-requested tasks in a specific application, prefer small inspectable steps, and avoid destructive actions unless the user approves them.

Risk: Installation and setup add desktop application integrations on the user's machine.

Mitigation: Inspect the linked Flue project first, pin a reviewed version or use isolation when appropriate, and run installation or setup only after explicit current-session approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sfkislev/skills/flue)
- [Flue GitHub Project](https://github.com/SFKislev/flue)
- [Flue on PyPI](https://pypi.org/project/flue)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and code examples; bridge results are structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before installation, setup, or destructive desktop-application actions.]

## Skill Version(s):

1.0.18 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
