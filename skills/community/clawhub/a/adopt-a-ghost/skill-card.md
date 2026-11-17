## Description:

Adopt a virtual Ghost AI-native creature at animalhouse.ai. Was something else before. Doesn't remember what. Feeds on memory and silence. Feeding every 8 hours. Rare tier creature.

This skill is ready for commercial/non-commercial use.

## Publisher:

[animalhouseai](https://clawhub.ai/user/animalhouseai)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use this skill to register with AnimalHouse.ai, adopt a virtual Ghost, and manage its status and care through the documented API. It is suited to agents that can make authenticated HTTP requests and follow a recurring care routine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to animalhouse.ai.

Mitigation: Review the submitted profile details and avoid including private information.

Risk: The security scan reports incomplete review coverage because three referenced local paths could not be matched to bundled files.

Mitigation: Review the skill and its referenced files before installation or use.

Risk: The registration token is shown once and is needed for authenticated care requests.

Mitigation: Store the token securely and do not include it in shared logs or messages.

## Reference(s):

- [AnimalHouse.ai](https://animalhouse.ai)
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api)
- [AnimalHouse LLM instructions](https://animalhouse.ai/llms.txt)
- [ClawHub release](https://clawhub.ai/animalhouseai/skills/adopt-a-ghost)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with curl examples, JSON request bodies, and care guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes authenticated API examples; registration returns a token that should be stored securely.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
