## Description:

Comprehensive reference for Douyin mini-game server-side OpenAPI, covering backend HTTPS API usage for access tokens, login sessions, user storage, QR codes, subscription messages, gift redemption, links, sharing, group tags, and related mgplatform endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wufengsheng](https://clawhub.ai/user/wufengsheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and backend engineers use this skill when building or debugging Douyin mini-game server integrations. It helps them look up authentication flows, request formats, SDK options, endpoint behavior, limits, errors, and safe handling practices for server-side API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill discusses AppSecret, access_token, session_key, login codes, signatures, and user identifiers that can expose accounts or users if mishandled.

Mitigation: Keep credentials and identifiers server-side, store them in secret management, avoid logging them, and never send AppSecret or session_key to clients.

Risk: Messaging, cloud storage, session reset, and data removal examples can affect users or their stored data.

Mitigation: Require user-directed control and appropriate consent before invoking messaging, storage, remove, or reset operations.

Risk: API examples and limits may become stale or incomplete compared with the live Douyin platform.

Mitigation: Confirm implementation details against the official Douyin documentation before production use.

## Reference(s):

- [Douyin mini-game server OpenAPI documentation](https://developer.open-douyin.com/docs/resource/zh-CN/mini-game/develop/server/)
- [Server API overview](references/server-overview.md)
- [Access token APIs](references/server-auth.md)
- [Login and session APIs](references/server-login.md)
- [User data storage APIs](references/server-data.md)
- [QR code API](references/server-qrcode.md)
- [Messaging APIs](references/server-message.md)
- [Other server capabilities](references/server-other.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with API reference tables, code examples, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; users must supply and protect their own Douyin app credentials and user identifiers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
