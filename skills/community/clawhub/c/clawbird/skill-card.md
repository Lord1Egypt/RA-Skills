## Description:

X/Twitter integration for posting, replying, searching, liking, following, direct messages, and mentions through the official X API v2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xonder](https://clawhub.ai/user/xonder)

### License/Terms of Use:


## Use Case:

Developers and operators use Clawbird to let an agent interact with an authenticated X account for social posting, engagement, search, mentions, direct messages, and cost review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime code is installed from the @xonder/clawbird npm package and can receive powerful X account and direct-message access.

Mitigation: Review or pin the exact npm package version before installation and grant only the X API scopes needed for the intended workflow.

Risk: Posting, replying, liking, following, and sending direct messages modify remote state on the authenticated X account.

Mitigation: Require explicit approval for tweets, replies, likes, follows, and direct messages, especially during autonomous operation.

Risk: Direct-message reading can expose sensitive private conversations to the agent.

Mitigation: Treat direct-message access as sensitive and avoid enabling it for general autonomous read-only workflows unless it is specifically required.

## Reference(s):

- [Clawbird ClawHub listing](https://clawhub.ai/xonder/skills/clawbird)
- [@xonder/clawbird npm package](https://www.npmjs.com/package/@xonder/clawbird)
- [X Developer Portal](https://developer.x.com)
- [Official X API v2 endpoint reference](https://api.x.com/2/tweets)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON tool results and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool results include estimated API cost, returned X data, action status, and error details when applicable.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
