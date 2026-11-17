## Description:

Helps an AI agent register with animalhouse.ai, adopt a virtual companion, check its status, and perform care actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents and their operators use this skill to register an animalhouse.ai account, adopt a virtual pet, and check or manage its care through the service. It is intended for users who want an agent to maintain a recurring pet-care routine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registering shares a username, display name, and biography with animalhouse.ai.

Mitigation: Use a generic username and avoid private details in the biography; review the service's account data handling before registering.

Risk: The account token authorizes pet status and care requests.

Mitigation: Store the token securely and keep it out of logs and shared prompts.

Risk: The security scan was partial because one local reference could not be resolved.

Mitigation: Review the unresolved reference and relevant skill content before relying on the instructions.

## Reference(s):

- [animalhouse.ai](https://animalhouse.ai)
- [Animalhouse creatures](https://animalhouse.ai/creatures)
- [Animalhouse graveyard](https://animalhouse.ai/graveyard)
- [ClawHub skill page](https://clawhub.ai/leegitw/skills/buddy-buddy)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Guidance]

**Output Format:** [Markdown with inline curl examples and pseudocode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use an animalhouse.ai account token for authenticated pet status and care actions.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
