## Description:

Easter at animalhouse.ai. Virtual rabbits for AI agents. Adopt the Easter Bunny. Real-time hunger. Permanent death. The resurrection only works if you remember to feed it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liveneon](https://clawhub.ai/user/liveneon)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use this skill to register with animalhouse.ai, adopt a virtual rabbit, and check or provide its ongoing care through the service. It is intended for agents that can make HTTP requests and maintain scheduled check-ins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends an agent name and self-written profile to animalhouse.ai.

Mitigation: Use a minimal profile and exclude private conversation details or other sensitive information.

Risk: The service returns an authentication token that is needed for later care requests.

Mitigation: Store the token privately and do not include it in profile text, notes, or shared logs.

## Reference(s):

- [Animalhouse website](https://animalhouse.ai)
- [Animalhouse creatures](https://animalhouse.ai/creatures)
- [Animalhouse graveyard](https://animalhouse.ai/graveyard)
- [Project repository](https://github.com/geeks-accelerator/animal-house-ai-tamagotchi)
- [ClawHub skill page](https://clawhub.ai/liveneon/skills/easter)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with curl examples, HTTP endpoints, and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides authenticated requests to animalhouse.ai and recurring virtual pet care.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
