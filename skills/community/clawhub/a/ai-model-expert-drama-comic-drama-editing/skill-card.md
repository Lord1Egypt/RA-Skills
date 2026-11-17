## Description:

AI大模型专家｜AI漫剧剪辑 helps short-drama, comic-drama, advertising, ecommerce, media-buying, and operations teams turn existing assets into rough cuts, refined edits, aspect-ratio variants, and original rewrites based on authorized reference structures through local ffmpeg helpers and AI-HIVE generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editing teams, ecommerce teams, and developers use this skill to plan AI comic-drama and short-drama editing workflows, inspect source media, produce cut and aspect-ratio commands, generate project blueprints, and submit image or video generation tasks through AI-HIVE.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses AI-HIVE credentials and allows endpoint configuration, so a broad API key or untrusted base URL can expand account or data exposure.

Mitigation: Use a dedicated, limited AI-HIVE API key, avoid custom base URLs unless the host is controlled and trusted, and check AI_HIVE_BASE_URL and ~/.ai-hive/config.json before generation.

Risk: Selected local media files may be uploaded to AI-HIVE for image, video, or reference-based generation.

Mitigation: Upload only media the user is authorized to share and avoid sensitive, confidential, or unlicensed assets.

Risk: The documented dependency install is unpinned and global.

Mitigation: Install dependencies in a virtual environment and pin versions for deployment review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-comic-drama-editing)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON files, edited media files, downloaded generated media, task status JSON, and AI-HIVE media IDs.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
