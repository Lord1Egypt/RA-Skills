## Description:

Coordinates phased evolution of a star-shaped memory architecture, including architecture health checks, phase status reporting, external project analysis, and evolution report generation.

This skill is for research and development only.

## Publisher:

[whoisme007](https://clawhub.ai/user/whoisme007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and architecture maintainers use this skill to coordinate OpenClaw memory-architecture evolution, check phase and health status, analyze external projects for integration ideas, and produce Markdown or JSON evolution reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes under-scoped local code execution through health checks that run or import workspace test and adapter files.

Mitigation: Run health checks only in trusted OpenClaw workspaces after reviewing the referenced tests, adapters, and workspace paths.

Risk: The skill includes a hardcoded personal email report path and email-password environment variable guidance.

Mitigation: Remove or reconfigure the report recipient before use and prefer managed secret storage over plain environment variables for email credentials.

Risk: The skill is tailored to a specific OpenClaw workspace layout with hardcoded local paths.

Mitigation: Configure workspace paths for the target environment and verify missing-path behavior before relying on generated health or phase reports.

Risk: External project analysis fetches GitHub README content and may use a GitHub token.

Mitigation: Use least-privileged tokens, avoid passing sensitive private repositories unless intended, and review generated fusion proposals before implementation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/whoisme007/skills/architecture-evolution-coordinator)
- [Full Evolution Guide](artifact/prompts/full_evolution_guide.md)
- [NeverOnce Example Analysis Target](https://github.com/WeberG619/neveronce)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON reports with command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include phase status, system health metrics, external project concept mappings, fusion proposals, implementation roadmaps, and email-reporting configuration.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
