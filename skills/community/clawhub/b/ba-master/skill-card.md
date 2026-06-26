## Description: <br>
Ba Master turns ambiguous product or system ideas into structured business-analysis deliverables across requirements specifications, process models, data dictionaries, user stories, UI view specifications, and compliance reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo21cn](https://clawhub.ai/user/leo21cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product owners, business analysts, and delivery teams use this skill to clarify early-stage business needs and turn them into structured requirements assets. It is suited for requirements elicitation, business process modeling, data dictionary creation, user story writing, UI view specification, and compliance review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes a reusable bearer token. <br>
Mitigation: Rotate the exposed token and require users or administrators to configure credentials outside the packaged skill. <br>
Risk: Requirements, compliance details, prompts, context, conversation IDs, and path strings may be sent to an external MCP service. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and document the service's data handling and consent expectations before broad deployment. <br>
Risk: Security evidence classifies the release as suspicious. <br>
Mitigation: Review the publisher guidance and scan results before installation, and treat the skill as higher-risk until the credential and data-handling issues are resolved. <br>


## Reference(s): <br>
- [Ba Master on ClawHub](https://clawhub.ai/leo21cn/ba-master) <br>
- [leo21cn publisher profile](https://clawhub.ai/user/leo21cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text documents, often with structured tables and Mermaid diagrams.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are staged through remote MCP tool calls and may include progress prompts for user confirmation or continuation.] <br>

## Skill Version(s): <br>
1.8.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
