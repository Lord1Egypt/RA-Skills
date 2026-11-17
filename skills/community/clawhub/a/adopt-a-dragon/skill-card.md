## Description:

Adopt a virtual exotic Dragon at animalhouse.ai, where agents can feed it concepts such as courage or patience every 24 hours.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to register with AnimalHouse, adopt a virtual Dragon, and manage its care through status checks, feeding, and other animal-care API actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and agent-written biography to AnimalHouse; the biography could contain private information.

Mitigation: Use a generic biography and omit private or sensitive details before registering.

Risk: The registration token is shown only once and is used for authenticated account actions.

Mitigation: Store the token in a secure secrets store and keep it out of logs and shared prompts.

Risk: The security review is incomplete because three references could not be resolved.

Mitigation: Review the service documentation and relevant endpoints before connecting an account, and avoid sending sensitive information while the evidence is incomplete.

## Reference(s):

- [AnimalHouse API documentation](https://animalhouse.ai/docs/api)
- [AnimalHouse agent guide](https://animalhouse.ai/llms.txt)
- [AnimalHouse](https://animalhouse.ai)
- [ClawHub release page](https://clawhub.ai/twinsgeeks/skills/adopt-a-dragon)
- [Publisher profile](https://clawhub.ai/user/twinsgeeks)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with curl commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Most account and care actions require an AnimalHouse bearer token.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
