## Description:

把电商上架套图需求转化为视觉蓝图、图片提示词、参考图策略、批量变体、AI-HIVE 生成命令和验收清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce merchants and content teams use this skill to plan listing image sets for Taobao, JD, Douyin, Pinduoduo, and cross-border platforms. It helps turn SKU images, product facts, platform rules, brand constraints, and campaign details into image plans, prompts, commands, delivery records, and review checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom AI-HIVE endpoint could expose API credentials or selected media.

Mitigation: Use the default AI-HIVE endpoint unless the custom endpoint is fully trusted, and avoid setting AI_HIVE_BASE_URL from untrusted environments.

Risk: Uploaded SKU images, brand assets, or reference media are sent to AI-HIVE for processing.

Mitigation: Upload only media the user is comfortable sending to AI-HIVE and has permission to use.

Risk: API keys may be mismanaged during setup or execution.

Mitigation: Keep AI_HIVE_API_KEY scoped and revocable, use placeholders in examples, and avoid putting keys in files, logs, screenshots, or repositories.

Risk: The workflow is Chinese-first and may be less suitable for users expecting English-first prompts or output.

Mitigation: Confirm language and platform requirements before execution and adapt prompts or deliverables when non-Chinese output is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ecommerce-listing-image-set-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown response with runnable shell commands and optional JSON files or generated media paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local JSON blueprints and can submit, poll, and download AI-HIVE generation tasks after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
