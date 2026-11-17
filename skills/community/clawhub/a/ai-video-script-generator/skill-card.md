## Description:

Generates structured video scripts for Douyin, Xiaohongshu, and Bilibili, including opening hooks, scene outlines, dialogue copy, BGM suggestions, cover text, hashtags, and posting-time suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nh5gntnf78-oss](https://clawhub.ai/user/nh5gntnf78-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and social media operators use this skill to draft platform-specific video scripts from a topic, platform, style, and duration. It is intended for Chinese social video workflows that need repeatable script structure, hooks, storyboard timing, and publishing copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated topics, scripts, and style history may be retained locally under ~/video-scripts by default, including confidential topics, client campaigns, or unpublished content.

Mitigation: Review topics before running the skill, use a non-sensitive output directory when possible, and delete retained history or memory files when local retention is not desired.

Risk: The server security verdict is suspicious because the skill saves generated outputs and a running topic/style history without clear opt-out or deletion guidance.

Mitigation: Review the skill before installation and document local cleanup expectations for users who handle sensitive content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nh5gntnf78-oss/skills/ai-video-script-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown video script printed as text and saved as a local .md file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform, duration, style, hook, storyboard table, cover text, hashtags, and recommended posting times.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
