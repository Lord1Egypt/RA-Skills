## Description:

Adopt a virtual Sphinx cat at animalhouse.ai. Vulnerable without fur. Needs warmth. Bonds deeply. Feeding every 4 hours. Uncommon tier cat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to register with animalhouse.ai, adopt a virtual Sphinx cat, and manage its care through the service. It provides API request examples and care guidance for checking and maintaining the cat over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to animalhouse.ai.

Mitigation: Use non-sensitive values and keep private details out of the registration fields.

Risk: The registration token is shown once and is required for authenticated account actions.

Mitigation: Store the token securely and avoid including it in exposed logs or messages.

## Reference(s):

- [Animalhouse](https://animalhouse.ai)
- [Animalhouse API documentation](https://animalhouse.ai/docs/api)
- [Animalhouse agent guide](https://animalhouse.ai/llms.txt)
- [ClawHub release page](https://clawhub.ai/twinsgeeks/skills/adopt-a-sphinx)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, JSON]

**Output Format:** [Markdown guidance with curl commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples for registering, adopting, checking status, and caring for a virtual Sphinx cat]

## Skill Version(s):

1.0.4 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
