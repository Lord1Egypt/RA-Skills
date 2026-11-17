## Description:

AI大模型专家｜AI API中转站 helps teams organize authorized model APIs behind a unified AI-HIVE gateway for key isolation, routing, quota control, audit trails, and image/video task testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI platform operators, enterprise engineering teams, and content teams use this skill to plan a compliant AI API relay workflow and run local AI-HIVE image or video connectivity tests with task IDs and cost snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API keys and allows configurable API base URLs, which can expose credentials if configuration is unsafe or the endpoint is not trusted.

Mitigation: Use a low-privilege AI-HIVE key, keep the local configuration file private, and avoid custom base URLs unless the endpoint is fully trusted.

Risk: The image and video scripts can upload selected local media and download URLs returned by the service, creating exposure risk for sensitive files or malicious responses.

Mitigation: Upload only authorized, non-sensitive media and review endpoint and storage URL handling before using the skill with confidential content.

Risk: The security summary recommends review before installation because the skill is a local client with insufficient endpoint validation.

Mitigation: Review the skill before installing and run it in an isolated Python environment with pinned dependencies.

## Reference(s):

- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-ai-api-relay)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON files, AI-HIVE media uploads, task status JSON, and downloaded generated image or video files when the user runs the bundled scripts.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
