## Description: <br>
Guides Chinese-language conversion of business workflow descriptions into Colored Petri Net models, including structured model data, CPN Tools XML, and local HTML visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theosunny](https://clawhub.ai/user/theosunny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and workflow designers use this skill to turn natural-language business processes into CPN/Petri-net models for scenarios such as approvals, e-commerce orders, restaurant ordering, engineering steps, and hospital workflows. It can also guide users who do not know CPN terminology by asking business-language questions before generating the model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate for broad workflow-modeling prompts. <br>
Mitigation: Use it when CPN/Petri-net workflow modeling is intended, and review generated models before relying on them. <br>
Risk: The skill can create a local /tmp HTML visualization file containing browser JavaScript. <br>
Mitigation: Open generated HTML only when that output is expected and clean up temporary visualization files after use. <br>
Risk: Incorrect dependency, guard, or token modeling can produce misleading or deadlocked CPN models. <br>
Mitigation: Review dependency rules, initial markings, resource places, and generated visualizations before importing or using the model. <br>


## Reference(s): <br>
- [CPN Modeling Skill ClawHub Page](https://clawhub.ai/theosunny/cpn-modeling) <br>
- [README](README.md) <br>
- [CPN Modeling Guide](references/modeling-guide.md) <br>
- [CPN JSON Schema Reference](references/json-schema.md) <br>
- [CPN Tools XML Template Reference](references/cpn-xml-template.md) <br>
- [HTML Visualization Template Reference](references/html-viz-template.md) <br>
- [Restaurant Workflow Example](references/example-restaurant.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown responses with JSON model data, CPN Tools XML, shell commands, and generated local HTML visualization files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local /tmp HTML visualization file containing browser JavaScript when visualization output is requested.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
