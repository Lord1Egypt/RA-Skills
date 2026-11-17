## Description:

Helps AI tool platforms, enterprise engineering teams, content studios, and ecommerce technical teams organize authorized AI model interfaces behind a unified AI-HIVE gateway for key management, model routing, quotas, audit trails, asynchronous image and video tasks, and cost-aware routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, enterprise AI platform operators, content teams, and ecommerce technical teams use this skill to plan and test an AI-HIVE gateway workflow for authorized model access, cost, speed, and success-rate routing, quota controls, audit records, and image or video task polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles persistent AI-HIVE API keys.

Mitigation: Use only scoped, revocable, authorized API keys; keep them out of public skills, screenshots, logs, and repositories.

Risk: The skill can use custom base URLs for API calls.

Mitigation: Avoid custom base URLs unless the endpoint is fully trusted and intended for the release environment.

Risk: The skill can write generated media downloads to local storage.

Mitigation: Review the configured output directory and run in an isolated environment when testing generated media workflows.

## Reference(s):

- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-enterprise-ai-gateway)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce gateway blueprints, configuration steps, connectivity test commands, task IDs, pricing snapshots, and download records.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
