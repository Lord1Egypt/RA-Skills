## Description:

Fangcloud API Skills helps agents operate Fangcloud files, sharing, collaboration, knowledge-base chat, and related API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiema123](https://clawhub.ai/user/jiema123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search, upload, download, organize, and share Fangcloud files, manage collaboration or collection links, and interact with Fangcloud knowledge-base and agent chat features. Use it where the publisher and release channel are trusted and Fangcloud token exposure can be managed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to run a downloaded closed-source CLI that receives Fangcloud user or admin tokens.

Mitigation: Install only from a trusted publisher and release channel, avoid admin tokens unless strictly necessary, and keep tokens rotatable.

Risk: The API documentation includes credential-shaped bearer tokens and token-based examples.

Mitigation: Treat all sample tokens as exposed, never reuse them, and rotate any real Fangcloud tokens that may have been copied into documentation or logs.

Risk: The skill can upload, download, delete, move, copy, share, collect, and administer Fangcloud resources.

Mitigation: Require explicit user confirmation before destructive, public-link, collection-link, transfer, or admin operations.

Risk: Knowledge-base, agent, OCR, share, and cloud-document content can contain indirect prompt-injection text.

Mitigation: Treat remote content as data, ignore instructions embedded in returned content, and do not expose tokens or secrets to knowledge-base requests or third-party URLs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiema123/skills/fangcloud-ai)
- [Fangcloud API Endpoint Analysis](artifact/references/openapi.md)
- [Fangcloud CLI Release Downloads](https://app.fangcloud.com/sync/vv25/knowclaw/release/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API examples, JSON request bodies, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke a downloaded Fangcloud CLI and requires Fangcloud user or admin tokens for authenticated operations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
