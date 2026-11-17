## Description:

Build secure authentication with sessions, JWT, OAuth, passwordless, MFA, and SSO for web and mobile apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this reference skill to choose and adapt authentication patterns for login flows, token strategies, password security, OAuth and OIDC integration, MFA, SSO, and framework middleware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copying the OAuth, OIDC, middleware, or session examples directly into production could leave token verification, session validation, or account-linking checks incomplete.

Mitigation: Treat examples as checklists and replace them with implementation patterns that verify tokens fully, validate sessions cryptographically or through a trusted server-side store, and require authenticated confirmation before linking accounts.

Risk: The skill discusses high-impact authentication controls, so incorrect adaptation could put user accounts at risk.

Mitigation: Use the guidance as design support only, review changes against current provider and framework documentation, and security-review authentication code before deployment.

## Reference(s):

- [ClawHub Auth skill page](https://clawhub.ai/ivangdavila/skills/auth)
- [Auth skill homepage](https://clawic.com/skills/auth)
- [Authentication Strategies](artifact/strategies.md)
- [Password Handling](artifact/passwords.md)
- [Multi-Factor Authentication](artifact/mfa.md)
- [OAuth and Social Login](artifact/oauth.md)
- [Framework Middleware](artifact/middleware.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with reference code examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; examples are not executed by the agent.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
