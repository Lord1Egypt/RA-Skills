## Description:

Creates production-grade agent skills from natural language requests, including skill files, documentation, and optional helper scaffolding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acrid-auto](https://clawhub.ai/user/acrid-auto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to scaffold new agent skills from a natural language request, including inputs, outputs, deterministic steps, documentation, quality checks, and optional helper scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes new skill files by design, which can change a workspace or introduce generated instructions that have not yet been reviewed.

Mitigation: Run it in an intended target directory or branch, then review the generated SKILL.md, README.md, and file diff before enabling the generated skill.

Risk: Generated skills may include external services, credentials, posting actions, or helper scripts based on the user's request.

Mitigation: Inspect any generated setup steps, environment variables, external service calls, and helper scripts before use, and grant only the access required.

## Reference(s):

- [Acrid's Skill Creator on ClawHub](https://clawhub.ai/acrid-auto/skills/acrid-skill-creator)
- [acrid-auto publisher profile](https://clawhub.ai/user/acrid-auto)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated skill files such as SKILL.md, README.md, and optional helper or configuration files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated skills may include templates, examples, validation guidance, and optional src/ or config/ assets depending on complexity.]

## Skill Version(s):

2.0.0 (source: server release metadata, package.json, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
