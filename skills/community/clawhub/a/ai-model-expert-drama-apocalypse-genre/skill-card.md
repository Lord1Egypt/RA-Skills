## Description:

AI大模型专家｜末日短剧 AI生成与编辑 helps short-drama and motion-comic teams turn concepts, scripts, character images, or reference videos into apocalypse-genre planning assets, prompts, AI-HIVE generation jobs, and delivery checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External short-drama creators, motion-comic studios, brand teams, e-commerce sellers, media buyers, and international release teams use this skill to plan apocalypse or survival short-drama projects and run AI-HIVE image or video generation workflows. Developers can also use the included scripts to create project blueprints, upload media, submit generation jobs, poll task status, and download results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API credentials and can store them in a local configuration file.

Mitigation: Use a dedicated, revocable API key, keep it out of public artifacts, and rotate or revoke it when no longer needed.

Risk: The scripts can upload local image, video, or audio media to AI-HIVE for generation tasks.

Mitigation: Review media before upload and confirm that referenced people, brands, music, videos, images, and trademarks are authorized for the intended use.

Risk: The skill allows a custom AI-HIVE base URL, which could redirect API traffic to an untrusted endpoint.

Mitigation: Use the default AI-HIVE endpoint unless the alternate endpoint is explicitly trusted and controlled.

Risk: Implicit invocation is enabled, so an agent could trigger this workflow while handling unrelated private content.

Mitigation: Disable or constrain implicit invocation in environments where private or unrelated user content may be present.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-apocalypse-genre)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API Base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON outputs from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON files and download generated image or video results after AI-HIVE tasks complete.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
