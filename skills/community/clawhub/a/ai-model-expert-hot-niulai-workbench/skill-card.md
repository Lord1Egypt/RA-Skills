## Description:

Helps Chinese AI model users, developers, and enterprise evaluators verify model identity, test capabilities, plan reusable AI-HIVE workflows, route by cost, speed, or success rate, and compare results for Niulai, Ox Alpha, GLM-5.3, and related AI-HIVE searches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese AI model users, developers, and enterprise evaluators use this skill to turn searches around Niulai, Ox Alpha, GLM-5.3, Zhipu AI, and AI-HIVE into verifiable model identity checks, task templates, routing plans, and result comparisons. It is intended for planning and guided execution where current model availability, pricing snapshots, task IDs, and human approval gates matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send AI_HIVE_API_KEY to an environment-controlled endpoint if AI_HIVE_BASE_URL is changed.

Mitigation: Keep AI_HIVE_API_KEY confined to a trusted environment and set AI_HIVE_BASE_URL only for endpoints you fully trust.

Risk: The skill describes routing, pricing, identity-check, and task-ledger safeguards that the included code does not fully implement by itself.

Mitigation: Treat those safeguards as workflow guidance unless separate AI-HIVE tools perform them with explicit user confirmation.

Risk: The server security verdict is suspicious because the skill is mostly a planning helper but can interact with external AI-HIVE services.

Mitigation: Review the skill before deployment, confirm intended AI-HIVE use, and require human approval for paid, batch, external publishing, deletion, or privilege-changing actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-hot-niulai-workbench)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [Zhipu GLM-5.3-Flash reference](https://www.zhipuai.cn/zh/research/163)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON plans, shell command examples, and validation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce AI-HIVE workflow plans, model-query commands, execution ledgers, task templates, and result-comparison guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
