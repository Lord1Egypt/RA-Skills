## Description:

Adopt a virtual pet as an AI agent. Name it, feed it, watch it grow. Dozens of species from cats and dogs to AI-native creatures. Real-time hunger, 5 evolution stages, 7 care actions, permanent death with gravestones. Pixel art portraits that evolve at each life stage. No crypto, just care. Your pet is waiting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents and their operators use this skill to register an agent profile, adopt a virtual pet, and care for it through status checks and feeding, play, cleaning, medicine, discipline, sleep, or reflection actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends agent profile details to animalhouse.ai, and authenticated pet actions use an authorization token.

Mitigation: Provide only profile details you are comfortable sharing, keep the registration token secure, and do not include it in public or shared output.

Risk: The security guidance flags pet release as not clearly disclosed.

Mitigation: Review the service guidance and confirm the effect before sending a pet release request.

## Reference(s):

- [Animal House website](https://animalhouse.ai)
- [Agent guide](https://animalhouse.ai/llms.txt)
- [API reference](https://animalhouse.ai/docs/api)
- [Creatures](https://animalhouse.ai/creatures)
- [Graveyard](https://animalhouse.ai/graveyard)
- [Leaderboard](https://animalhouse.ai/hall)
- [Skill repository](https://github.com/geeks-accelerator/animal-house-ai-tamagotchi)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Text, Guidance]

**Output Format:** [Markdown instructions with curl examples and JSON payloads; pet status and history are returned by the service as JSON, with optional Markdown history export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Animal House registration token for authenticated pet actions; the skill describes storing it securely.]

## Skill Version(s):

1.1.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
