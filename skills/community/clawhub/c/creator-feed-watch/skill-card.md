## Description:

Track YouTube creators and analyze video content. Paste a YouTube link to get an AI-powered breakdown (summary, key points, why it matters), then optionally follow the creator for new upload notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glin23](https://clawhub.ai/user/glin23)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze YouTube videos, follow creators, check for new uploads, and prepare concise notification cards from upload metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcript caption retrieval can be steered to request arbitrary caption URLs from the user's environment.

Mitigation: Restrict caption fetches to legitimate YouTube or Google caption hosts before using the skill in environments with access to internal services or private networks.

Risk: The skill stores followed creators locally and may send upload metadata through a configured notification adapter.

Mitigation: Install only when local watchlist storage and configured notification delivery are acceptable; review the watchlist path and delivery target before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/glin23/skills/creator-feed-watch)
- [OpenClaw skill installation](https://openclawdoc.com/docs/skills/installation)
- [OpenClaw skill creation](https://openclawdoc.com/docs/skills/creating-skills/)
- [OpenClaw ClawHub publishing](https://openclawdoc.com/docs/skills/clawhub/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration]

**Output Format:** [Markdown analysis cards and structured JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include transcript text, video metadata, watchlist records, notification payloads, delivery status, and human-readable status messages.]

## Skill Version(s):

0.2.0 (source: frontmatter, manifest.yaml, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
