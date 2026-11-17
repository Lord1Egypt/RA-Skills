## Description:

AI大模型专家｜Seedance 2.5 视频生成与编辑 helps users generate, edit, extend, track, and download Seedance 2.5 video tasks through AI-HIVE from prompts, product images, reference media, or existing clips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing teams, e-commerce merchants, brand content teams, short-drama or comic-video producers, and social media creators use this skill to run Seedance 2.5 text-to-video, image-to-video, reference-video, video-editing, and video-extension workflows through AI-HIVE. The skill guides setup, media upload, routing mode selection, task submission, polling, and result download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom API endpoint override could send the user's AI-HIVE API key to an untrusted server.

Mitigation: Use the default AI-HIVE endpoint and avoid AI_HIVE_BASE_URL or --base-url unless the endpoint is fully trusted.

Risk: The dependency installation guidance does not pin the requests package version.

Mitigation: Install dependencies in a virtual environment and review or pin dependency versions before operational use.

Risk: Video generation and media uploads can spend account balance or expose uploaded assets.

Mitigation: Use a dedicated low-limit API key and verify generated tasks, media uploads, routing choices, and pricing snapshots before submitting high-cost work.

## Reference(s):

- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-seedance-2-5-video-generation-editing)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash commands and JSON task or status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download generated video files and last-frame images to a local output directory when users do not choose no-download mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
