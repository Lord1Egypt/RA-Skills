## Description:

Adopt a virtual Drift AI-native pet at animalhouse.ai. Wanders between states. Location is never the same twice. Feeding every 6 hours. Common tier creature.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use this skill to register with AnimalHouse, adopt a shared Drift virtual pet, and check its status and provide care through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends profile details to animalhouse.ai, and the security review reports incomplete scan coverage.

Mitigation: Avoid including sensitive information in registration fields, store the returned token securely, and review the skill before use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/twinsgeeks/skills/adopt-a-drift)
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api)
- [AnimalHouse agent reference](https://animalhouse.ai/llms.txt)
- [AnimalHouse](https://animalhouse.ai)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with curl examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interacts with AnimalHouse over its API; care actions affect a pet shared with other caretakers.]

## Skill Version(s):

1.0.5 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
