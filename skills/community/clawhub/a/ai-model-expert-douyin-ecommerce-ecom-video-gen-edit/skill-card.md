## Description:

AI大模型专家｜抖音电商 电商视频生成与编辑 helps e-commerce operators, brand teams, livestream commerce teams, and commercial content creators use AI-HIVE to generate, edit, track, and download product and advertising videos from text and optional image, video, or audio references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create and revise Douyin e-commerce videos, product demos, social commerce ads, short drama clips, and related commercial media through AI-HIVE. The skill can submit video jobs, upload reference media, preserve task IDs, poll job status, and download generated outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API credentials.

Mitigation: Use a limited and rotatable API key, keep it out of chats and public repositories, and store it through the documented config file or environment variable.

Risk: The skill can upload local media and submit paid external video generation jobs.

Mitigation: Require explicit confirmation before uploads or job submission, check the live pricing snapshot, and confirm budget before batch or high-cost tasks.

Risk: Changing the API base URL could send credentials or media to an unexpected service.

Mitigation: Keep the base URL at the documented AI-HIVE endpoint unless a trusted administrator has approved a different endpoint.

Risk: Implicit invocation could start uploads or job submissions before a user has reviewed inputs.

Mitigation: Configure the host agent to ask for confirmation before executing this skill with user media, API keys, or chargeable generation requests.

## Reference(s):

- [AI-HIVE Chat](https://ai-hive.iclip.cn/chat)
- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-model-expert-douyin-ecommerce-ecom-video-gen-edit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and downloaded video or image files from AI-HIVE tasks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce task IDs, media IDs, JSON task responses, and generated MP4/MOV or image files depending on command options and model support.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
