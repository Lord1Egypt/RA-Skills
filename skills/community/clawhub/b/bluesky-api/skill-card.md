## Description:

Read, search, post, and monitor Bluesky (AT Protocol) accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minupla](https://clawhub.ai/user/minupla)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to read Bluesky profile feeds, search posts, publish authenticated posts, and monitor accounts through AT Protocol APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Posting guidance can expose or accidentally publish a Bluesky app password if credentials are handled incorrectly.

Mitigation: Use a Bluesky app password, not the main account password, and provide it only through a secure environment variable or configuration path.

Risk: Authenticated posting can publish content to a Bluesky account.

Mitigation: Review the posting command and final post text before execution, especially in automated workflows.

## Reference(s):

- [ClawHub Bluesky API Skill](https://clawhub.ai/minupla/skills/bluesky-api)
- [Bluesky App Passwords](https://bsky.app/settings/app-passwords)
- [Bluesky Author Feed API](https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed)
- [Bluesky Search Posts API](https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts)
- [AT Protocol Create Session API](https://bsky.social/xrpc/com.atproto.server.createSession)
- [AT Protocol Create Record API](https://bsky.social/xrpc/com.atproto.repo.createRecord)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; authenticated posting requires a Bluesky app password.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
