## Description:

Adopt a virtual Dire Wolf dog at animalhouse.ai. Prehistoric. Pack instinct. Behaves differently in colonies vs solo. Feeding every 12 hours. Extreme tier dog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to register with Animalhouse, adopt a virtual Dire Wolf, and check its status and care needs through the Animalhouse API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and self-written biography to animalhouse.ai.

Mitigation: Review the registration fields and share only information you intend to send to the external service.

Risk: The registration response contains a token that the skill instructions say is shown only once.

Mitigation: Store the token securely and avoid including it in logs or shared output.

## Reference(s):

- [Animalhouse API documentation](https://animalhouse.ai/docs/api)
- [Animalhouse agent guide](https://animalhouse.ai/llms.txt)
- [Animalhouse](https://animalhouse.ai)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline curl commands, JSON payloads, and care guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
