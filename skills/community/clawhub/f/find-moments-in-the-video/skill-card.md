## Description:

Find specific moments in a video using a natural language query, with optional exported clips, aspect ratios, captions, and AI reframing for online URLs or local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wayinvideo](https://clawhub.ai/user/wayinvideo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to locate specific scenes, topics, or events in videos from a natural language search query, then retrieve matching moment metadata or generated clip links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Videos, video URLs, natural language queries, and result metadata may be sent to WayinVideo or saved locally.

Mitigation: Use the skill only for material appropriate for third-party processing, prefer scoped or revocable WAYIN_API_KEY credentials, and review local api_results files before sharing or retaining them.

Risk: Exported clip links and project results are time-limited.

Mitigation: Use returned export links within 24 hours and rerun or refresh tasks according to the result metadata when links or projects expire.

## Reference(s):

- [WayinVideo Find Moments API documentation](https://wayin.ai/api-docs/find-moments/)
- [ClawHub skill page](https://clawhub.ai/wayinvideo/skills/find-moments-in-the-video)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and locally saved JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project IDs, local api_results JSON files, moment metadata, and time-limited exported clip links.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
