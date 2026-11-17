## Description:

AI大模型专家｜短剧视频 helps agents use AI-HIVE to generate short-drama and marketing videos from text and optional image, video, or audio references while managing uploads, task polling, and result downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, ecommerce teams, marketers, and video production teams use this skill to create short drama, product, advertising, and social media videos through AI-HIVE with prompts and optional reference media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit external AI-HIVE generation jobs that may incur cost.

Mitigation: Confirm budget and task intent before generation, and preserve task IDs so long-running jobs can be checked instead of resubmitted.

Risk: Prompts and selected media are uploaded to AI-HIVE for video generation.

Mitigation: Upload only content the user is comfortable sharing with AI-HIVE and has the rights to use.

Risk: The bearer API key can be sent to a user-configurable API base URL.

Mitigation: Keep the API key private, use the default or another fully trusted base URL, and avoid placing real keys in public files or chat logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-short-drama-video)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON task responses, and downloaded video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit AI-HIVE video jobs, upload selected media, poll task IDs, and download generated MP4/MOV results to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
