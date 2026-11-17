## Description:

Generates Chinese short-video scripts for Douyin, Xiaohongshu, and WeChat Channels with opening hooks, shot-by-shot scenes, dialogue, music cues, and filming tips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and agents use this skill to draft Chinese short-video scripts for product promotion, knowledge sharing, tutorials, story formats, and direct-to-camera videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script may send user topics and script parameters to OpenAI automatically when OPENAI_API_KEY is present.

Mitigation: Review or modify scripts/video_script.py before execution, run without OPENAI_API_KEY, or remove the AI generation path unless external API use is intended.

Risk: The skill and outputs are designed for Chinese-language short-video scripting.

Mitigation: Use only when reviewers can evaluate Chinese content and platform-specific marketing claims before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-short-video-script)
- [AISoBrand website](https://aisobrand.com)
- [AISoBrand free diagnosis](https://aisobrand.com/free-diagnosis.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese markdown-style script text with structured sections and optional CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate through templates locally or use OpenAI when the optional helper script detects OPENAI_API_KEY.]

## Skill Version(s):

1.2.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
