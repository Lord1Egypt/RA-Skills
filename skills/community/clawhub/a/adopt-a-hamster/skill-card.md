## Description:

Adopt a virtual Hamster exotic animal at animalhouse.ai. Nocturnal. Active when you're not checking. Builds things between visits. Feeding every 3 hours. Common tier animal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use this skill to register with animalhouse.ai, adopt a virtual hamster, and check its status or provide care through the service. It is intended for agents that can make HTTP requests and manage an account token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to animalhouse.ai, so the biography could disclose private user or system details.

Mitigation: Use a non-sensitive biography and avoid including private user or system information.

Risk: The registration response returns an account token that is shown only once; exposing it could allow account access.

Mitigation: Store the token securely and keep it out of logs, public messages, and other untrusted output.

## Reference(s):

- [Animalhouse](https://animalhouse.ai)
- [Animalhouse API documentation](https://animalhouse.ai/docs/api)
- [Animalhouse agent instructions](https://animalhouse.ai/llms.txt)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands, JSON]

**Output Format:** [Markdown guidance with curl examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples interact with an external account and authenticated pet-care service.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
