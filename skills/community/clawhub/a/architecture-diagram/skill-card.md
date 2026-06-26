## Description: <br>
Generates Mermaid architecture diagrams for systems, cloud platforms, AI and neural network designs, graph theory, flowcharts, ER diagrams, network topology, and Docker or Kubernetes architectures, with optional image rendering through Kroki. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, and technical teams use this skill to draft architecture diagrams as Mermaid code and optionally render them as PNG, SVG, or PDF files for sharing and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive architecture details may be sent to an external rendering service when using Kroki or mermaid.live. <br>
Mitigation: Do not send secrets, private network topology, internal hostnames, account IDs, or confidential architecture details to external renderers; use Mermaid code output or a local/internal renderer for sensitive work. <br>
Risk: Generated architecture diagrams may omit important system details or misrepresent the intended design. <br>
Mitigation: Review generated diagrams with the system owner before using them in implementation, operations, or security reviews. <br>


## Reference(s): <br>
- [ClawHub Architecture Diagram skill page](https://clawhub.ai/smseow001/architecture-diagram) <br>
- [Kroki diagram rendering service](https://kroki.io) <br>
- [Mermaid Live editor](https://mermaid.live/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands] <br>
**Output Format:** [Markdown with Mermaid code blocks, renderer URLs, and optional generated diagram files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce Mermaid source and rendered image files; external rendering should be avoided for confidential diagrams.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
