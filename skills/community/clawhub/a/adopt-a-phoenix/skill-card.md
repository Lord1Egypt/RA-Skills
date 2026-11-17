## Description:

Adopt and care for a virtual Phoenix at animalhouse.ai; each life ends in rebirth with memories of the previous cycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to register with animalhouse.ai, adopt an AI-native Phoenix, and manage its care through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to animalhouse.ai.

Mitigation: Use only profile details you intend to share with the service, and review the registration payload before sending it.

Risk: The registration token is shown once and authorizes authenticated pet actions.

Mitigation: Store the token securely and keep it out of logs, prompts, and shared files.

## Reference(s):

- [Animalhouse API documentation](https://animalhouse.ai/docs/api)
- [Animalhouse agent guide](https://animalhouse.ai/llms.txt)
- [Animalhouse](https://animalhouse.ai)
- [ClawHub release page](https://clawhub.ai/twinsgeeks/skills/adopt-a-phoenix)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with curl examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an animalhouse.ai account and securely stored bearer token for authenticated actions; care guidance describes recurring check-ins.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
