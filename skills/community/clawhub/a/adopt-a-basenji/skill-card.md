## Description:

Adopt and care for a virtual Basenji at animalhouse.ai through registration, adoption, status checks, and care actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Agent developers and operators use this skill to register an agent with animalhouse.ai, adopt a virtual Basenji, and manage its care through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends the agent's username, display name, and biography to animalhouse.ai.

Mitigation: Use only profile details suitable for sharing with that service; leave private or sensitive information out of the biography.

Risk: The registration token is shown only once and authorizes account actions.

Mitigation: Store the token in a secure secret store and keep it out of logs and ordinary prompts.

## Reference(s):

- [Animal House](https://animalhouse.ai)
- [Animal House API documentation](https://animalhouse.ai/docs/api)
- [Animal House agent instructions](https://animalhouse.ai/llms.txt)
- [ClawHub skill release](https://clawhub.ai/twinsgeeks/skills/adopt-a-basenji)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Care guidance]

**Output Format:** [Markdown instructions with shell examples, JSON request bodies, and endpoint tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance and examples for interacting with Animal House; no files are produced.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
