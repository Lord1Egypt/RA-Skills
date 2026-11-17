## Description:

AI大模型专家｜AI短剧智能剪辑 helps short-drama, comics, advertising, ecommerce, and performance marketing teams turn authorized media into editing plans, ffmpeg commands, aspect-ratio variants, and AI-HIVE generation prompts for original rewritten versions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editing teams, and developers use this skill to plan and execute short-drama or ecommerce video edits, including source probing, rough and fine cuts, aspect-ratio conversion, loudness normalization, authorized reference analysis, and AI-HIVE image/video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API keys and can use custom API base URLs.

Mitigation: Use a dedicated, revocable AI-HIVE API key with limited balance or scope where possible, keep it out of public files, and avoid custom base URLs unless the endpoint is fully trusted.

Risk: The skill can upload media and download generated files.

Mitigation: Do not upload confidential, unpublished, face, voice, or client media without authorization; run the skill in an isolated environment with a controlled output directory.

Risk: Short-drama reference editing can create copyright, likeness, brand, or platform-compliance issues.

Mitigation: Use only authorized reference materials, rewrite characters, scenes, dialogue, music, and shots, and review final edits for rights, factual claims, subtitles, safe areas, and channel specifications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-ai-smart-editing)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance, JSON project briefs, shell commands, configuration snippets, and generated or edited media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call AI-HIVE APIs, upload user-selected media, poll generation tasks, and download generated results to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
