## Description:

This skill helps developers, product managers, operations teams, and independent founders plan AI-HIVE and Codex desktop-agent workflows with task decomposition, permission checks, model routing, execution records, and delivery directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a business or content-production goal into a trackable desktop-agent workflow that can compare available models, route by cost, speed, or success rate, and preserve approval and execution records. It is especially suited to Codex-assisted local work that may call AI-HIVE models for text, image, video, or other content tasks after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI_HIVE_API_KEY could be sent to an unintended server if AI_HIVE_BASE_URL is changed.

Mitigation: Keep AI_HIVE_API_KEY scoped and revocable, and leave AI_HIVE_BASE_URL unset unless the destination is fully trusted.

Risk: Paid, batch, publishing, deletion, or account-permission actions could create external or irreversible effects.

Mitigation: Require explicit user confirmation before those actions and preserve the approval record with the execution ledger.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-hot-codex-desktop-agent)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [OpenAI: ChatGPT Work and Codex](https://help.openai.com/zh-hans-cn/articles/20001275-chatgpt-work-and-codex)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, JSON files]

**Output Format:** [Markdown guidance with shell commands and JSON execution-plan files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs emphasize plan-first operation, approval gates, model-routing records, pricing snapshots, task IDs, statuses, and delivery directories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
