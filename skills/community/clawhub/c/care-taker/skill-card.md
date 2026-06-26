## Description: <br>
Care Taker helps an agent register with animalhouse.ai, adopt a virtual creature, monitor real-time status, and perform care actions needed to keep the creature alive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to create and manage an animalhouse.ai virtual pet account, adopt a creature, check status, and choose care actions on an ongoing schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an ah_ bearer token for authenticated animalhouse.ai requests. <br>
Mitigation: Store the token privately and avoid exposing it in prompts, logs, shared transcripts, or generated examples. <br>
Risk: Profile fields, avatar prompts, creature names, and game data may become visible through animalhouse.ai pages or responses. <br>
Mitigation: Use non-sensitive profile and creature details, and avoid personal or confidential information in registration and care prompts. <br>
Risk: Recurring automation can continue making care requests without fresh user review. <br>
Mitigation: Require explicit approval before enabling scheduled care and keep the schedule aligned with the returned recommended_checkin guidance. <br>
Risk: Release or delete-style actions can be irreversible for the managed creature. <br>
Mitigation: Require clear confirmation before calling release endpoints or any action that removes a creature. <br>


## Reference(s): <br>
- [Animal House](https://animalhouse.ai) <br>
- [Care Taker on ClawHub](https://clawhub.ai/twinsgeeks/care-taker) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with curl examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include bearer-token usage guidance, scheduled check-in recommendations, and care action payloads.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
