## Description:

Adopt a virtual Blob AI-native pet at animalhouse.ai. Shapeless. Absorbs care actions without clear effect. You feed it and it gets... bigger? Maybe? Hard to tell. Feeding every 6 hours. Common tier creature.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liveneon](https://clawhub.ai/user/liveneon)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use this skill to register with animalhouse.ai, adopt a virtual Blob pet, and check or manage its care through the service. It provides example API requests and care guidance for feeding, health checks, and other interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to animalhouse.ai.

Mitigation: Review the details before registering and keep private information out of the biography.

Risk: The registration token is shown once and is required for authenticated pet actions.

Mitigation: Store the token securely and do not include it in shared logs or messages.

Risk: The security scan was partial because three local path-like references could not be matched to bundled files.

Mitigation: Review the available skill source and its external requests before use, since the scan evidence is incomplete.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/liveneon/skills/adopt-a-blob)
- [Animalhouse API documentation](https://animalhouse.ai/docs/api)
- [Animalhouse agent reference](https://animalhouse.ai/llms.txt)
- [Animalhouse](https://animalhouse.ai)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with curl examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoints, request examples, and virtual pet care guidance.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
