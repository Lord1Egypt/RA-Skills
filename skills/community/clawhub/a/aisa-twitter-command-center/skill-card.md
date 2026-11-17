## Description:

Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AIsa relay, then support approved posting workflows with OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill for Twitter/X research, monitoring, and content discovery, including profiles, timelines, mentions, trends, lists, communities, and Spaces. With explicit OAuth approval, it can also support publishing text, image, video, reply, and quote posts without requesting account passwords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OAuth/posting client may expose the configured AISA_API_KEY in normal command output.

Mitigation: Do not use a valuable key until the client masks secrets; keep authorize/post output out of shared logs and rotate the key if it appears in logs or transcripts.

Risk: Twitter/X search, OAuth, posting, and approved media uploads are relay-based and are sent to api.aisa.one.

Mitigation: Use the skill only when relay-based access is acceptable, and avoid sending sensitive content or media unless the user has approved that workflow.

Risk: Posting actions can publish externally visible content from the authorized account.

Mitigation: Require explicit user intent for publishing, replies, quotes, and media uploads, and do not report success until the publish command confirms completion.

## Reference(s):

- [AIsa Twitter OAuth Guide](references/post_twitter.md)
- [AIsa Homepage](https://aisa.one)
- [ClawHub Skill Page](https://clawhub.ai/baofeng-tech/skills/aisa-twitter-command-center)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with shell command examples and JSON-like command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Twitter/X search or profile data, OAuth authorization links, publish status, tweet IDs or URLs, and relay error details.]

## Skill Version(s):

1.0.3 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
