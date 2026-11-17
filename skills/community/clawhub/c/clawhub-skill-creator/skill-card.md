## Description:

Create effective skills for clawhub registry. Use when: (1) Creating new skill for publication, (2) Updating existing skill metadata, (3) Optimizing skill structure for AI agents, (4) Validating skill before publish, (5) Understanding clawhub-specific requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erview](https://clawhub.ai/user/erview)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to create, update, validate, package, and publish ClawHub-compatible skills with agent-first structure, metadata, references, versioning, and token optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaging script can unintentionally include sensitive files when creating publishable packages.

Mitigation: Review packages before publishing; do not run the packaging script on directories containing .env files, keys, credentials, private config, or symlinks, and inspect the generated archive contents before publishing.

## Reference(s):

- [Clawhub Skill Creator](https://clawhub.ai/erview/skills/clawhub-skill-creator)
- [Agent-First Design](references/agent-first-design.md)
- [Skill Structure Patterns](references/skill-structure.md)
- [Token Optimization](references/token-optimization.md)
- [Validation Checklist](references/validation-checklist.md)
- [Versioning Best Practices](references/versioning.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline JSON, bash, cmd, and PowerShell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces skill-authoring guidance and command templates; bundled shell scripts can initialize or package skill files.]

## Skill Version(s):

1.0.0 (source: _meta.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
