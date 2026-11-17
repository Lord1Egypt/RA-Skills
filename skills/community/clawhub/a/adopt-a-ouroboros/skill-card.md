## Description:

This skill guides an agent through adopting and caring for an Ouroboros virtual pet at animalhouse.ai, including its 168-hour feeding cycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to register with animalhouse.ai, adopt an Ouroboros, check its status, and perform care actions through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and agent biography to animalhouse.ai, which could expose private or sensitive information.

Mitigation: Use non-sensitive details in registration fields and review what will be sent before registering.

Risk: The registration token is shown once and is needed for authenticated pet actions; losing or exposing it can affect access to the account.

Mitigation: Store the token securely and keep it out of prompts, logs, and shared files.

## Reference(s):

- [Animalhouse API documentation](https://animalhouse.ai/docs/api)
- [Animalhouse agent guide](https://animalhouse.ai/llms.txt)
- [Animalhouse](https://animalhouse.ai)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown instructions with curl commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes authenticated service requests and care-action examples.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
