## Description:

Analyzes Douyin short-video links to explain why a video may be viral, including audience reach, engagement signals, content hooks, visual framing, and viewer behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[csak47mu](https://clawhub.ai/user/csak47mu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content analysts use this skill by sending a Douyin link to receive a structured Markdown breakdown of video metadata, engagement metrics, visual content, viral drivers, audience profile, behavioral psychology, and reusable content patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch Douyin pages and media with weak request scoping.

Mitigation: Restrict requests to known Douyin and media hosts, and require user confirmation before following unfamiliar or redirected links.

Risk: Video downloads and frame extraction can create temporary media files containing user-provided content.

Mitigation: Run the skill in a sandbox, limit file size and duration, and delete downloaded videos and extracted frames after analysis.

Risk: Third-party parsing or vision services may receive video frames or metadata.

Mitigation: Require explicit consent before external uploads and disclose when third-party services are used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/csak47mu/skills/douyin-viral-breakdown)

## Skill Output:

**Output Type(s):** [markdown, text, code, shell commands, guidance]

**Output Format:** [Markdown report with tables and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extracted Douyin metadata, engagement-rate calculations, visual-frame analysis, audience and behavior analysis, and reusable content formulas.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
