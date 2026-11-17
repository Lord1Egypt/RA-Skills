## Description:

Run Twitter/X research, monitoring, watchlists, and OAuth-gated posting through AIsa for trend tracking, competitor monitoring, and approved posting workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research Twitter/X activity, monitor keywords or watchlists, and publish approved posts through an OAuth relay without sharing Twitter passwords or cookies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AIsa API key exposure in normal command output.

Mitigation: Use a limited-scope or non-production AISA_API_KEY where possible and avoid sharing logs or transcripts that include command output until key redaction is confirmed.

Risk: Twitter/X queries, tweet content, IDs, and uploaded media are sent to AIsa services.

Mitigation: Install only when the user trusts AIsa with that data and clearly disclose that requests go to https://api.aisa.one.

Risk: Local media upload can send user-provided image or video files to the relay.

Mitigation: Pass only media files the user explicitly selected for upload, and verify the path before invoking --media-file.

## Reference(s):

- [AIsa Twitter ClawHub listing](https://clawhub.ai/bibaofeng/skills/aisa-twitter)
- [AIsa homepage](https://aisa.one)
- [AIsa API endpoint](https://api.aisa.one)
- [AIsa Twitter OAuth reference](references/post_twitter.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and network access to https://api.aisa.one; posting can upload user-approved local image or video files.]

## Skill Version(s):

1.0.5 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
