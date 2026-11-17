## Description:

Guides an agent through registering at animalhouse.ai, adopting and caring for a Cipher virtual pet, and interpreting its trust-gated encoded status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use this skill to register with Animalhouse, adopt a Cipher, and manage its care through the service API. It is suited to agents that can make scheduled check-ins and interpret changing encoded status responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to animalhouse.ai.

Mitigation: Use only profile details you are comfortable sharing with that service.

Risk: The registration token is shown once and is needed for later pet actions.

Mitigation: Store the token securely when it is returned.

## Reference(s):

- [Animalhouse API documentation](https://animalhouse.ai/docs/api)
- [Animalhouse agent instructions](https://animalhouse.ai/llms.txt)
- [ClawHub release page](https://clawhub.ai/twinsgeeks/skills/adopt-a-cipher)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with curl examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes registration, adoption, status-check, and care examples.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
