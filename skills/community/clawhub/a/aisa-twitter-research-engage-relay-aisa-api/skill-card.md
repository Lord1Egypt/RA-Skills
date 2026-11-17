## Description:

Runs Twitter/X research, likes, follows, replies, and OAuth-gated posting through AIsa for explicit, approved engagement workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research known Twitter/X targets, then carry out reviewed engagement actions such as likes, follows, replies, quotes, posts, and approved media uploads through AIsa.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AIsa API key can be exposed to the local agent environment or command output.

Mitigation: Use a key intended for agent use, avoid logging command output that may contain secrets, and rotate the key if exposure is suspected.

Risk: Selected local media paths are read and uploaded through a third-party relay.

Mitigation: Pass only media files the user explicitly selected for upload and confirm that the files are intended for Twitter/X publication.

Risk: Likes, follows, unfollows, replies, quotes, and posts are real public account actions.

Mitigation: Require explicit user approval for each target and do not report success until the relay confirms the action.

## Reference(s):

- [AIsa Twitter Engagement](references/engage_twitter.md)
- [AIsa Twitter OAuth](references/post_twitter.md)
- [AIsa homepage](https://aisa.one)
- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/aisa-twitter-research-engage-relay-aisa-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and sends Twitter/X read, engagement, OAuth, posting, and selected media-upload requests through AIsa.]

## Skill Version(s):

1.0.6 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
