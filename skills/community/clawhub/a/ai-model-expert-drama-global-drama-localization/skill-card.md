## Description:

AI大模型专家｜海外短剧多语言本地化与发行 helps short-drama and comic-drama teams turn localization and overseas distribution goals into briefs, asset plans, prompts, AI-HIVE image/video generation tasks, and delivery checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, studios, brands, ecommerce teams, and overseas distribution teams use this skill to plan and generate multilingual short-drama workflows, including story structure, character and scene boards, image/video prompts, task tracking, and delivery acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be sent to an unvalidated custom endpoint when users override the AI-HIVE base URL.

Mitigation: Use the default AI-HIVE HTTPS endpoint; avoid --base-url and AI_HIVE_BASE_URL unless the endpoint is fully trusted, and use a separate limited key for any non-default endpoint.

Risk: Credential or media exposure can occur if users upload unintended files or reuse keys after testing with an untrusted endpoint.

Mitigation: Upload only intended and authorized media, keep API keys out of public files and screenshots, and rotate the key if it may have been used with an untrusted endpoint.

Risk: Unpinned local dependencies can change behavior during setup.

Mitigation: Run setup in a dedicated virtual environment and pin the requests dependency before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-global-drama-localization)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON briefs, task IDs, and optional generated media files from AI-HIVE workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local blueprint JSON, query AI-HIVE model and pricing data, upload media, poll generation tasks, and download generated image or video results.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
