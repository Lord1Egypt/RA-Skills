## Description:

Guides users to create safer, clearer data-analysis prompts and templates across common analysis, extraction, SQL, reporting, web-collection, and methodology-distillation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to turn data-analysis needs into structured prompts, validation checklists, templates, and workflow guidance. It is intended for guided data work and methodology distillation, not direct production database access, ML model building, or pure summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated web-scraping and dynamic API templates may be used outside their intended public-data and terms-compliant boundaries.

Mitigation: Review scraping templates before installation or use, require robots.txt and Terms of Service checks, and do not use the skill for paywalls, login/session bypass, anti-bot bypass, or production databases.

Risk: Users may expose cookies, API keys, Feishu tokens, or other sensitive values while configuring generated examples.

Mitigation: Do not paste real secrets into chat; require .env-based local secret handling, sensitive_fields configuration, and preview/redaction before any cloud upload.

Risk: Cloud-upload templates can move sensitive or regulated data to Feishu or other external services.

Mitigation: Use data minimization, local-first processing, explicit sensitive-field redaction, and a human review step before uploading generated outputs.

Risk: Scheduled-task examples or generated shell commands may run with higher privilege than necessary.

Mitigation: Remove /rl HIGHEST from scheduled-task examples unless an administrator has a specific reason and review command side effects before execution.

Risk: The distillation entry can modify the skill's own method library, routing files, indexes, and tests.

Mitigation: Require a pre-write review list, limit each mount to five methods, back up existing files before modification, and review the resulting diff before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardwason/skills/data-prompt-coach)
- [Publisher profile](https://clawhub.ai/user/edwardwason)
- [Project homepage](https://github.com/EdwardWason/data-prompt-coach)
- [Methodology index](assets/INDEX.md)
- [Security compliance guidance](references/audit/security-compliance.md)
- [Rollback policy](references/audit/rollback-policy.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code, shell-command, JSON, SQL, CSV, and template files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local files and templates only after the user provides enough context and approves relevant write actions.]

## Skill Version(s):

3.4.4 (source: frontmatter and server release evidence, released 2026-07-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
