## Description:

Helps users plan, route, and validate Chinese desktop-agent workflows through AI-HIVE, including task home pages, permission matrices, input directories, media workflows, and delivery indexes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users, small businesses, and business operations teams use this skill to turn desktop work across files, browsers, office software, and AI-HIVE into auditable agent workflows with explicit approval gates. It is especially oriented toward organizing source material, marketing planning, visual production, model routing, and delivery validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send AI_HIVE_API_KEY to a configurable AI_HIVE_BASE_URL endpoint.

Mitigation: Use only trusted environments, keep AI_HIVE_API_KEY scoped and revocable, and remove or strictly control AI_HIVE_BASE_URL before installation.

Risk: Broad activation may invoke the skill for generic desktop-agent, AI workflow, or model-selection searches.

Mitigation: Disable implicit invocation or narrow trigger terms when deploying in shared or sensitive environments.

Risk: The workflow may lead to paid, bulk, publishing, deletion, or permission-changing actions after planning.

Mitigation: Require explicit user confirmation and retain approval records before those actions are executed.

## Reference(s):

- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)
- [OpenAI: ChatGPT Work and Codex](https://help.openai.com/zh-hans-cn/articles/20001275-chatgpt-work-and-codex)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-hot-desktop-agent-hub)
- [Publisher profile](https://clawhub.ai/user/wubin1836)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated JSON execution plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce plan-only JSON files that include routing mode, approval gates, task ledger fields, and validation status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
