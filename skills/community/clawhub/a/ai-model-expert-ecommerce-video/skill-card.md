## Description:

AI大模型专家｜电商视频 helps ecommerce, brand, live-commerce, and content teams generate product and advertising videos through AI-HIVE from text and optional image, video, or audio references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, brand product teams, live-commerce teams, and commercial content creators use this skill to create ecommerce videos, ads, TVC-style clips, product showcases, social-commerce content, and short-form narrative videos. The skill guides AI-HIVE task setup, media upload, routing choice, task tracking, and result download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected media may be sent to AI-HIVE for remote video generation and may create service charges.

Mitigation: Use only approved assets, review real-time pricing before bulk work, and confirm budget before submitting high-volume or high-cost tasks.

Risk: A configurable API endpoint could expose the AI-HIVE API key to an unintended host.

Mitigation: Use a dedicated limited API key and confirm the configured base_url is the legitimate AI-HIVE endpoint before running commands.

Risk: Generated ecommerce video can contain inaccurate product claims, brand misuse, or unauthorized third-party references.

Mitigation: Validate product facts, brand permissions, media rights, and final video content before publication or ad use.

## Reference(s):

- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [ClawHub Skill Listing](https://clawhub.ai/wubin1836/skills/ai-model-expert-ecommerce-video)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with CLI commands, task identifiers, status text, and downloaded video files when generation succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload user-provided media to AI-HIVE, submit paid remote generation jobs, poll task status, and save generated media to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
