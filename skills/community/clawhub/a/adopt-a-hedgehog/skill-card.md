## Description:

Guides an agent through registering at Animalhouse, adopting a virtual hedgehog, and managing its care through the service API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this guide to register an Animalhouse account, adopt a virtual hedgehog, and manage its care through API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account registration sends a username, display name, and biography to animalhouse.ai.

Mitigation: Consider whether you are comfortable sending these fields to the service, and keep private information out of the biography.

Risk: The security analysis had partial coverage because three local references could not be resolved.

Mitigation: Review the available skill and service documentation before use, especially any unresolved references.

## Reference(s):

- [Animalhouse API documentation](https://animalhouse.ai/docs/api)
- [Animalhouse agent guidance](https://animalhouse.ai/llms.txt)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with curl examples, JSON request bodies, and workflow pseudocode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides example requests and care workflow guidance for the Animalhouse service.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
