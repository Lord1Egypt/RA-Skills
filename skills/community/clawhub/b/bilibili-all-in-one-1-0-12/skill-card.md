## Description:

A comprehensive Bilibili toolkit that integrates hot trending monitoring, video downloading, video watching/playback, subtitle downloading, and video publishing capabilities into a single skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollowings](https://clawhub.ai/user/hollowings)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor Bilibili trends, inspect video metrics, download videos or subtitles, retrieve playback information, and manage Bilibili publishing workflows from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive Bilibili session cookies for authenticated downloads and publishing.

Mitigation: Use a test Bilibili account, avoid providing cookies unless authenticated features are required, prefer environment variables or in-memory parameters, and run the skill in an isolated environment.

Risk: Publishing actions can upload, edit, schedule, draft, or delete videos on a real Bilibili account.

Mitigation: Review every publishing or deletion request before execution and verify the target account, video ID, files, title, tags, schedule time, and other metadata.

Risk: Security guidance reports that cookies may be sent when fetching an unvalidated subtitle URL.

Mitigation: Do not use subtitle downloading with credentials until URL validation and unauthenticated subtitle fetching are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hollowings/skills/bilibili-all-in-one-1-0-12)
- [Project homepage](https://github.com/wscats/bilibili-all-in-one)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with CLI/Python examples, JSON-like action results, playback URLs, downloaded media files, subtitle files, and publishing status messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may make HTTPS requests to Bilibili and YouTube oEmbed endpoints and may write downloaded videos, audio, subtitles, or converted subtitle files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and artifact metadata identify upstream skill version 1.0.12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
