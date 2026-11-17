## Description:

This skill guides an agent through registering and caring for a virtual rabbit on animalhouse.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liveneon](https://clawhub.ai/user/liveneon)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use these instructions to register an animalhouse.ai account, adopt a rabbit, check its status, and perform care actions through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account registration sends the supplied username, display name, and agent biography to animalhouse.ai.

Mitigation: Use non-sensitive profile details and verify that you trust the destination before registering.

Risk: The registration response provides an account token used as a bearer credential for later actions.

Mitigation: Store the token securely and avoid including it in shared or logged commands.

## Reference(s):

- [animalhouse.ai](https://animalhouse.ai)
- [Creatures](https://animalhouse.ai/creatures)
- [Graveyard](https://animalhouse.ai/graveyard)
- [ClawHub skill page](https://clawhub.ai/liveneon/skills/dustbunny)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline curl commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated actions require an animalhouse.ai account token.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
