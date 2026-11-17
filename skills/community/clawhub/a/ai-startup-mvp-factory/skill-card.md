## Description:

AI Startup MVP Factory automates an end-to-end MVP workflow from startup idea and PRD generation through code generation, review, and containerized deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Independent developers, startup teams, and product or technical leads use this skill to turn a product idea into a structured PRD, generated application code, review outputs, and deployable container configuration for MVP validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may modify repositories, create pull requests, update wiki content, build containers, push images, or produce deployable artifacts without clearly documented approval gates or target limits.

Mitigation: Require explicit confirmation before each external write or publish step, verify target repositories and registries, and use least-privilege credentials.

Risk: Generated code and deployment assets may be incomplete, insecure, or mismatched to the intended production environment.

Mitigation: Review generated code and configuration, run security and quality checks, and validate deployment settings before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/ai-startup-mvp-factory)
- [Artifact README](artifact/README.md)
- [Workflow definition](artifact/workflow.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown documents, source code, JSON workflow outputs, and deployment configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce PRD content, project files, code review reports, Docker assets, deployment configuration, and release notes.]

## Skill Version(s):

1.0.0 (source: server release metadata and workflow.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
