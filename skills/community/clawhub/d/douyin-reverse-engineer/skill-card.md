## Description:

Analyzes Douyin or local video inputs to reverse-engineer AI image prompts, scene-by-scene storyboard scripts, and optional game-style rewrites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clair-001](https://clawhub.ai/user/clair-001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to download or analyze video content, generate structured scene breakdowns, and produce AI image prompts or storyboard tables for creative workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User videos and derived analysis may be sent to external Volcengine/Ark services during video analysis.

Mitigation: Use only videos suitable for external processing and review applicable data-handling requirements before running the skill.

Risk: Douyin identifiers may be handled through TikHub-related downloader code when downloading Douyin videos.

Mitigation: Review the downloader dependency before use and prefer local-video analysis when external downloader handling is not acceptable.

Risk: The skill relies on unpinned third-party skill dependencies.

Mitigation: Pin and review dependency versions, including the missing douyin-downloader dependency, before deployment.

Risk: Running with a broad environment could expose unrelated local secrets to subprocesses or dependencies.

Mitigation: Run with a minimal environment containing only the required ARK_API_KEY secret.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clair-001/skills/douyin-reverse-engineer)
- [Publisher profile](https://clawhub.ai/user/clair-001)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, CSV, and console text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write analysis.json, storyboard Markdown and CSV files, prompt Markdown files, downloaded video files, and optional rewritten variants.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
