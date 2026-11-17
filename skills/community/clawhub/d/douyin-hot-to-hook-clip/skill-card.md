## Description:

Creates short talking-hook videos from public Douyin hot-search topics and seller-selected still images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers use this skill to turn a selected public Douyin trend and presenter or product stills into individual talking-hook clips for social content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shared Beatra authorization can permit paid image and music generation beyond this clip workflow.

Mitigation: Review the broader authorization before connecting and proceed only if those additional paid capabilities are acceptable; revoke device access in the Beatra Console when no longer needed.

Risk: Selected photos and voice samples leave the computer, and installation metadata is reported automatically.

Mitigation: Share only media you have permission to use, avoid sensitive photos or voice samples, and consider the metadata disclosure before installing.

Risk: Paid speech and video generation can consume account credits.

Mitigation: Review the current price and obtain approval before each paid task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/douyin-hot-to-hook-clip)
- [Beatra skill page](https://beatra.ai/skills/douyin-hot-to-hook-clip)
- [Workflow](references/workflow.md)
- [Trend lookup](references/trend-lookup.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Updates and security](references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Text, Audio, Video, Files]

**Output Format:** [Talking-hook scripts and short video media files.]

**Output Parameters:** [2–15 seconds per clip; 2–8 clips per request; one still per clip.]

**Other Properties Related to Output:** [Clips are delivered separately, not stitched together; available MIME type, duration, size, and actual credits charged are reported.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
