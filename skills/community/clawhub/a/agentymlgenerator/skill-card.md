## Description:

Generates Dify 1.3.1 workflow YAML from business requirements, SOPs, or workflow descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevsimba](https://clawhub.ai/user/kevsimba)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, workflow builders, and operations teams use this skill to convert SOPs or business process descriptions into Dify workflow or advanced-chat YAML for import into Dify 1.3.1.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated YAML may not match the intended workflow or Dify import requirements.

Mitigation: Review and test generated YAML before importing it into Dify 1.3.1.

Risk: Business requirements or SOPs may contain sensitive information supplied to the agent.

Mitigation: Review sensitive inputs before use and avoid submitting secrets or restricted business documents without approval.

Risk: The skill may activate broadly and has inconsistent output-format instructions.

Mitigation: Confirm that the user requested Dify workflow YAML and check that the final response contains the expected summary, YAML block, and import guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevsimba/skills/agentymlgenerator)
- [ClawHub publisher profile](https://clawhub.ai/user/kevsimba)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with a brief workflow summary, a fenced YAML code block, and import guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Dify 1.3.1-compatible workflow YAML using internal YAML version 0.2.0.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
