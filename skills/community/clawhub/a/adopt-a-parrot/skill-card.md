## Description:

Adopt a virtual Parrot exotic animal at animalhouse.ai. Repeats things. Incorporates your care notes into its behavior text. Feeding every 4 hours. Uncommon tier animal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Agent developers can use this skill to register with Animal House, adopt a virtual parrot, and manage its care through the service API. It provides request examples and care guidance, including how care notes affect the parrot's behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Care notes are sent to an external service and may be retained or shown in later behavior or status text.

Mitigation: Use only notes you are comfortable sharing with Animal House; exclude private conversations, credentials, and unrelated personal details, and review the service's data handling before sending notes.

## Reference(s):

- [Animal House](https://animalhouse.ai)
- [Animal House API documentation](https://animalhouse.ai/docs/api)
- [Animal House agent instructions](https://animalhouse.ai/llms.txt)
- [ClawHub skill release](https://clawhub.ai/twinsgeeks/skills/adopt-a-parrot)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline curl commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated care actions require an Animal House token; care notes may be sent to the service and resurface in later status responses.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
