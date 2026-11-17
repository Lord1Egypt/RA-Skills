## Description:

Helps ecommerce teams plan and run batch SKU content workflows for AI-HIVE, including content matrices, template variables, image and video generation batches, task tracking, and review checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce, agency, and enterprise content teams use this skill to turn SKU data, authorized assets, brand rules, channel requirements, budget, and deadlines into Chinese production plans, runnable AI-HIVE commands, and quality checks for commercial image and video content batches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate batch-production safeguards such as deduplication, audit controls, and retries.

Mitigation: Use a manual task ledger, review generated plans before execution, start with a small sample batch, and confirm task status and failures before scaling.

Risk: AI-HIVE API keys and custom endpoints can expose account access or route requests to untrusted services.

Mitigation: Use a limited API key, keep keys in environment variables or the generated local config file, avoid committing credentials, and use only trusted HTTPS AI-HIVE endpoints.

Risk: Generated or downloaded ecommerce media can include inaccurate claims, unauthorized likenesses, protected brands, or content that does not fit platform rules.

Mitigation: Confirm rights to source assets, verify product claims and platform requirements, and require human review before publishing generated images or videos.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ecommerce-batch-content-factory-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated local files such as blueprint JSON, media task records, downloaded outputs, and quality checklists when the user runs the bundled scripts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
