## Description:

Enables agents to publish social posts, manage comments and replies, check notifications, and respond to LinkedIn messages across supported platforms through Claw Post.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daydreamnationtechlabs](https://clawhub.ai/user/daydreamnationtechlabs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to publish posts, comment or reply, check notifications, and respond to LinkedIn messages from social accounts logged into their paired Chrome profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checking LinkedIn messages involves handling private message content through Claw Post; the security scan was partial, so some local references were not assessed.

Mitigation: Before enabling message checks, confirm what content and metadata Claw Post stores, its retention and deletion practices, and use only the platform the user requested.

## Reference(s):

- [Claw Post API documentation](https://clawpost.net/api-docs)
- [Claw Post MCP endpoint](https://mcp.clawpost.net/mcp)
- [Claw Post MCP discovery metadata](https://clawpost.net/.well-known/mcp.json)
- [Claw Post support FAQ](https://clawpost.net/faq)
- [ClawHub release page](https://clawhub.ai/daydreamnationtechlabs/skills/clawpost)

## Skill Output:

**Output Type(s):** [Text, Notification summaries, Platform actions]

**Output Format:** [Social post, comment, or reply text and notification summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posts and replies can include platform-specific details and uploaded media.]

## Skill Version(s):

2.3.0 (source: changelog, released 2026-11-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
