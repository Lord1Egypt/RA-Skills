## Description:

Generate draw.io diagrams from Mermaid, XML, or CSV code and return a markdown link that opens the diagram in draw.io.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizha](https://clawhub.ai/user/qizha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and other diagram authors use this skill to turn Mermaid, XML, or CSV diagram text into an editable diagrams.net link for flowcharts, UML, ERD, architecture, organization, network, wireframe, BPMN, and similar diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opening a generated link sends the diagram content to app.diagrams.net in the browser.

Mitigation: Avoid placing sensitive information in generated diagrams unless the user is comfortable using the external diagrams.net service.

Risk: Invalid draw.io XML can prevent the generated diagram from opening correctly.

Mitigation: Ensure XML is well formed, avoid double hyphens in XML comments, and escape special characters in XML attribute values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qizha/skills/drawio-generator-bak)
- [diagrams.net editor](https://app.diagrams.net/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown link to a diagrams.net URL, with optional diagram source code and command-line invocation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated link encodes Mermaid, XML, or CSV diagram content for opening in app.diagrams.net.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
