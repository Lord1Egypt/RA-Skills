## Description:

Use when adding docstrings, creating API documentation, or building documentation sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhwa8685](https://clawhub.ai/user/lhwa8685)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to add maintainable docstrings, API documentation, documentation-site assets, tutorials, and coverage reports for software projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated documentation-site and interactive API portal configurations may normalize persisted API authorization, credentialed browser requests, mutable remote scripts, or unpinned package execution.

Mitigation: Review generated portal and site configuration before use, pin package and CDN versions, disable persisted API authorization unless controlled, and avoid sending browser credentials from try-it consoles by default.

Risk: Generated documentation may be inaccurate or misleading if code examples, API schemas, or error behavior are not verified against the target project.

Mitigation: Validate examples, rendered API docs, and coverage reports against the project before publishing or deploying the documentation.

## Reference(s):

- [Python Docstrings](references/python-docstrings.md)
- [TypeScript JSDoc](references/typescript-jsdoc.md)
- [API Documentation: FastAPI & Django](references/api-docs-fastapi-django.md)
- [API Documentation: NestJS & Express](references/api-docs-nestjs-express.md)
- [Coverage Reports](references/coverage-reports.md)
- [Documentation Systems & Infrastructure](references/documentation-systems.md)
- [Interactive API Documentation](references/interactive-api-docs.md)
- [User Guides & Tutorials](references/user-guides-tutorials.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks, configuration snippets, documentation text, and coverage summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed for accuracy and tested where examples, generated specs, or documentation-site configuration are produced.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
