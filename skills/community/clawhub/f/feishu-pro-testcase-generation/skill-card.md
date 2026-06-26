## Description: <br>
Converts requirement documents, form-field rules, approval workflow definitions, and UI notes into structured test cases for validation, approvals, state transitions, permission boundaries, and business branches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lens-lzy](https://clawhub.ai/user/Lens-lzy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, product teams, and developers use this skill to turn PRDs, form rules, workflow definitions, state machines, roles, permissions, and UI behavior into reviewable Markdown test scenarios and executable test cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated test cases may reflect omissions or ambiguity in the user's requirements. <br>
Mitigation: Review the Markdown tables and resolve the generated requirement-confirmation questions before using the cases for release decisions. <br>
Risk: User-provided PRDs, workflow definitions, screenshots, and business rules may contain proprietary information. <br>
Mitigation: Use normal data-handling controls and avoid exporting to Feishu, cloud storage, or local files unless the destination is approved. <br>
Risk: Optional export behavior can place generated content outside the chat context if the user explicitly requests it and tools are available. <br>
Mitigation: Confirm the target document, cloud folder, or file path before export and do not treat unsupported tool calls as completed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lens-lzy/feishu-pro-testcase-generation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown tables with scenario overviews, test case details, and requirement-confirmation questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May optionally propose Feishu, cloud-drive, or local-file export only when the environment provides those tools and the user requests export.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
