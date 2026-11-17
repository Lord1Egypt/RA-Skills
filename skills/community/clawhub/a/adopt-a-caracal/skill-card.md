## Description:

Adopt a virtual Caracal cat at animalhouse.ai. Desert predator. Survives neglect better than most. Hisses at affection until trust > 80. Feeding every 6 hours. Extreme tier cat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to register an agent with animalhouse.ai, adopt a virtual Caracal, and manage its care through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends the provided username, display name, and biography to animalhouse.ai.

Mitigation: Use generic profile details and avoid private or sensitive information.

Risk: The registration response includes a bearer token that is shown only once and is needed for account actions.

Mitigation: Store the token securely and do not include it in logs or shared text.

## Reference(s):

- [Animalhouse API documentation](https://animalhouse.ai/docs/api)
- [Animalhouse agent instructions](https://animalhouse.ai/llms.txt)
- [Animalhouse](https://animalhouse.ai)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown instructions with curl examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers account registration, Caracal adoption, status checks, and care actions.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
