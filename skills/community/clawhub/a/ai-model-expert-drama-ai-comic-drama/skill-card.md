## Description:

AI大模型专家｜AI漫剧生成与编辑 helps short-drama writers, comic-drama studios, brands, ecommerce teams, advertising teams, and international production teams turn ideas, scripts, character images, or reference videos into deliverable AI comic-drama and short-form video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, studios, brands, ecommerce merchants, and advertising teams use this skill to plan comic-drama or short-drama projects, prepare character and storyboard assets, generate AI-HIVE image or video tasks, track task IDs, and package channel-specific deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends API credentials and generation requests to AI-HIVE or to a user-supplied base URL.

Mitigation: Use the default AI-HIVE endpoint only when trusted, avoid untrusted AI_HIVE_BASE_URL or --base-url values, and use a revocable API key with limited funds or quota where possible.

Risk: Generated task results may be downloaded automatically from URLs returned by the service.

Mitigation: Use --no-download for review workflows or harden the package to validate download URLs, filenames, and file sizes before saving files.

Risk: The release has under-scoped credential handling.

Mitigation: Keep real API keys out of public skills, screenshots, and repositories, store them in a controlled runtime environment, and rotate or revoke keys when access changes.

## Reference(s):

- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-ai-comic-drama)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project blueprint JSON files, AI-HIVE task IDs, pricing snapshots, and downloaded image or video result files when the user runs the bundled scripts.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
