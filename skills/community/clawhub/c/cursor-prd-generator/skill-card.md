## Description: <br>
Generates a Chinese PRD workflow for small feature requests by clarifying scope, target users, success criteria, and boundaries, then producing FEATURE_SPEC.md content and a Cursor rules snippet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2025biophilia-coder](https://clawhub.ai/user/2025biophilia-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product builders use this skill to turn a small, bounded feature idea into a structured PRD and Cursor agent rules after sequential clarification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad PRD, feature, or publish wording may activate the skill unexpectedly. <br>
Mitigation: Confirm the user wants a small-feature PRD workflow and narrow the scope before generating artifacts. <br>
Risk: Generated PRD and Cursor rules can introduce incorrect requirements if accepted without review. <br>
Mitigation: Review the generated FEATURE_SPEC.md and .cursor/rules content before using it in a project or uploading it elsewhere. <br>
Risk: Publishing workflows may require credentials such as TAI_PAT_TOKEN. <br>
Mitigation: Configure publishing credentials only when intentionally publishing, and avoid including secrets in generated documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2025biophilia-coder/cursor-prd-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown containing FEATURE_SPEC.md content and a .cursor/rules snippet separated by a divider.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Simplified Chinese by default; requires sequential clarification before generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
