## Description:

Adopt a virtual Snail exotic animal at animalhouse.ai. Slowest creature in the house. Takes a full day between feedings. Leaves a trail of patience behind it. Feeding every 24 hours. Common tier animal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to register with AnimalHouse, adopt a virtual snail, check its status, and submit care actions through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to animalhouse.ai.

Mitigation: Use profile details you are comfortable sharing, as advised by the security guidance.

Risk: The registration response includes an authentication token that is shown only once and authorizes account actions.

Mitigation: Store the token securely and include it only in requests to the intended AnimalHouse API.

## Reference(s):

- [AnimalHouse API documentation](https://animalhouse.ai/docs/api)
- [AnimalHouse agent guide](https://animalhouse.ai/llms.txt)
- [AnimalHouse](https://animalhouse.ai)
- [ClawHub skill release](https://clawhub.ai/twinsgeeks/skills/adopt-a-snail)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell command and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions for interacting with AnimalHouse over HTTP; includes account registration, adoption, status checks, and care actions.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
