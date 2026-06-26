## Description: <br>
Helps agents turn systems, workflows, and data structures into structured diagrams such as architecture diagrams, flowcharts, sequence diagrams, state machines, ER diagrams, topology diagrams, and data-flow diagrams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, analysts, and other external users use this skill to select an appropriate diagram type, extract entities and relationships, choose visual encodings, and produce renderable SVG or Mermaid diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may trigger on broad diagram-related terms such as draw or architecture when the user intended a different workflow. <br>
Mitigation: Invoke another skill explicitly when diagram-focused output is not desired. <br>
Risk: Generated diagrams can reflect incomplete or sensitive user-provided information. <br>
Mitigation: Review entity selection, relationships, and labels before use; redact sensitive information before rendering or sharing diagrams. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/diagram-workflow-method) <br>
- [Publisher profile](https://clawhub.ai/user/wangjiaocheng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with SVG or Mermaid code blocks when diagram output is requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include entity and relationship tables, encoding plans, layout coordinates, validation checklists, SVG markup, or Mermaid diagram code.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
