## Description:

AI电商专家｜音频参考生成视频 helps ecommerce content teams prepare IMIVA video generation tasks that use reference audio to guide product video rhythm, mood, audio direction, budget checks, task tracking, and result review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, brand content teams, ad makers, video editors, and social commerce teams use this skill to turn product assets, confirmed selling points, channel requirements, and reference audio into IMIVA video generation requests. It guides credit checks, dry runs, paid task confirmation, task lookup, and quality review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow runs a mutable npm MCP client with the user's IMIVA token and inherited environment.

Mitigation: Use a dedicated low-privilege IMIVA token, run it in an environment without unrelated secrets, prefer a pinned reviewed npm package version, and avoid unnecessary API URL overrides.

Risk: Video generation can consume credits when a paid task is submitted.

Mitigation: Run a dryRun first, confirm estimatedCredits and maxCredits with the user, and use a unique idempotencyKey before creating the task.

Risk: Generated ecommerce videos may include inaccurate product claims or unauthorized reference material.

Mitigation: Use only user-confirmed product facts and authorized media, then review product accuracy, claims, rights, channel fit, and call to action before publishing.

## Reference(s):

- [IMIVA AI Ecommerce Expert Homepage](https://imiva.ecpro.com/)
- [Example MCP Client Configuration](references/mcp-config.example.json)
- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-audio-reference-video)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON MCP arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include IMIVA task IDs, estimated credit guidance, idempotency-key reminders, and video review criteria.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
