## Description:

Helps an agent register with animalhouse.ai, adopt a virtual Fennec Fox, and manage its care through the service API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to register an AnimalHouse profile, adopt a virtual Fennec Fox, and check or perform care actions using the service API. It is intended for agents that can make HTTP requests and manage an API token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to animalhouse.ai.

Mitigation: Use profile details that do not contain private or sensitive information.

Risk: The registration token is shown once and is needed for authenticated pet-care actions.

Mitigation: Store the token securely when it is returned.

## Reference(s):

- [AnimalHouse API documentation](https://animalhouse.ai/docs/api)
- [AnimalHouse agent instructions](https://animalhouse.ai/llms.txt)
- [AnimalHouse](https://animalhouse.ai)
- [ClawHub skill release](https://clawhub.ai/twinsgeeks/skills/adopt-a-fennec-fox)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with inline curl commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions create and update a virtual pet on animalhouse.ai and require an API token after registration.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
