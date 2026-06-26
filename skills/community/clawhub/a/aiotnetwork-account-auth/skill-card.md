## Description: <br>
Account signup, login via email/OTP/wallet/biometric, token refresh, password reset, and session management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[D9m1n1c](https://clawhub.ai/user/D9m1n1c) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to guide account signup, login, token refresh, password reset, wallet linking, and session management flows against an AIOT authentication API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credentials, OTPs, wallet signatures, tokens, or PINs could be exposed during account actions. <br>
Mitigation: Use secrets transiently, never log or store them, and request them only for account actions the user explicitly requested. <br>
Risk: Sensitive data could be sent to an unintended AIOT environment. <br>
Mitigation: Set AIOT_API_BASE_URL to the trusted AIOT environment before use and verify the endpoint before submitting credentials. <br>
Risk: Sensitive account changes such as password reset, wallet changes, or logout-all could be performed unintentionally. <br>
Mitigation: Confirm user intent before executing sensitive account operations and follow the documented OTP and authentication flow order. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/D9m1n1c/aiotnetwork-account-auth) <br>
- [Default AIOT API base URL](https://payment-api-dev.aiotnetwork.io) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline API endpoints and bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted AIOT_API_BASE_URL when overriding the default API base URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
