## Description:

This skill turns furniture room-placement requests into Chinese production workflows, reviewable image prompts, runnable AI-HIVE commands, and delivery checklists for furniture brands, e-commerce, interior design, and styling teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External furniture, home-goods, e-commerce, interior design, and styling teams use this skill to plan and produce marketing previews that place home products into realistic rooms. The skill helps an agent gather requirements, create visual blueprints and prompts, run AI-HIVE image generation commands when approved, and report delivery checks and risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit billable AI-HIVE generation jobs and upload selected media.

Mitigation: Review prompts, routing mode, batch size, model parameters, and media authorization before running generation; start with a small sample.

Risk: AI-HIVE API keys are required and may be stored in ~/.ai-hive/config.json.

Mitigation: Use environment variables or a protected config file, keep file permissions restricted, and do not paste keys into prompts, logs, screenshots, or repositories.

Risk: Custom base URLs can send credentials and uploaded media to untrusted endpoints.

Mitigation: Use the default official AI-HIVE base URL and avoid untrusted AI_HIVE_BASE_URL or --base-url values.

Risk: Generated room-placement images may imply product fit, scale, or claims that were not measured or verified.

Mitigation: Treat outputs as marketing previews, require manual measurement for fit and installation decisions, and label unsupported claims as pending verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/furniture-room-placement-image-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured sections, inline bash commands, and optional JSON files from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include visual blueprints, prompts, reference-image strategy, batch variant plans, AI-HIVE task records, local output paths, and acceptance checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
