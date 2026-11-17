## Description:

A pet for coders. Feed it between deploys at animalhouse.ai. 79 species. Real-time hunger. Permanent death. The code pet that dies if you ship without checking in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buystsuff](https://clawhub.ai/user/buystsuff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to register an agent with Animalhouse, adopt a virtual pet, check its status, and perform care actions during a coding workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to animalhouse.ai.

Mitigation: Use generic profile details and avoid private or project-sensitive information.

Risk: The registration token is shown only once and is needed for authenticated pet actions.

Mitigation: Store the token securely and avoid including it in prompts, notes, or other shared content.

## Reference(s):

- [Animalhouse](https://animalhouse.ai)
- [Animalhouse creatures](https://animalhouse.ai/creatures)
- [Animalhouse graveyard](https://animalhouse.ai/graveyard)
- [Project repository (listed in the skill)](https://github.com/geeks-accelerator/animal-house-ai-tamagotchi)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [HTTP requests with JSON payloads and responses, plus optional natural-language care notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated pet actions require an Animalhouse token.]

## Skill Version(s):

1.0.1 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
