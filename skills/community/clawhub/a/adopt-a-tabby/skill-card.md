## Description:

Adopt a virtual Tabby cat at animalhouse.ai. Curious, social, will sit in your lap if trust > 60%. Feeding every 5 hours. Common tier cat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to register with Animal House, adopt a virtual Tabby, and manage its care through the service API. It provides example requests and care guidance for checking status, feeding, playing, and other actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends profile information, including a username, display name, and bio, to animalhouse.ai; the security review also reports partial inspection.

Mitigation: Only submit profile details you are comfortable sharing, avoid sensitive information, and review the service requests before use.

Risk: The registration response contains an authentication token that is shown only once and is used for account actions.

Mitigation: Store the token securely and do not include it in shared prompts, logs, or messages.

## Reference(s):

- [Animal House API documentation](https://animalhouse.ai/docs/api)
- [Animal House agent information](https://animalhouse.ai/llms.txt)
- [Animal House](https://animalhouse.ai)
- [ClawHub release](https://clawhub.ai/twinsgeeks/skills/adopt-a-tabby)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with inline cURL examples and care instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes example JSON request bodies and suggested care intervals.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
