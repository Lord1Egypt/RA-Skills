## Description:

Helps e-commerce operators, brand teams, livestream commerce teams, and content creators use AI-HIVE to generate or edit Taobao-focused product videos from text and optional image, video, or audio references, then track tasks and download finished videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, e-commerce merchants, brand teams, and developers use this skill to prepare prompts and run AI-HIVE video generation or editing workflows for product videos, ads, social commerce clips, short drama, and related campaign assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be forwarded to an untrusted service if a custom base URL is supplied.

Mitigation: Use only the official AI-HIVE endpoint, avoid untrusted --base-url or AI_HIVE_BASE_URL values, and rotate any API key used with a custom endpoint.

Risk: The skill can upload private media and submit jobs that may consume account credits.

Mitigation: Confirm media sensitivity, usage rights, task scope, and budget before uploading files or submitting generation jobs.

Risk: Generated videos may contain unsupported product claims, copied branding, or misleading depictions if prompts or references are not reviewed.

Mitigation: Review prompts, references, product facts, rights, and final outputs before publication or ad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-taobao-ecommerce-video-generation-editing)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown instructions, shell commands, JSON task responses, and downloaded media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload user-provided media, submit credit-consuming AI-HIVE jobs, save task IDs, and download generated video outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
