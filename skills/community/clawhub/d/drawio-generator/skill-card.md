## Description: <br>
Generate draw.io diagrams from Mermaid, XML, or CSV code and create a markdown link that opens the diagram in draw.io. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Thincher](https://clawhub.ai/user/Thincher) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and other users can use this skill to turn Mermaid, draw.io XML, or CSV diagram definitions into editable diagrams opened through diagrams.net. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram content is encoded into a generated diagrams.net link, which can expose secrets, credentials, private network details, or sensitive internal architecture if shared or opened through the external service. <br>
Mitigation: Do not include sensitive content unless the user is comfortable opening it through diagrams.net and sharing it in the generated link. <br>
Risk: Malformed draw.io XML can fail to render or open correctly. <br>
Mitigation: Ensure XML is well formed, avoid double hyphens inside XML comments, and escape special characters in attribute values before generating the link. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Thincher/drawio-generator) <br>
- [diagrams.net app](https://app.diagrams.net/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown link with a diagrams.net URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated URL encodes the provided Mermaid, XML, or CSV diagram content for opening in diagrams.net.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
