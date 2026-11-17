## Description:

Query and manage EVE Online characters via the ESI (EVE Swagger Interface) REST API with OAuth2/PKCE authentication, local token refresh, read-only defaults, and explicit opt-in for account-changing requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[burnshall-ui](https://clawhub.ai/user/burnshall-ui)

### License/Terms of Use:

MIT-0

## Use Case:

EVE Online players and agent operators use this skill to authenticate characters, query ESI character and universe data, inspect wallet, assets, skills, planetary interaction, industry, market, and route information, and validate dashboard-style configuration. It is suitable for public ESI lookups and user-approved account data access where the operator grants only the scopes needed for the task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth refresh tokens provide long-lived account access if exposed.

Mitigation: Store tokens locally, prefer esi_query.py --char so tokens stay out of argv and shell history, avoid putting tokens in config files or logs, and install from a reviewed release.

Risk: Overbroad EVE scopes can expose private wallet, mail, asset, location, and character data.

Mitigation: Grant only the EVE scopes needed for the task, start with the narrowest suitable scope profile, and re-authenticate only when a missing scope is required.

Risk: Account-changing ESI operations can modify in-game state when explicitly enabled.

Mitigation: Keep the read-only default for normal use and require deliberate user approval before using write scopes or --allow-write.

Risk: Optional notification channels may forward user-defined alert text to third-party services.

Mitigation: Configure Telegram or Discord only when needed and avoid sending raw wallet, asset, mail, token, or credential data in alert templates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/burnshall-ui/skills/eve-esi)
- [Authentication reference](references/authentication.md)
- [Endpoint reference](references/endpoints.md)
- [EVE ESI API Explorer](https://developers.eveonline.com/api-explorer)
- [EVE Developer Portal](https://developers.eveonline.com/applications)
- [ESI OpenAPI specification](https://esi.evetech.net/meta/openapi.json)
- [ESI compatibility dates](https://esi.evetech.net/meta/compatibility-dates)
- [ESI changelog](https://esi.evetech.net/meta/changelog)
- [OpenClaw Docs](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public ESI endpoints can run without authentication; authenticated output depends on user-granted EVE SSO scopes.]

## Skill Version(s):

1.3.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
