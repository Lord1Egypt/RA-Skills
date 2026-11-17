## Description:

Generates video and article content ideas from trending topics, user preferences, and platform style cues for Douyin, Xiaohongshu, Bilibili, Zhihu, and related content channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nh5gntnf78-oss](https://clawhub.ai/user/nh5gntnf78-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, marketing teams, media operators, and businesses use this skill to generate topic lists, angles, expected popularity, and platform-adapted ideas for video or article planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated topic suggestions may rely on trend claims or expected popularity estimates that are stale, simplified, or unsupported by live data.

Mitigation: Review ideas against current platform trends and require citation or confirmation before publishing time-sensitive content.

Risk: The skill describes optional saving, Tencent Docs or Excel export, cron scheduling, and video-generation chaining workflows that can affect files or downstream publication processes.

Mitigation: Require user confirmation before writing files, exporting to external services, scheduling recurring runs, or invoking downstream generation and publishing skills.

Risk: The packaged script uses preset hot topics, so its behavior may be less capable than the advertised multi-platform trend-gathering workflow.

Mitigation: Treat script output as draft planning material and validate any live-trend requirements with approved search or trend-tracking tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nh5gntnf78-oss/skills/content-idea-generator)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-style content idea lists, with optional local Markdown or JSON files from the packaged Python script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ideas may include titles, angles, target platform, expected views, difficulty, rationale, and timestamps.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
