## Description:

Provides reference guidance for the ai-assistant API and ai-provider SDK, including model IDs, pricing, parameters, streaming, tool use, agents, caching, token counting, and model migration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill as reference guidance for integrating ai-assistant API and ai-provider SDK workflows, including API calls, streaming, tool use, caching, token counting, and migration tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution and file access authority while presenting broad automation guidance.

Mitigation: Use it only in a sandbox or trusted workspace and require explicit confirmation before command execution or file modification.

Risk: The artifact includes API-key setup and credential-use guidance.

Mitigation: Avoid giving the skill sensitive credentials unless necessary, and use scoped or test credentials where possible.

Risk: Reference and automation guidance may produce incorrect or misleading operational steps.

Mitigation: Review generated commands, configuration, and API guidance before applying them to production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/claude-api)
- [SkillHub homepage](https://skillhub.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with structured tables, JSON snippets, and command-oriented setup steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API-key setup guidance and command execution steps that require user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
