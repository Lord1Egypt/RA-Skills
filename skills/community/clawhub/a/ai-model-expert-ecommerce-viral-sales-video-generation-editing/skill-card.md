## Description:

Generates and edits ecommerce sales videos through AI-HIVE by uploading optional media, submitting video model jobs, polling task status, and downloading finished outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, ecommerce operators, brand teams, and marketing/video teams use this agent to generate or edit product videos, ads, social commerce clips, and related media through AI-HIVE without writing API code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the user's AI-HIVE API key to a configured base URL.

Mitigation: Use only the official AI-HIVE endpoint and avoid setting --base-url, AI_HIVE_BASE_URL, or config base_url to any other server.

Risk: Automatic invocation can upload local media and submit chargeable generation tasks.

Mitigation: Review the invocation before allowing uploads or task submission, and confirm budget for batch or high-cost video jobs.

Risk: Generated commercial videos can contain incorrect product claims, identity misuse, trademark misuse, or unlicensed reference material.

Mitigation: Verify product facts, rights to reference assets, brand usage, and final output suitability before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-ecommerce-viral-sales-video-generation-editing)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON task/status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload user-selected media to AI-HIVE, print task IDs and status payloads, and download generated video or image files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
