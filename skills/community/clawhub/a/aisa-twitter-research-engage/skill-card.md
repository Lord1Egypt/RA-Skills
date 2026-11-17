## Description:

Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa for research, monitoring, and approved engagement workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to research X/Twitter profiles, tweets, trends, conversations, lists, communities, and Spaces, then perform approved posting or engagement actions through AIsa-backed command-line clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose AISA_API_KEY in normal command output and logs.

Mitigation: Use a scoped or disposable AISA_API_KEY, avoid running status, authorize, or post commands where output is logged, and rotate the key if it is disclosed.

Risk: Credentialed relay requests can be sent to a configurable TWITTER_RELAY_BASE_URL.

Mitigation: Use the default AIsa relay or only a fully trusted HTTPS relay endpoint; do not set custom relay URLs for untrusted destinations.

Risk: Posting, media upload, likes, follows, and unfollows are live actions on the connected X/Twitter account.

Mitigation: Require explicit user approval for posting and engagement actions, and report success only after the API confirms the action.

## Reference(s):

- [AIsa Twitter Engagement](references/engage_twitter.md)
- [AIsa Twitter OAuth](references/post_twitter.md)
- [ClawHub Skill Page](https://clawhub.ai/aisadocs/skills/aisa-twitter-research-engage)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON client outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and may return authorization links, Twitter/X research data, publish results, or engagement action results.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
