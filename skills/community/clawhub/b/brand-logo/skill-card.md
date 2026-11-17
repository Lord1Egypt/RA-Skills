## Description:

Retrieves a public-domain brand logo image or keyless JSON logo result for one supplied domain through ReplyNodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[replynodes-ai](https://clawhub.ai/user/replynodes-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agents use this skill to retrieve a logo for one known public website domain without an account or API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A requested domain is sent to ReplyNodes over the network.

Mitigation: Use public domains only; avoid private hostnames and bulk crawling.

Risk: A fallback favicon or placeholder can be mistaken for a verified brand logo.

Mitigation: Check the fallback indicator and report placeholders honestly.

Risk: Public logo retrieval does not grant rights to reuse the image.

Mitigation: Retain the source domain and confirm trademark or copyright permissions before reuse.

Risk: Optional authenticated routes require an API key.

Mitigation: Use keyless logo routes by default; if broader routes are needed, store the key securely and never expose or log it.

## Reference(s):

- [ReplyNodes logo image endpoint](https://img.replynodes.com)
- [ReplyNodes keyless logo JSON endpoint](https://api.replynodes.com/v1/brand/logo)
- [ReplyNodes MCP endpoint for optional authenticated operations](https://mcp.replynodes.com/mcp)
- [ReplyNodes authentication guide](https://docs.replynodes.com/docs/auth)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Images, JSON]

**Output Format:** [Markdown guidance with GET examples; retrieved image bytes or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single public domain; image results may be favicons or placeholders.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence; skill frontmatter still lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
