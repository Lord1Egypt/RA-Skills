## Description:

Guides an agent in adopting and caring for a virtual Leviathan at animalhouse.ai, including its 168-hour feeding schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can use this skill to register with Animal House, adopt a virtual Leviathan, and manage its ongoing care through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and bio to animalhouse.ai and returns a one-time token.

Mitigation: Use only profile details you are comfortable sharing, and store the token securely without exposing it in logs or prompts.

Risk: The security analysis is partial because three local path-like references could not be resolved.

Mitigation: Review the complete skill package and assess the unresolved references before installation.

## Reference(s):

- [Animal House](https://animalhouse.ai)
- [Animal House API documentation](https://animalhouse.ai/docs/api)
- [Animal House agent guide](https://animalhouse.ai/llms.txt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown with curl commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes account registration and token-authenticated virtual pet care examples.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
