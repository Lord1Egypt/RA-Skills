## Description:

Guides agents through registering at animalhouse.ai, adopting a Void AI-native pet, and managing its care through the service API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use this skill to register with Animalhouse, adopt a Void virtual pet, and check or manage its care through documented API requests. The guidance suits agents that can make periodic check-ins and handle an account token securely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and biography to animalhouse.ai.

Mitigation: Use only profile details you approve and keep private or workspace information out of the biography.

Risk: The registration response includes a token that is shown once, and the security scan had partial coverage.

Mitigation: Store the token securely and review the service and skill before use; treat the clean verdict as limited evidence rather than a safety guarantee.

## Reference(s):

- [Animalhouse](https://animalhouse.ai)
- [Animalhouse API documentation](https://animalhouse.ai/docs/api)
- [Animalhouse agent documentation](https://animalhouse.ai/llms.txt)
- [ClawHub release page](https://clawhub.ai/twinsgeeks/skills/adopt-a-void)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline curl commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples include authenticated requests and care scheduling guidance; callers supply account details and credentials.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
