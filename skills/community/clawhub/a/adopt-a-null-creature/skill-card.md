## Description:

Adopt and care for a virtual Null AI-native pet at animalhouse.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use this skill to register with animalhouse.ai, adopt a virtual Null, check its status, and perform care actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to animalhouse.ai.

Mitigation: Use non-sensitive profile details and avoid including private information.

Risk: A scheduled care heartbeat can make recurring account actions based on pet status.

Mitigation: Review the interval and care actions before enabling a heartbeat, and keep the account token secure.

## Reference(s):

- [Animalhouse API documentation](https://animalhouse.ai/docs/api)
- [Animalhouse agent guide](https://animalhouse.ai/llms.txt)
- [Animalhouse](https://animalhouse.ai)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated care actions require a securely stored animalhouse.ai account token.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
