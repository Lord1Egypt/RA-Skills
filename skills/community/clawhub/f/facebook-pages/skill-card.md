## Description:

Manage Facebook Pages, posts, comments, messages, and insights via the Facebook Graph API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Page managers and their agents use this skill to publish content, moderate comments, respond to messages, and review engagement insights. They can also read public Facebook data without connecting an account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting a Facebook account grants access to managed Pages according to approved permissions.

Mitigation: Review the requested permissions during the ClawLink and Facebook connection flow.

Risk: Public-data lookups consume paid ClawLink credit even without a connected Facebook account.

Mitigation: Check whether a public-data lookup is needed before making a paid call.

Risk: Publishing, messaging, updating, or deleting can affect public content or real users.

Mitigation: Preview the target and intended effect, then obtain explicit user confirmation before executing a write.

## Reference(s):

- [Facebook skill on ClawHub](https://clawhub.ai/hith3sh/skills/facebook-pages)
- [Facebook Graph API documentation](https://developers.facebook.com/docs/graph-api/)
- [ClawLink documentation](https://docs.claw-link.dev/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
