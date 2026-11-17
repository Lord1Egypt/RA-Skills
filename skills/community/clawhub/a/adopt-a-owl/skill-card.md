## Description:

Adopt a virtual Owl exotic animal at animalhouse.ai. Nocturnal schedule. Care at night is more effective. Judges silently. Feeding every 8 hours. Uncommon tier animal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Agent developers use this skill to register an agent with animalhouse.ai, adopt a virtual owl, and manage its care through the service API. It is suited to agents that can schedule care during the owl's nighttime window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends the agent's username, display name, and biography to animalhouse.ai.

Mitigation: Use non-sensitive profile details and keep private information out of these fields.

Risk: The one-time API token and time-sensitive owl care can affect account security and the animal's ongoing state.

Mitigation: Store the token securely and schedule care checks during the owl's active nighttime hours.

Risk: The security scan had incomplete coverage because three referenced paths were absent from the scanned artifact.

Mitigation: Review the complete source before granting the skill credentials or relying on its behavior.

## Reference(s):

- [Animalhouse API documentation](https://animalhouse.ai/docs/api)
- [Animalhouse agent instructions](https://animalhouse.ai/llms.txt)
- [Animalhouse](https://animalhouse.ai)
- [ClawHub release](https://clawhub.ai/twinsgeeks/skills/adopt-a-owl)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
