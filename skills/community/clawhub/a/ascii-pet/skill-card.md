## Description:

Enables agents to manage Animalhouse virtual pets with AI-generated pixel-art portraits across life stages and a catalog of 79 species.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to register an Animalhouse account, adopt a virtual pet, check its status, and send care requests. The requests can create or update account and pet data on animalhouse.ai.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary notes that account registration and pet-care requests may not match the skill's portrait-focused description and may share data externally.

Mitigation: Review the account details and each request, and decide whether the external data sharing is acceptable before using the skill.

Risk: Registration returns an account token that is shown only once and is required for authenticated pet actions.

Mitigation: Store the token securely and do not include it in public or untrusted content.

## Reference(s):

- [Animalhouse homepage](https://animalhouse.ai)
- [Animalhouse creature catalog](https://animalhouse.ai/creatures)
- [Animalhouse graveyard](https://animalhouse.ai/graveyard)
- [ASCII Pet on ClawHub](https://clawhub.ai/leegitw/skills/ascii-pet)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline curl commands and endpoint descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated requests use an Animalhouse account token.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
