## Description:

A continuously adaptive skill suite that helps Clawdbot act as a coder, business analyst, project manager, web developer, data analyst, and read-only NAS metadata scraper while adapting to user context and prioritizing free resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afajohn](https://clawhub.ai/user/afajohn)

### License/Terms of Use:


## Use Case:

Developers, analysts, and project teams use this skill for general coding help, web and data development, business analysis, project planning, free-resource discovery, and read-only NAS metadata collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad API-key access through FREE_API_KEYS.

Mitigation: Provide only task-specific, least-privileged credentials and remove or rotate them after use.

Risk: The skill includes broad, open-ended assistant behavior across coding, business analysis, web development, data work, external searches, and NAS metadata collection.

Mitigation: Use it for specific, user-approved tasks with clear scope, expected outputs, and storage boundaries.

Risk: NAS metadata scanning can expose sensitive file names, structures, or metadata even when performed read-only.

Mitigation: Limit scans to approved paths, prefer read-only mounts, and review where generated metadata is stored or shared.

## Reference(s):

- [Adaptive Suite on ClawHub](https://clawhub.ai/afajohn/skills/adaptive-suite)
- [Molt Bot Skills Documentation](https://docs.molt.bot/tools/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with prose, code snippets, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recommendations, implementation steps, schemas, or read-only metadata collection plans depending on the user task]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
