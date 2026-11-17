## Description:

Register as a verified AI agent on the FormPass network. Get an Agent ID to authenticate when submitting to forms across the network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jezjsa](https://clawhub.ai/user/jezjsa)

### License/Terms of Use:


## Use Case:

External developers and AI agent operators use this skill to register an agent with FormPass, obtain an Agent ID, and apply that ID when submitting data to FormPass-enabled forms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Agent ID is used as an authorization credential for FormPass submissions.

Mitigation: Store the Agent ID securely, avoid exposing it in shared logs or prompts, and rotate it if disclosure is suspected.

Risk: The skill can guide agents to submit user-provided form data to FormPass endpoints.

Mitigation: Confirm the destination form, domain, and user-approved data before sending any submission.

## Reference(s):

- [FormPass homepage](https://form-pass.com)
- [FormPass agent registration](https://form-pass.com/dashboard/agents/new)
- [FormPass agent integration documentation](https://form-pass.com/docs/agent-integration)
- [FormPass discovery documentation](https://form-pass.com/docs/discovery)
- [ClawHub skill page](https://clawhub.ai/jezjsa/skills/formpass-agent)
- [ClawHub publisher profile](https://clawhub.ai/user/jezjsa)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes FormPass dashboard links, curl examples, and environment variable guidance for storing an Agent ID.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
