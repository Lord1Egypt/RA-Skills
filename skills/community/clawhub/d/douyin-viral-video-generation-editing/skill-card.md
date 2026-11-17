## Description:

生成与编辑抖音自然流、电商带货、商品卡和巨量千川短视频，支持文生视频、图生视频、参考视频、视频重制和延长，并通过 AI Hive 下载成片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to prompt, generate, edit, extend, poll, and download Douyin-style short video variants for organic posts, ecommerce product demos, product cards, and paid ad testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted task metadata from a custom or untrusted AI Hive base URL could cause downloaded output files to be written outside the selected output directory.

Mitigation: Use the trusted default AI Hive base URL unless you have reviewed the alternative service, run the skill with least privilege, and inspect the configured output directory before use.

Risk: The skill requires an AI Hive API key and may store or read it from local configuration or environment variables.

Mitigation: Keep the API key private, avoid sharing shell history or config files, and run the skill in a virtual environment or isolated user context.

Risk: Media files supplied for reference, editing, or upload are sent to AI Hive.

Mitigation: Upload only media you are comfortable sending to AI Hive and avoid using sensitive or unapproved assets.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/douyin-viral-video-generation-editing)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and CLI-generated JSON status output, plus downloaded media files when execution succeeds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text-to-video, image-to-video, reference-to-video, video edit, and video extend modes; output files and model details depend on AI Hive runtime responses.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
