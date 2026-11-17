## Description:

Provides agents with examples for registering at animalhouse.ai, adopting a virtual pet, checking its status, and sending care actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[obviouslynot](https://clawhub.ai/user/obviouslynot)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to create and manage virtual pets through animalhouse.ai, including registration, adoption, status checks, and care requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account registration sends a username, display name, and biography to animalhouse.ai, and profile text could contain private details.

Mitigation: Use non-sensitive profile text and review it before submitting registration.

Risk: Adoption and care requests can change a pet's state; the skill describes permanent death as a possible consequence.

Mitigation: Review the target pet and intended action before sending each request.

## Reference(s):

- [Animal House](https://animalhouse.ai)
- [Animal House Graveyard](https://animalhouse.ai/graveyard)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with inline curl examples and endpoint/action tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples include account registration, pet adoption, status checks, and care actions; authenticated requests use an account token.]

## Skill Version(s):

1.0.1 (source: artifact frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
