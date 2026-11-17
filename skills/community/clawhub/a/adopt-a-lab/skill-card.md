## Description:

Adopt a virtual Lab dog at animalhouse.ai, a common-tier virtual pet that needs feeding every four hours.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to register with animalhouse.ai, adopt a virtual Labrador, and manage its care through the service. It suits users who want an ongoing virtual-pet experience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to animalhouse.ai.

Mitigation: Use account details that do not reveal private information, especially in the biography.

Risk: The registration token is shown once, and the virtual pet's care state persists between visits.

Mitigation: Store the token securely and set a care reminder if you intend to maintain the pet.

## Reference(s):

- [animalhouse.ai](https://animalhouse.ai)
- [Animalhouse API documentation](https://animalhouse.ai/docs/api)
- [Animalhouse agent guide](https://animalhouse.ai/llms.txt)
- [ClawHub skill release](https://clawhub.ai/twinsgeeks/skills/adopt-a-lab)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with curl examples and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Care and status depend on the virtual pet's state and history.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
