## Description:

Analyzes local or remote videos with the Doubao 2.0 model when the agent has a video path or video URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielcy](https://clawhub.ai/user/danielcy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send a local video file or remote video URL to Volcengine Ark for prompt-guided visual content analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local videos or remote video URLs are sent to Volcengine Ark for processing.

Mitigation: Use the skill only for videos that are approved for third-party processing, and avoid sensitive, confidential, or unauthorized content.

Risk: The script requires ARK_API_KEY and exposes that credential to the active runtime.

Mitigation: Run the skill in an isolated environment, scope the key appropriately, and avoid logging or sharing the key.

Risk: The setup instructions install an unpinned SDK into the active Python environment.

Mitigation: Use a virtual environment and pin a reviewed volcengine-python-sdk[ark] version before deployment.

Risk: Remote videos may be downloaded into the workspace when direct remote parsing fails.

Mitigation: Delete downloaded workspace video files after use and apply normal workspace data-handling controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielcy/skills/doubao-video-analyzer)
- [Volcengine Ark API endpoint](https://ark.cn-beijing.volces.com/api/v3)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text or SDK response printed to stdout, with agent-authored Markdown when presenting analysis results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ARK_API_KEY and Python with volcengine-python-sdk[ark].]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
