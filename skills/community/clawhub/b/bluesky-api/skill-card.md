## Description: <br>
Read, search, post, and monitor Bluesky (AT Protocol) accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minupla](https://clawhub.ai/user/minupla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to read Bluesky profiles, search posts, monitor accounts, and create Bluesky posts through AT Protocol API calls and helper scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The posting quick reference contains a stale credential argument form that could encourage app passwords to be passed through shell history or process arguments. <br>
Mitigation: Use only a Bluesky app password supplied through BSKY_APP_PASSWORD or a protected secret mechanism, and verify examples use handle and text arguments only. <br>
Risk: Authenticated posting can publish content to a Bluesky account. <br>
Mitigation: Require explicit user approval before creating any public post. <br>


## Reference(s): <br>
- [ClawHub Bluesky API Skill](https://clawhub.ai/minupla/bluesky-api) <br>
- [Bluesky App Passwords](https://bsky.app/settings/app-passwords) <br>
- [Bluesky Author Feed Endpoint](https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=alice.bsky.social&limit=5) <br>
- [Bluesky Search Posts Endpoint](https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=openclaw&limit=10) <br>
- [Bluesky Session Endpoint](https://bsky.social/xrpc/com.atproto.server.createSession) <br>
- [Bluesky Create Record Endpoint](https://bsky.social/xrpc/com.atproto.repo.createRecord) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read and search operations use public endpoints; authenticated posting requires a Bluesky app password supplied through BSKY_APP_PASSWORD or another protected secret mechanism.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
