## Description:

This skill helps developers, AI applications, content platforms, and batch generation operators diagnose failed AI-HIVE model tasks and produce repair plans, runnable commands, retry strategies, task recovery steps, and review checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI applications, content platforms, and batch generation operators use this skill to classify AI-HIVE task failures, repair parameters, plan model fallback, manage idempotent retries, and restore asynchronous generation task state for ecommerce, advertising, marketing, short-video, and social content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be exposed to the tool or stored locally.

Mitigation: Use a dedicated AI-HIVE API key with limited tolerance for exposure, prefer environment variables or a protected local config, and never place keys in prompts, logs, code, screenshots, or submitted files.

Risk: Image or video generation can create billable tasks or duplicate charges.

Mitigation: Require manual confirmation of final parameters, routing mode, and cost expectations before submission, and keep task IDs, input hashes, pricing snapshots, and retry records for deduplication.

Risk: Custom base URLs or media uploads may send data to endpoints the user does not control.

Mitigation: Use the default AI-HIVE endpoint unless the user fully controls the replacement endpoint, and upload only files the user intends to send to AI-HIVE.

Risk: Generated guidance or content may include unsupported claims, unauthorized reference use, or misleading commercial outputs.

Mitigation: Verify source facts, rights to reference assets, product claims, and platform constraints before using generated commands or publishing generated content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-task-repair-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE OpenAPI base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline shell commands, JSON snippets, and optional generated files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit billable AI-HIVE image or video tasks only after user confirmation; helper scripts can upload media and download generated results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
