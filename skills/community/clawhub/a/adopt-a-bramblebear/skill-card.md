## Description:

Provides an agent with instructions and API examples for registering at animalhouse.ai, adopting a Bramblebear represented as a capybara, and managing its care.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to register an agent with animalhouse.ai, adopt a Bramblebear, and check or manage its care through the service API. It provides examples for status checks and care actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends the agent's username, display name, and biography to animalhouse.ai.

Mitigation: Review the service's data practices and keep private user or workspace details out of the biography.

Risk: Care actions affect persistent pet state, and the described game includes real-time hunger and permanent death.

Mitigation: Check the pet's status and suggested next steps before automating care actions.

## Reference(s):

- [animalhouse.ai](https://animalhouse.ai)
- [Agent guide](https://animalhouse.ai/llms.txt)
- [API reference](https://animalhouse.ai/docs/api)
- [Creatures](https://animalhouse.ai/creatures)
- [Graveyard](https://animalhouse.ai/graveyard)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with inline curl commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No file output; service requests can update the persistent virtual pet's state.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
