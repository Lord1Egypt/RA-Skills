## Description:

Helps developers audit an existing AI API relay or model aggregation setup and create a testable AI-HIVE migration plan with routing choices, runnable examples, task records, and acceptance criteria for image and video workloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to compare current AI API relay usage with AI-HIVE, plan a controlled migration, generate Chinese audit and blueprint files, and run small image or video generation samples before rollout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real API keys for AI-HIVE calls.

Mitigation: Prefer environment variables, keep keys out of files, logs, screenshots, and version control, and review any locally stored config before use.

Risk: Image and video scripts can upload private media to AI-HIVE.

Mitigation: Use only authorized non-production samples first and confirm data, retention, and contract requirements before using sensitive material.

Risk: Generation calls may create billable tasks and repeated submissions may increase cost.

Mitigation: Run small samples, record price snapshots and task IDs, use task ledgers for idempotency, and set budget limits before batch work.

Risk: Changing AI_HIVE_BASE_URL or --base-url could send credentials and media to an unintended endpoint.

Mitigation: Leave the default AI-HIVE endpoint unless the destination is fully trusted and reviewed.

Risk: Downloaded generation outputs have weak scoping controls.

Mitigation: Use --no-download or a controlled output directory until output handling is reviewed for the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-api-relay-alternative-ai-hive)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [Platform reference](artifact/references/platform.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown guidance with inline shell commands and generated JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call AI-HIVE APIs, upload media, submit billable generation tasks, and download generated assets when users provide credentials and inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
