## Description:

Generate draw.io diagrams from Mermaid, XML, or CSV code and create a markdown link that opens the diagram in draw.io.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thincher](https://clawhub.ai/user/thincher)

### License/Terms of Use:


## Use Case:

Developers, engineers, and other diagram authors use this skill to turn Mermaid, XML, or CSV diagram definitions into editable draw.io links for visual documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented command-line workflow can turn untrusted diagram text into shell command execution if followed literally.

Mitigation: Review before installing and change invocation patterns so diagram text is passed through stdin, a temporary file, or a shell-free argument-array call.

Risk: The generated output link text is localized, which may be unclear to readers expecting neutral English labels.

Mitigation: Consider replacing the output link label with neutral localized text appropriate for the release audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thincher/skills/drawio-generator)
- [Publisher profile](https://clawhub.ai/user/thincher)
- [diagrams.net editor](https://app.diagrams.net/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown link to a generated draw.io URL, with supporting diagram code and command guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Mermaid, draw.io XML, and CSV diagram inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
