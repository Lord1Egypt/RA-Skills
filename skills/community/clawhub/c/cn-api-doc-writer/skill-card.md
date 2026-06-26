## Description: <br>
Generates professional Chinese API documentation from code, OpenAPI/Swagger specifications, or endpoint descriptions, with terminology guidance, examples, error tables, authentication notes, rate limiting sections, and optional validation support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to create or convert API reference documentation into natural Chinese for Chinese developer audiences. It supports OpenAPI/Swagger specs, source-code-derived endpoint descriptions, and plain-language endpoint descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan marks the release suspicious because it advertises an external validation service and includes an executable validation script without clear data-handling guidance. <br>
Mitigation: Install only after confirming the operator and data-handling terms; avoid sending private OpenAPI specs, internal source-derived documentation, tokens, authentication examples, or unreleased API details to the external service. <br>
Risk: The skill is in maintenance mode and states that it will not receive feature updates. <br>
Mitigation: Review generated documentation before publication and use maintained alternatives for compliance-focused checks as suggested by the skill text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lm203688/cn-api-doc-writer) <br>
- [External validation API base URL](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown with API documentation sections, tables, JSON examples, and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese API documentation may include generated request and response examples, error code tables, authentication guidance, terminology mappings, and validation notes.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
