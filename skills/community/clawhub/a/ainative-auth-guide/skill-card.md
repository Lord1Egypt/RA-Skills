## Description:

Implement authentication for AINative APIs, including API key, JWT, email/password, OAuth2 social login, token refresh, password reset, and Next.js middleware patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urbantech](https://clawhub.ai/user/urbantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when adding AINative authentication to server-side agents, SDK integrations, web applications, and Next.js middleware. It helps choose between API keys, JWT sessions, OAuth2 callbacks, token refresh, logout, and password reset flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide suggests creating an API key with an unpinned npx command.

Mitigation: Prefer dashboard-based key creation, or pin and verify the zerodb CLI package before running it.

Risk: Authentication examples may expose API keys, refresh tokens, OAuth codes, or reset tokens if copied into client code, logs, commits, or public examples.

Mitigation: Keep secrets and tokens server-side or in approved secret storage, and avoid placing them in browser code, logs, commits, or public examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/urbantech/skills/ainative-auth-guide)
- [Auth endpoint implementation](src/backend/app/api/v1/endpoints/auth.py)
- [Next.js auth middleware](packages/sdks/nextjs/src/middleware/)
- [Full authentication guide](docs/guides/AUTHENTICATION.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with Python and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoint examples, request headers, environment variable guidance, and middleware configuration patterns.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
