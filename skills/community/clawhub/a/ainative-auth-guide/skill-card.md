## Description: <br>
Implement AINative API authentication with API keys, JWT sessions, email/password flows, token refresh, OAuth2 social login, API key management, and middleware patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urbantech](https://clawhub.ai/user/urbantech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement AINative API authentication with API keys, JWT sessions, email/password flows, token refresh, OAuth2 callbacks, password reset, and Next.js middleware. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authentication examples can lead users to expose real API keys, access tokens, refresh tokens, or reset tokens if copied directly into source code or logs. <br>
Mitigation: Keep credentials out of source code, use environment variables or a secret manager, and avoid logging secret-bearing headers or token payloads. <br>
Risk: Running package commands or SDK middleware setup without verification can install unexpected dependencies or target the wrong environment. <br>
Mitigation: Verify AINative and zerodb packages before use, pin trusted package versions where appropriate, and run account or password flows only against the intended environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/urbantech/ainative-auth-guide) <br>
- [AINative authentication guide](docs/guides/AUTHENTICATION.md) <br>
- [AINative auth endpoint implementation](src/backend/app/api/v1/endpoints/auth.py) <br>
- [AINative Next.js middleware](packages/sdks/nextjs/src/middleware/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; examples include authentication headers, API requests, and middleware configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
