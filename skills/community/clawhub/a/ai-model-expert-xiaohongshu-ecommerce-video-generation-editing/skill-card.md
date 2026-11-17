## Description:

AI大模型专家｜小红书 电商视频生成与编辑 helps agents generate and edit ecommerce or social-commerce videos through AI-HIVE by preparing prompts and media, submitting jobs, polling task status, and downloading finished results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, ecommerce operators, brand teams, marketers, and content production teams use this skill to produce product videos, ads, short-form social content, and video edits for Xiaohongshu and related commerce channels. It is useful when an agent needs to turn text prompts and optional reference media into AI-HIVE video-generation jobs and track the resulting task output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected media are sent to AI-HIVE for video generation.

Mitigation: Install and invoke the skill only when AI-HIVE use is intended, and confirm with the user before submitting generation jobs.

Risk: Broad implicit invocation can trigger the workflow for comparison-only or exploratory requests.

Mitigation: Avoid automatic use unless the user asks to generate, edit, submit, poll, upload, or download an AI-HIVE video task.

Risk: API key and base URL handling require manual review.

Mitigation: Keep the API key private, do not place it in public prompts or repositories, and do not point base_url at untrusted hosts.

Risk: Downloaded outputs may be written to a user-selected output directory.

Mitigation: Choose an output directory where accidental overwrites or unexpected downloaded files would have limited impact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-xiaohongshu-ecommerce-video-generation-editing)
- [AI-HIVE entry point](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON task or status data; generated media is saved as video or image files by the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an AI-HIVE API key, user prompts, optional media inputs, routing mode, model parameters, task IDs, and an output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
