## Description: <br>
Parse natural language descriptions and output diagram scheme recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zatanyong](https://clawhub.ai/user/zatanyong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and external users use this skill to classify visualization requests and choose an appropriate Mermaid diagram, ECharts chart template, or image prompt fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can recommend a diagram format or chart template that does not fit the user's data or rendering environment. <br>
Mitigation: Review the recommended primary type and alternatives against the actual data, Mermaid version, ECharts support, and allowed diagram constraints before rendering. <br>
Risk: Users may expect direct Feishu integration or automatic chart rendering even though the security guidance says the skill provides guidance and structured output only. <br>
Mitigation: Treat the output as a diagram-planning recommendation and use a separate renderer or Feishu workflow to create the final visual artifact. <br>
Risk: Generated Mermaid code, ECharts configuration, or image prompts may be incomplete or misleading for ambiguous visualization requests. <br>
Mitigation: Use the clarification questions when confidence is low and validate generated code or configuration in the target rendering environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zatanyong/feishu-diagram-chooser) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, code, configuration] <br>
**Output Format:** [Structured DiagramScheme object with recommendation text, optional Mermaid code, ECharts chart configuration, or image prompt.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a primary recommendation, ordered alternatives, confidence score, and clarification questions when intent is ambiguous.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
