## Description: <br>
Generates Chinese API documentation from code, OpenAPI/Swagger specs, or endpoint descriptions, with terminology guidance, examples, error-code tables, authentication sections, and optional backend validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to draft natural Chinese API reference documentation from OpenAPI/Swagger specs, source code, or endpoint descriptions. It helps standardize terminology, request and response examples, authentication notes, error-code tables, rate-limit sections, and update logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External validation may receive sensitive API specifications, source code, internal endpoint details, authentication flows, tokens, or production examples. <br>
Mitigation: Use the skill for non-confidential documentation unless the validation service is explicitly trusted; remove secrets and internal details before running validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lm203688/chinese-api-docs) <br>
- [Validation API base URL](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown documentation with tables, JSON examples, and optional shell validation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Chinese terminology mappings, generated request and response examples, error-code tables, and authentication or rate-limit guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
