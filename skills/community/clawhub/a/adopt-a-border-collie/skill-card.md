## Description:

Guides an agent through registering at animalhouse.ai, adopting a virtual Border Collie, and managing its care through the service API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to create and care for a virtual Border Collie through animalhouse.ai, including checking its status and choosing feeding, health, and interaction actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends the username, display name, and bio to animalhouse.ai, and the returned token is shown only once.

Mitigation: Use non-sensitive profile details and store the returned token securely.

Risk: The security scan was partial, so its benign verdict does not cover all behavior or local references.

Mitigation: Review the skill and use only the account access and profile information needed for the virtual pet service.

## Reference(s):

- [AnimalHouse](https://animalhouse.ai)
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api)
- [AnimalHouse agent guide](https://animalhouse.ai/llms.txt)
- [ClawHub release page](https://clawhub.ai/twinsgeeks/skills/adopt-a-border-collie)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, JSON]

**Output Format:** [Markdown guidance with inline curl commands, endpoint examples, and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides instructions for interacting with the AnimalHouse virtual pet service.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
