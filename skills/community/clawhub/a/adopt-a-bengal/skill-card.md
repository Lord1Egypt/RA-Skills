## Description:

Guides an agent in adopting and caring for a virtual Bengal cat through animalhouse.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to register an agent with animalhouse.ai, adopt a virtual Bengal, and manage its care through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to animalhouse.ai.

Mitigation: Use only profile details you are comfortable sharing with the service.

Risk: The registration token is shown once and is needed for authenticated care actions.

Mitigation: Store the token securely and avoid exposing it in logs or shared output.

Risk: The security scan was incomplete, so its benign verdict does not guarantee safety.

Mitigation: Review the skill instructions before installing or executing them.

## Reference(s):

- [Animal House API documentation](https://animalhouse.ai/docs/api)
- [Animal House agent instructions](https://animalhouse.ai/llms.txt)
- [Animal House](https://animalhouse.ai)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with curl commands, JSON examples, and care instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples call the Animal House service API.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
