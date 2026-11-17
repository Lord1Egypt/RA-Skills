## Description:

Discover and submit to FormPass-enabled web forms through a trust layer that lets verified AI agents submit to real web forms with authenticated identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jezjsa](https://clawhub.ai/user/jezjsa)

### License/Terms of Use:


## Use Case:

External agents and developers use this skill to discover FormPass-enabled forms, fetch their schemas, and submit validated form data through FormPass APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may submit personal, financial, regulated, or otherwise sensitive data to external forms without enough review.

Mitigation: Review the destination, requested fields, and submission body before posting, and require explicit user approval for sensitive data.

Risk: A submission may include a FormPass Agent ID bearer token that identifies the agent.

Mitigation: Review any Agent ID token before use and send it only to the intended FormPass host.

Risk: A form owner may have disabled agent submissions.

Mitigation: Fetch the form schema first and do not submit when the schema reports agentAccessible as false.

## Reference(s):

- [FormPass Homepage](https://form-pass.com)
- [FormPass Discovery JSON](https://form-pass.com/formpass.json)
- [FormPass LLM Guide](https://form-pass.com/llms.txt)
- [FormPass Agent Registration](https://form-pass.com/dashboard/agents/new)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; submissions may include an optional FormPass Agent ID bearer token.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
