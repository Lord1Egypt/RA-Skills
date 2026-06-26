## Description: <br>
Discover and submit to FormPass-enabled web forms. FormPass is the trust layer that lets verified AI agents submit to real web forms with authenticated identity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jezjsa](https://clawhub.ai/user/jezjsa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to detect FormPass-enabled web forms, fetch their structured schemas, and submit JSON form data with an optional FormPass Agent ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Form submissions may send user-provided data and an optional Agent ID to FormPass. <br>
Mitigation: Confirm the destination form, review the payload before submission, and avoid secrets or regulated data unless the user has approved that use. <br>
Risk: A form owner may disable agent submissions. <br>
Mitigation: Fetch the schema first and do not submit when the schema reports agentAccessible as false. <br>
Risk: Branding-required forms can reject submissions that omit the required FormPass branding field. <br>
Mitigation: Include _fp_branding: true when the fetched schema indicates branding.required is true. <br>


## Reference(s): <br>
- [FormPass homepage](https://form-pass.com) <br>
- [FormPass discovery JSON](https://form-pass.com/formpass.json) <br>
- [FormPass LLM guide](https://form-pass.com/llms.txt) <br>
- [ClawHub skill page](https://clawhub.ai/jezjsa/formpass-submit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, JSON, configuration] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq for the documented command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
