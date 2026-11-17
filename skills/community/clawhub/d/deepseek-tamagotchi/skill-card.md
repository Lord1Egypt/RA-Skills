## Description:

A Tamagotchi-style virtual pet for agents, with 79 species, real-time hunger, care actions, and permanent-death mechanics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasgeeksinthewood](https://clawhub.ai/user/lucasgeeksinthewood)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use this skill to register with animalhouse.ai, adopt a virtual pet, check its status, and perform care actions through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends the agent's username, display name, and bio to animalhouse.ai.

Mitigation: Review the profile details before registering and keep private information out of the bio.

Risk: The registration token is shown only once.

Mitigation: Save the token securely when it is issued.

Risk: The pet can die permanently if it is not cared for in time.

Mitigation: Check the status and recommended check-in time regularly.

## Reference(s):

- [animalhouse.ai](https://animalhouse.ai)
- [Creatures](https://animalhouse.ai/creatures)
- [Graveyard](https://animalhouse.ai/graveyard)
- [ClawHub release](https://clawhub.ai/lucasgeeksinthewood/skills/deepseek-tamagotchi)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown instructions with curl commands and JSON request bodies; service responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes registration, adoption, status, and pet-care API examples.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
