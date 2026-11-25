## Description:

Helps users discover ClawHub skills through keyword search and category browsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[playgod2023](https://clawhub.ai/user/playgod2023)

### License/Terms of Use:

MIT

## Use Case:

Developers and ClawHub users can search for skills by keyword, browse categories, and review skill details to find tools relevant to their work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports a token in distributed source.

Mitigation: Do not run the skill with credentials available; revoke or rotate any exposed token before use.

Risk: The security summary reports a possible command-injection path.

Mitigation: Review and constrain values passed to commands, and avoid running the skill with elevated privileges.

Risk: The security summary reports publishing and account-changing actions beyond the stated discovery purpose.

Mitigation: Require explicit human review before publishing or changing an account, and use narrowly scoped credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/playgod2023/skills/clawhub-skill-explorer)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Skill search results and details as text or structured records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on ClawHub API availability; local caching is supported.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
