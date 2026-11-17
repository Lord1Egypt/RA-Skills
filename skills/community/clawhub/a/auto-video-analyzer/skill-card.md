## Description:

Auto Video Analyzer helps an agent analyze video content by extracting key frames with FFmpeg and using AI vision to produce a structured report across Windows, macOS, and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shishenbaiye](https://clawhub.ai/user/shishenbaiye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, QA teams, and other external users can use this skill to summarize video content, inspect UI or gameplay recordings, and debug visible behavior by sampling frames and returning a structured visual analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs GitHub-hosted scripts without version pinning or integrity checks.

Mitigation: Review the downloaded scripts before execution, prefer pinned release URLs, and verify file integrity when deploying in managed environments.

Risk: Private or sensitive video frames may be extracted and analyzed.

Mitigation: Use only videos approved for the target AI environment, remove sensitive content before analysis, and clean temporary analysis files after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shishenbaiye/skills/auto-video-analyzer)
- [GitHub Repository](https://github.com/shishenbaiye/auto-video-analyzer)
- [Tool Scripts](https://github.com/shishenbaiye/auto-video-analyzer/tree/main/tools)
- [GitHub Releases](https://github.com/shishenbaiye/auto-video-analyzer/releases)
- [GitHub Issues](https://github.com/shishenbaiye/auto-video-analyzer/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with structured video analysis and inline shell commands when setup or execution steps are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FFmpeg and platform-specific shell support; frame counts vary by analysis mode.]

## Skill Version(s):

1.0.0 (source: server release, skill metadata, README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
