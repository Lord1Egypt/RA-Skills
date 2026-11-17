## Description:

Post to Instagram, TikTok, YouTube Shorts, LinkedIn, Facebook, Threads, and Bluesky via the Postmoore API. Schedule posts, upload media, save drafts, and manage content autonomously.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rkotchamp](https://clawhub.ai/user/rkotchamp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media managers, and developers use this skill to prepare, schedule, publish, upload media for, draft, list, and manage social posts across connected Postmoore accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, upload, or delete content on connected social accounts.

Mitigation: Ask the agent to draft first and require explicit approval before posting, uploading, or deleting.

Risk: A live Postmoore API key can be exposed through shell history, shared workspaces, or plaintext setup storage.

Mitigation: Prefer an environment variable or credential manager, avoid storing keys in shared workspaces, and rotate any key that may have been exposed.

## Reference(s):

- [Postmoore](https://postmoo.re)
- [Postmoore API base URL](https://postmoo.re/api/v1)
- [ClawHub skill page](https://clawhub.ai/rkotchamp/skills/agent-postmoore)
- [ClawHub publisher profile](https://clawhub.ai/user/rkotchamp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline HTTP examples, shell commands, and JSON API response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a POSTMOORE_API_KEY; the video workflow also references ffmpeg.]

## Skill Version(s):

1.0.0 (source: server release metadata); artifact frontmatter reports 1.1.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
