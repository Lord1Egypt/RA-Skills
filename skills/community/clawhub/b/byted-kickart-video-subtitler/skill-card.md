## Description:

Adds and embeds subtitles into video files through a Volcengine Kickart workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to upload a video, prepare subtitle timing data from text, SRT, or timestamped input, and submit a Volcengine Kickart task that returns a subtitled video link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles cloud credentials for Volcengine API access.

Mitigation: Use scoped temporary credentials, keep long-lived AK/SK values out of chat, and sanitize logs before sharing them.

Risk: The skill can receive an update command from a remote service.

Mitigation: Do not run returned update commands until the command and target version are independently verified.

Risk: The skill uploads and processes user media through remote services.

Mitigation: Use a private skill-specific working directory and review media sensitivity, account scope, and retention expectations before processing sensitive files.

Risk: Some Python dependencies are specified with open lower bounds.

Mitigation: Pin and review dependencies in controlled environments before commercial deployment.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/volcengine-skills/skills/byted-kickart-video-subtitler)
- [Publisher profile](https://clawhub.ai/user/volcengine-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON subtitle configuration and result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a subtitle configuration JSON file and a result JSON file containing the subtitled video URL; documented limits include 3000 caption characters, 50 MB video size, and 10 minute video duration.]

## Skill Version(s):

1.0.9 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
