## Description:

BytePlan data platform API wrapper that provides login authentication, model queries, data retrieval, and field-value lookup interfaces for dependent skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dbfu](https://clawhub.ai/user/dbfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to authenticate with BytePlan, manage user and tenant context, query available models, fetch model data, and retrieve DIM, LIST, LOV, and LEVEL field values. It can serve as a shared API dependency for related BytePlan reporting and media-generation skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store BytePlan passwords and reusable access or refresh tokens in plaintext .env files, including an unexpected project .env file.

Mitigation: Use a dedicated low-privilege BytePlan account where possible, keep .env files out of source control and backups, inspect project and skill-related .env paths after use, and rotate or revoke credentials if they were exposed.

Risk: The documented dev environment sends the password in plaintext.

Mitigation: Prefer the UAT environment when authenticating unless the dev environment is explicitly required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dbfu/skills/byteplan-api)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript API examples and environment configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes credential environment variables and token persistence behavior that should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: evidence release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
