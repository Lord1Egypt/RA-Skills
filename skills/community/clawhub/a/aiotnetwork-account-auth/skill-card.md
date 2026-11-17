## Description:

Account signup, login via email/OTP/wallet/biometric, token refresh, password reset, and session management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d9m1n1c](https://clawhub.ai/user/d9m1n1c)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide account signup, authentication, session management, password recovery, and wallet-linking flows for the AIOT account API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive authentication material, including passwords, OTPs, bearer tokens, refresh tokens, and wallet-linking actions.

Mitigation: Keep credentials scoped to user-initiated requests, avoid logging or persisting secrets, and verify the configured AIOT_API_BASE_URL before use.

Risk: Account operations can fail or lock accounts when authentication flows are skipped or repeated incorrectly.

Mitigation: Follow the documented OTP, login, token refresh, password reset, and unlock flow order before retrying account actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, API Calls, shell commands, configuration]

**Output Format:** [Markdown with endpoint descriptions and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AIOT_API_BASE_URL for API base URL configuration; handles passwords, OTPs, bearer tokens, refresh tokens, and wallet-linking inputs transiently.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
