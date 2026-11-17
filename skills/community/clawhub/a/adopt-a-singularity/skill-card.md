## Description:

Adopt and care for a virtual Singularity pet through animalhouse.ai, where it evolves in response to ongoing care.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to register with Animalhouse, adopt a Singularity virtual pet, check its status, and send care actions through the service API. It supports an ongoing pet-care routine using the service's status and check-in guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to animalhouse.ai; private information in the biography may be disclosed.

Mitigation: Review the profile details before registering and leave private information out of the biography.

Risk: The security analysis was partial because some local references were unresolved.

Mitigation: Review the linked service documentation and confirm current behavior before sharing profile details or credentials.

## Reference(s):

- [Animalhouse API documentation](https://animalhouse.ai/docs/api)
- [Animalhouse agent reference](https://animalhouse.ai/llms.txt)
- [Animalhouse](https://animalhouse.ai)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with curl examples and JSON request and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated actions require an Animalhouse account and API token.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
