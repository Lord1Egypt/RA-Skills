## Description:

Automates Douyin video download, watermark removal, remix-based deduplication, and audio removal from Douyin URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanxueda](https://clawhub.ai/user/hanxueda)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to process Douyin video URLs into deduplicated, muted MP4 files for workflows where the user has rights to process the source media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads remote media and may contact unexpected URLs if supplied a crafted link.

Mitigation: Run only with trusted Douyin URLs in a network-restricted environment until URL validation is tightened.

Risk: The skill removes watermarks and remixes videos, which can create rights or platform-policy concerns.

Mitigation: Use only for videos the user has rights to process and review outputs before redistribution.

Risk: The skill writes processed MP4 files under ~/video-dedup/output and temporary files under ~/video-dedup/workspace.

Mitigation: Run in an environment where those paths are acceptable and review available storage before processing large or sensitive media.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Files, Text]

**Output Format:** [Command-line status text and MP4 video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes processed MP4 files under ~/video-dedup/output and temporary processing files under ~/video-dedup/workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
