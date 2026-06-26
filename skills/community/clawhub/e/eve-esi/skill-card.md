## Description: <br>
Query and manage EVE Online characters via the ESI (EVE Swagger Interface) REST API for character data, wallet balance, assets, skills, contracts, market orders, mail, industry jobs, killmails, planetary interaction, loyalty points, and related EVE account management tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[burnshall-ui](https://clawhub.ai/user/burnshall-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External EVE Online players and OpenClaw users use this skill to authenticate with EVE SSO, query ESI character and universe data, monitor planetary interaction, inspect market data, and configure alerts or reports. Developers can also use its scripts and JSON schema as a reusable ESI query and dashboard configuration helper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local agent may access private EVE character data such as wallet, assets, location, mail, contracts, and killmails. <br>
Mitigation: Grant only the minimum EVE SSO scopes needed for the task and review data requests before using authenticated endpoints. <br>
Risk: OAuth access and refresh tokens can expose an EVE account if pasted, logged, committed, or stored in an unsafe location. <br>
Mitigation: Use the local token store or environment-variable references, keep token files private, and do not paste, log, or commit real tokens. <br>
Risk: The raw ESI helper can make token-authorized account changes when write scopes are granted. <br>
Mitigation: Avoid write scopes unless account changes are intended and review endpoint paths, HTTP methods, and request bodies before execution. <br>
Risk: Telegram or Discord alert delivery can disclose EVE account information to configured channels. <br>
Mitigation: Configure notifications only for trusted bots, webhooks, and channels that should receive the selected alerts or reports. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/burnshall-ui/eve-esi) <br>
- [EVE SSO OAuth2 Authentication](references/authentication.md) <br>
- [EVE ESI Character Endpoints Reference](references/endpoints.md) <br>
- [Dashboard Config Schema](config/schema.json) <br>
- [Example Dashboard Config](config/example-config.json) <br>
- [EVE ESI API Explorer](https://developers.eveonline.com/api-explorer) <br>
- [EVE Developer Portal](https://developers.eveonline.com/applications) <br>
- [EVE ESI Swagger Spec](https://esi.evetech.net/latest/swagger.json) <br>
- [OpenClaw Docs](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated outputs depend on granted EVE SSO scopes; optional notifications may use Telegram or Discord channels configured by the user.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
