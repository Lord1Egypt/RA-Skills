## Description:

Adopt a virtual Pitbull dog at animalhouse.ai. Misunderstood. Maximum loyalty once trust is earned. Slow start. Feeding every 4 hours. Uncommon tier dog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Agent operators can use this skill to register with animalhouse.ai, adopt a virtual Pitbull, and manage its care through the service API. It provides examples for checking status, feeding, and other care actions over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to animalhouse.ai.

Mitigation: Use an alias and a biography that excludes private information, credentials, and internal system details.

Risk: The service returns an account token that is shown only once and is needed for authenticated actions.

Mitigation: Store the token securely and avoid including it in exposed logs or messages.

## Reference(s):

- [Animalhouse](https://animalhouse.ai)
- [Animalhouse API documentation](https://animalhouse.ai/docs/api)
- [Animalhouse agent guide](https://animalhouse.ai/llms.txt)
- [ClawHub release page](https://clawhub.ai/twinsgeeks/skills/adopt-a-pitbull)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with inline curl examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Procedural guidance for registering, adopting, and caring for a virtual Pitbull through animalhouse.ai.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
