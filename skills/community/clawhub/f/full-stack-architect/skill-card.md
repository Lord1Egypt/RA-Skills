## Description:

灵枢·AI全栈构建师 provides full-stack development guidance across frontend, backend, mobile, game development, architecture, PRD generation, code templates, quality review, and deployment planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drip618](https://clawhub.ai/user/drip618)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and build software projects from requirements through architecture, implementation, review, and deployment. It is suited for technical guidance, rapid prototypes, PRD workflows, technology selection, generated code, and reusable development patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Executable helpers can run code or shell commands with broad local effects.

Mitigation: Review the helpers before installation, and do not run code-execution features on untrusted, user-supplied, or model-generated input.

Risk: AI provider adapters use environment API keys and configurable endpoints.

Mitigation: Restrict allowed provider endpoints, use least-privilege keys, and avoid exposing sensitive environment variables to untrusted prompts or generated code.

Risk: Generated PRDs, code, recommendations, and knowledge artifacts may be written to local paths.

Mitigation: Run the skill in an approved project workspace and review output paths before allowing generated-code writes.

Risk: Backup and scheduled update helpers can modify files and run shell commands.

Mitigation: Keep backup or scheduled update scripts disabled until their paths, command construction, and shell usage are reviewed and fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drip618/skills/full-stack-architect)
- [Release notes](docs/RELEASE_NOTES.md)
- [AI and machine learning reference](references/ai_machine_learning.md)
- [Backend frameworks reference](references/backend_frameworks.md)
- [Backend performance reference](references/backend_performance.md)
- [Cloud native and DevOps reference](references/cloud_native_devops.md)
- [Composition patterns reference](references/composition_patterns.md)
- [Computer networking reference](references/computer_networking.md)
- [Data structures and algorithms reference](references/data_structures_algorithms.md)
- [Database best practices reference](references/database_best_practices.md)
- [Frontend best practices reference](references/frontend_best_practices.md)
- [Frontend frameworks reference](references/frontend_frameworks.md)
- [Frontend performance reference](references/frontend_performance.md)
- [Game development reference](references/game_development.md)
- [Go best practices reference](references/go_best_practices.md)
- [Knowledge system reference](references/knowledge_system.md)
- [Mobile development reference](references/mobile_development.md)
- [Node.js best practices reference](references/nodejs_best_practices.md)
- [Security best practices reference](references/security_best_practices.md)
- [Software engineering reference](references/software_engineering.md)
- [Vue best practices reference](references/vue_best_practices.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text with code blocks, shell commands, JSON, YAML, and generated project files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated PRDs, code files, configuration files, quality reports, recommendations, and knowledge artifacts inside the active project workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
