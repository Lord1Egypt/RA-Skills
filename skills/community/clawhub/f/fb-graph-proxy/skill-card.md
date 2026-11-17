## Description:

尤里改 Facebook Graph API 代理服务使用指南

This skill is ready for commercial/non-commercial use.

## Publisher:

[evte](https://clawhub.ai/user/evte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advertisers use this skill to route Facebook Graph API requests through baiz.ai's proxy by replacing the Graph API host and authenticating with a baiz.ai bearer token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes broad Facebook Graph API access through a third-party proxy that injects stored Facebook tokens.

Mitigation: Use only accounts and baiz.ai tokens with the minimum needed permissions, and confirm how baiz.ai stores Facebook authorizations and logs requests before use.

Risk: Supported write, delete, and upload operations could affect production Facebook assets or business data.

Mitigation: Test with non-production or low-risk accounts first, and avoid destructive or production operations until tenant isolation, token revocation, upload handling, and data-retention controls are clear.

## Reference(s):

- [baiz.ai](https://baiz.ai)
- [ClawHub skill page](https://clawhub.ai/evte/skills/fb-graph-proxy)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, API Calls]

**Output Format:** [Markdown with HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIZ_API_TOKEN as a sensitive credential.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
