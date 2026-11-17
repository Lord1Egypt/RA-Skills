## Description:

Builds editable cloud architecture diagrams for Azure/Microsoft, AWS, GCP, and Microsoft Fabric from text descriptions or screenshots, using vendor icons and exporting Excalidraw and draw.io files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hansraj316](https://clawhub.ai/user/hansraj316)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and solutions architects use this skill to turn cloud architecture descriptions or reference screenshots into editable Excalidraw and draw.io diagrams with embedded service icons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote icon URLs in diagram specs may fetch from unintended local or internal resources.

Mitigation: Use bundled offline icons and allow only trusted, reviewed icon_url values.

Risk: Icon-pack import or refresh commands can replace bundled provider icon directories when run with untrusted source or provider values.

Mitigation: Run maintenance commands only in a disposable or version-controlled copy and review the source path and provider before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hansraj316/skills/cloud-architecture-diagrams)
- [Spec format and layout cookbook](references/spec-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with JSON diagram specs and generated .excalidraw JSON plus .drawio XML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; generated diagram files embed icons for offline editing.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
