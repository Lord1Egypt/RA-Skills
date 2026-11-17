## Description:

Helps apparel brands, photography teams, cross-border sellers, and product designers turn AI apparel model-swap requests into reviewable workflows, prompts, runnable AI-HIVE commands, and delivery checklists for model-swapped ecommerce visuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and commercial apparel teams use this skill to plan and execute AI-HIVE based model-swap image workflows for ecommerce, advertising, social commerce, and marketing assets while preserving apparel structure and texture. It supports brief generation, prompt and reference strategy, small-batch generation, task tracking, and final quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API client can forward credentials and user-selected media to configured endpoints.

Mitigation: Install only for intended AI-HIVE workflows, keep the base URL on the official AI-HIVE endpoint, review commands before execution, and upload only media the user is authorized to use.

Risk: The helper can persist an AI-HIVE API key locally.

Mitigation: Prefer environment variables for valuable production keys, trust the local environment before storing credentials, and avoid exposing keys in files, logs, screenshots, or version control.

Risk: Generated apparel visuals can misrepresent product details, people, rights, or commercial claims.

Mitigation: Require human review of apparel structure, colors, logos, permissions, and claims before publication, and do not use the skill for unauthorized likeness replication, fake endorsements, or platform-rule evasion.

## Reference(s):

- [AI-HIVE product entry](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/apparel-model-swap-ai-hive)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash commands and generated JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit AI-HIVE image generation tasks, upload authorized media, poll asynchronous task status, and download generated image files when the user confirms parameters and credentials are available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
